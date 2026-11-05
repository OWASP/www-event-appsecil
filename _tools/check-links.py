"""Check built-site links; optionally probe external conference-archive links.

Build the site first, then run: python _tools/check-links.py --external
Reports are written beside this script. External fragments are not checked.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / '_site'
ORIGIN = 'https://appsecil.org'


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.add(attrs['name'])
        for attr in ('href', 'src', 'poster'):
            if attrs.get(attr) and not (tag == 'link' and attrs.get('rel') in ('preconnect', 'dns-prefetch')):
                self.links.append(attrs[attr])


def probe(url):
    attempts = [url]
    if url.startswith('http:'):
        attempts.append('https:' + url[5:])
    last = None
    for candidate in attempts:
        try:
            request = Request(candidate, headers={'User-Agent': 'Mozilla/5.0 (OWASP Israel link checker)'})
            with urlopen(request, timeout=15) as response:
                response.read(1024)
                return {'url': url, 'status': response.status, 'result': 'ok', 'final_url': response.url}
        except HTTPError as error:
            last = {'url': url, 'status': error.code, 'result': 'broken' if error.code in (404, 410) else 'unverified', 'detail': str(error)}
        except Exception as error:
            last = {'url': url, 'result': 'unverified', 'detail': str(error)}
    return last


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external', action='store_true')
    parser.add_argument('--site', type=Path, default=SITE, help='Built site directory (default: _site).')
    parser.add_argument('--reuse-external', action='store_true', help='Reuse recorded external results; probe only new URLs.')
    args = parser.parse_args()
    site = args.site.resolve()
    documents = {p: Document(p.read_text(encoding='utf-8')) for p in site.rglob('*.html')}
    if not documents:
        raise SystemExit('Build the site before running this checker.')
    internal = {}
    external = {}
    checked = 0
    for page, document in documents.items():
        relative = page.relative_to(site).as_posix()
        page_url = '/' + relative
        if page_url.endswith('index.html'):
            page_url = page_url[:-10]
        archive = relative.split('/')[0] in {str(y) for y in range(2007, 2017)} or relative == 'conferences/index.html'
        for link in document.links:
            resolved = urljoin(ORIGIN + page_url, link)
            parsed = urlparse(resolved)
            if parsed.scheme not in ('http', 'https'):
                continue
            if parsed.hostname not in ('appsecil.org', 'www.appsecil.org'):
                if archive:
                    external.setdefault(resolved.split('#')[0], set()).add(page_url)
                continue
            checked += 1
            target = site / unquote(parsed.path).lstrip('/')
            if target.is_dir():
                target /= 'index.html'
            # GitHub Pages serves extensionless requests from matching .html files.
            if not target.is_file() and not target.suffix and target.with_suffix('.html').is_file():
                target = target.with_suffix('.html')
            issue = None
            if not target.is_file():
                issue = 'missing file'
            elif parsed.fragment and target in documents:
                fragment = unquote(parsed.fragment)
                if fragment not in documents[target].ids and not fragment.startswith(':~:text='):
                    issue = 'missing anchor'
            if issue:
                key = (resolved, issue)
                internal.setdefault(key, set()).add(page_url)
    results = []
    if args.external or args.reuse_external:
        cached = {}
        previous = ROOT / '_tools/link-check-report.json'
        if args.reuse_external and previous.exists():
            cached = {r['url']: r for r in json.loads(previous.read_text(encoding='utf-8'))['external_results']}
        print(f'Checking {len(external)} external archive URLs...', flush=True)
        with ThreadPoolExecutor(max_workers=12) as pool:
            results.extend(dict(cached[url], pages=sorted(external[url])) for url in sorted(external) if url in cached)
            futures = [pool.submit(probe, url) for url in sorted(external) if url not in cached]
            for index, future in enumerate(as_completed(futures), 1):
                result = future.result()
                result['pages'] = sorted(external[result['url']])
                results.append(result)
                if index % 25 == 0:
                    print(f'{index}/{len(external)} checked', flush=True)
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'html_pages': len(documents),
              'internal_references_checked': checked,
              'internal_issues': [{'url': url, 'issue': issue, 'pages': sorted(pages)} for (url, issue), pages in sorted(internal.items())],
              'external_scope': 'Conference history and 2007–2016 archive pages; external fragments are not checked.',
              'external_results': sorted(results, key=lambda result: result['url'])}
    (ROOT / '_tools/link-check-report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    lines = ['# Link check', '', f"Checked {len(documents)} built HTML pages and {checked} internal references.", '', '## Internal issues', '']
    for issue in report['internal_issues']:
        lines.append(f"- {issue['issue']}: `{issue['url']}` — {', '.join(issue['pages'])}")
    if not internal:
        lines.append('None.')
    for category in ('broken', 'unverified'):
        subset = [result for result in report['external_results'] if result['result'] == category]
        lines.extend(['', f'## External: {category} ({len(subset)})', ''])
        for result in subset:
            lines.append(f"- {result['url']} — {result.get('status', result.get('detail'))}; pages: {', '.join(result['pages'])}")
    lines.extend(['', report['external_scope'], '', 'HTTP 404/410 responses are reported as broken. Other failures require manual review; bot blocking, expired TLS certificates and unavailable hosts are not treated as confirmed missing pages.', ''])
    (ROOT / '_tools/link-check-report.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'{len(documents)} HTML pages; {checked} internal references; {len(internal)} internal issues.')
    print('External:', {category: sum(r['result'] == category for r in results) for category in ('ok', 'broken', 'unverified')})


if __name__ == '__main__':
    main()
