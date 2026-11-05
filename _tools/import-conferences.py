"""Preserve the legacy OWASP conference pages and their wiki-hosted assets.

Install _tools/conference-requirements.txt into .bundle/conference-import first.
Run from any directory. Existing downloads are reused; failures are recorded.
"""
import concurrent.futures
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.bundle/conference-import'))
from bs4 import BeautifulSoup, Comment
import importlib.util
_spec = importlib.util.spec_from_file_location("conference_pages", Path(__file__).with_name("conference-pages.py"))
_renderer = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_renderer)

WIKI = 'https://wiki.owasp.org'
PAGES = {year: ('AppSec_Israel_' if year >= 2014 else 'OWASP_Israel_') + str(year)
         for year in range(2007, 2017)}
PAGES[2007] += '_Conference'
PAGES[2008] += '_Conference_at_the_Interdisciplinary_Center_Herzliya'
ARCHIVE = ROOT / 'assets/conferences'
ARCHIVE.mkdir(parents=True, exist_ok=True)
assets = {}


def fetch(url):
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (OWASP Israel history preservation)'}), timeout=45) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise


def asset(url):
    if url in assets:
        return assets[url]
    name = re.sub(r'[^A-Za-z0-9._-]', '_', urlparse(url).path.split('/')[-1])
    path = ARCHIVE / 'files' / (hashlib.sha256(url.encode()).hexdigest()[:12] + '-' + name)
    path.parent.mkdir(exist_ok=True)
    try:
        if not path.exists():
            data = fetch(url)
            if data.lstrip().lower().startswith((b'<!doctype html', b'<html')):
                raise ValueError('Expected a file, received HTML')
            path.write_bytes(data)
        result = {'source': url, 'local': '/' + path.relative_to(ROOT).as_posix(), 'bytes': path.stat().st_size,
                  'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    except Exception as error:
        result = {'source': url, 'error': str(error)}
    assets[url] = result
    return result


def main():
    pages = []
    for year, title in PAGES.items():
        folder = ARCHIVE / str(year)
        folder.mkdir(exist_ok=True)
        api = WIKI + '/api.php?' + urlencode({'action': 'parse', 'page': title, 'format': 'json'})
        snapshot = folder / 'source.json'
        if not snapshot.exists():
            snapshot.write_bytes(fetch(api))
        parsed = json.loads(snapshot.read_text(encoding='utf-8'))['parse']
        soup = BeautifulSoup(parsed['text']['*'], 'html.parser')
        redirect = soup.select_one('.redirectText a')
        if redirect:
            target = redirect.get('title').replace(' ', '_')
            resolved = folder / 'resolved-source.json'
            if not resolved.exists():
                resolved.write_bytes(fetch(WIKI + '/api.php?' + urlencode({'action': 'parse', 'page': target, 'format': 'json'})))
            parsed = json.loads(resolved.read_text(encoding='utf-8'))['parse']
            snapshot = resolved
            soup = BeautifulSoup(parsed['text']['*'], 'html.parser')
        related = {}
        related_sources = []
        pending = [parsed]
        while pending:
            current = pending.pop()
            for link in current.get('links', []):
                linked = link['*']
                if linked == parsed['title'] or linked in related:
                    continue
                if not ((str(year) in linked and 'Israel' in linked) or linked == 'OWASP IL Sponsorship'):
                    continue
                slug = linked.replace(' ', '_')
                related[linked] = 'archive-' + slug
                subfile = folder / (slug + '.json')
                if not subfile.exists():
                    subfile.write_bytes(fetch(WIKI + '/api.php?' + urlencode({'action': 'parse', 'page': linked, 'format': 'json'})))
                subpage = json.loads(subfile.read_text(encoding='utf-8'))['parse']
                related_sources.append({'title': linked, 'revision': subpage['revid'], 'snapshot': '/' + subfile.relative_to(ROOT).as_posix()})
                section = soup.new_tag('section', id=related[linked])
                heading = soup.new_tag('h2')
                heading.string = linked
                section.append(heading)
                section.append(BeautifulSoup(subpage['text']['*'], 'html.parser'))
                soup.append(section)
                pending.append(subpage)
        for comment in soup.find_all(string=lambda value: isinstance(value, Comment)):
            comment.extract()
        for node in soup.select('script, style, iframe, object, embed, form, .mw-editsection, .printfooter, #toc'):
            node.decompose()
        # MediaWiki tabs contain substantive agendas, speaker bios and sponsors.
        # Keep every panel, removing the interactive tab markup only.
        for node in soup.find_all(True):
            for key in list(node.attrs):
                if key.startswith('on') or key in ('style', 'srcset'):
                    del node[key]
        urls = set()
        for node in soup.find_all(['a', 'img']):
            attr = 'src' if node.name == 'img' else 'href'
            value = node.get(attr, '')
            if not value or value.startswith('#'):
                continue
            url = urljoin(WIKI + '/index.php/' + title, value)
            url = re.sub(r'^https?://(https?://)', r'\1', url)
            if urlparse(url).hostname in ('owasp.org', 'www.owasp.org') and urlparse(url).path.startswith('/images/'):
                url = WIKI + urlparse(url).path
            target = unquote(urlparse(url).path.removeprefix('/index.php/')).replace('_', ' ')
            if target in related:
                node[attr] = '#' + related[target]
                continue
            node[attr] = url
            if urlparse(url).hostname == 'wiki.owasp.org' and urlparse(url).path.startswith('/images/'):
                urls.add(url)
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            list(pool.map(asset, sorted(urls)))
        for node in soup.find_all(['a', 'img']):
            attr = 'src' if node.name == 'img' else 'href'
            result = assets.get(node.get(attr))
            if result and 'local' in result:
                node[attr] = "{{ '" + result['local'] + "' | relative_url }}"
        for node in soup.select('a[href]'):
            image = node.find('img')
            link = urlparse(node['href'])
            if image and image.get('src', '').startswith('{{') and link.hostname == 'wiki.owasp.org' and link.path.startswith('/index.php/File:'):
                node['href'] = image['src']
        for heading in reversed(soup.find_all(re.compile('^h[1-5]$'))):
            heading.name = 'h' + str(min(int(heading.name[1]) + 1, 6))
        source = WIKI + '/index.php/' + title
        name = ('AppSec' if year >= 2014 else 'OWASP') + f' Israel {year}'
        content = str(soup)
        # Prevent source text from being interpreted as Liquid template code.
        content = re.sub(r'\{%.*?%\}', '', content, flags=re.S)
        content = re.sub(r'\{\{(?! \'/assets/conferences/).*?\}\}', lambda m: m[0].replace('{', '&#123;'), content, flags=re.S)
        # Render the sanitized, preserved content into linked archive pages.
        rendered_pages = _renderer.render_pages(ROOT, year, name, BeautifulSoup(content, 'html.parser'),
                                                source, parsed['revid'], snapshot, related_sources)
        pages.append({'year': year, 'source': source, 'revision': parsed['revid'], 'related': related_sources, 'rendered_pages': rendered_pages, 'page': '/' + str(year) + '/', 'files': sorted(urls)})
        print(f'{year}: {len(content)} characters, {len(urls)} files', flush=True)
    manifest = {'imported_at': datetime.now(timezone.utc).isoformat(), 'pages': pages, 'assets': sorted(assets.values(), key=lambda x: x['source'])}
    (ARCHIVE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    failures = [x for x in assets.values() if 'error' in x]
    print(f'Archived {len(pages)} pages; {len(assets) - len(failures)} files; {len(failures)} unavailable files.')


if __name__ == '__main__':
    main()
