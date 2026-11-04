"""Render preserved wiki content as an accessible, static multipage archive."""
from html import escape
import json
import re
from urllib.parse import quote

from bs4 import BeautifulSoup


def render_pages(root, year, name, soup, source, revision, snapshot, related_sources=()):
    def slug(text):
        return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-') or 'section'

    def url(path):
        return "{{ '" + path + "' | relative_url }}"

    overview = BeautifulSoup('', 'html.parser')
    parts = [('Overview', '', overview)]
    related = list(soup.select('section[id^="archive-"]'))
    for section in related:
        section.extract()
    headings = soup.find_all(re.compile('^h[2-6]$'), recursive=False)
    split_level = min((int(h.name[1]) for h in headings), default=2)
    destination = overview
    used_slugs = set()
    provenance = {}
    source_by_title = {item['title']: item for item in related_sources}

    def add_part(title, body):
        base = slug(title)
        key = base
        suffix = 2
        while key in used_slugs:
            key = f'{base}-{suffix}'
            suffix += 1
        used_slugs.add(key)
        parts.append((title, key, body))

    for node in list(soup.contents):
        is_heading = getattr(node, 'name', None) == f'h{split_level}'
        sponsor_tier = is_heading and re.match(r'^(platinum|gold|silver|bronze)\s+sponsor', node.get_text(strip=True), re.I)
        if sponsor_tier:
            node.name = f'h{min(6, split_level + 1)}'
        elif is_heading:
            destination = BeautifulSoup('', 'html.parser')
            add_part(node.get_text(' ', strip=True), destination)
        destination.append(node.extract())
    for section in related:
        heading = section.find(re.compile('^h[2-6]$'))
        title = heading.get_text(' ', strip=True)
        original_title = title
        title = re.sub(r'^(?:AppSec|OWASP) Israel ' + str(year) + r'(?: Conference)?\s*', '', title) or title
        if any(existing[0].lower() == title.lower() for existing in parts):
            title += ' details'
        heading.name = 'h2'
        heading.string = title
        for child in section.find_all(re.compile('^h[2-6]$')):
            if child is not heading:
                child.name = 'h' + str(min(6, max(3, int(child.name[1]))))
        body = BeautifulSoup('', 'html.parser')
        body.append(section)
        if original_title in source_by_title:
            provenance[id(body)] = source_by_title[original_title]
        add_part(title, body)

    anchors = {}
    page_data = []
    for title, key, body in parts:
        path = f'/{year}/' + (key + '/' if key else '')
        ids = {tag['id'] for tag in body.select('[id]')}
        for index, heading in enumerate(body.find_all(re.compile('^h[2-6]$')), 1):
            if not heading.get('id'):
                candidate = f'heading-{index}-{slug(heading.get_text())}'
                while candidate in ids:
                    candidate += '-section'
                heading['id'] = candidate
                ids.add(candidate)
        for ident in ids:
            anchors.setdefault(ident, path)
        page_data.append((title, key, body, path, ids))

    for position, (title, key, body, path, ids) in enumerate(page_data):
        for link in body.select('a[href^="#"]'):
            ident = link['href'][1:]
            if ident not in ids and ident in anchors:
                link['href'] = url(anchors[ident]) + '#' + ident
        # Retain historical centring of logos only; prose follows the archive CSS.
        for node in body.select('[align]'):
            del node['align']
        nav = []
        for other_title, _, _, other_path, _ in page_data:
            current = ' aria-current="page"' if path == other_path else ''
            nav.append(f'<li><a href="{url(other_path)}"{current}>{escape(other_title)}</a></li>')
        toc = BeautifulSoup('<ul></ul>', 'html.parser')
        stack = [(0, toc.ul)]
        for heading in body.find_all(re.compile('^h[2-6]$')):
            level = int(heading.name[1])
            while len(stack) > 1 and level <= stack[-1][0]:
                stack.pop()
            parent = stack[-1][1]
            if parent.name == 'li':
                nested = parent.find('ul', recursive=False)
                if nested is None:
                    nested = toc.new_tag('ul')
                    parent.append(nested)
                parent = nested
            item = toc.new_tag('li')
            link = toc.new_tag('a', href='#' + heading['id'])
            link.string = heading.get_text(' ', strip=True)
            item.append(link)
            parent.append(item)
            stack.append((level, item))
        toc_html = f'<nav aria-label="On this page"><h2>On this page</h2>{toc}</nav>' if toc.select('li') else ''
        pagination = []
        for offset, label in [(-1, 'Previous'), (1, 'Next')]:
            index = position + offset
            if 0 <= index < len(page_data):
                adjacent = page_data[index]
                pagination.append(f'<a href="{url(adjacent[3])}">{label}: {escape(adjacent[0])}</a>')
        page_title = name if not key else f'{title} | {name}'
        page_source = source
        page_revision = revision
        page_snapshot = '/assets/conferences/' + str(year) + '/' + snapshot.name
        if id(body) in provenance:
            record = provenance[id(body)]
            page_source = 'https://wiki.owasp.org/index.php/' + quote(record['title'].replace(' ', '_'))
            page_revision = record['revision']
            page_snapshot = record['snapshot']
        overview_links = ''
        if not key:
            overview_links = '<h2>Explore this conference</h2><ul class="archive-page-list">' + ''.join(
                f'<li><a href="{url(item[3])}">{escape(item[0])}</a></li>'
                for item in page_data[1:]) + '</ul>'
        output = root / str(year) / (key if key else '') / 'index.html'
        output.parent.mkdir(parents=True, exist_ok=True)
        rendered = f'''---
layout: chapter
title: {json.dumps(page_title, ensure_ascii=False)}
section: conferences
conference_archive: true
permalink: {path}
---
<div class="conference-archive">
<p class="archive-breadcrumb"><a href="{url('/conferences/')}">Past conferences</a> / <a href="{url(f'/{year}/')}">{escape(name)}</a></p>
<h1>{escape(title if key else name)}</h1>
<div class="archive-layout">
<aside class="archive-sidebar"><details open><summary>Conference contents</summary>
<nav aria-label="Conference pages"><ul>{''.join(nav)}</ul></nav>{toc_html}
</details></aside>
<article class="archive-body" aria-label="{escape(title, quote=True)}">
{body}
{overview_links}
<nav class="archive-pagination" aria-label="Previous and next pages">{' '.join(pagination)}</nav>
<footer class="archive-source"><p>Preserved from the <a href="{page_source}">original OWASP wiki</a> (revision {page_revision}). <a href="{url(page_snapshot)}">Source snapshot</a>.</p>
<p>OWASP wiki contributors, <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>, unless otherwise noted. Formatting and navigation adapted for this archive. Available wiki files are stored locally; external websites and recordings depend on their original hosts.</p></footer>
</article></div></div>
'''
        output.write_text('\n'.join(line.rstrip() for line in rendered.splitlines()) + '\n', encoding='utf-8')
    expected = {root / item[3].strip('/') / 'index.html' for item in page_data}
    for old_page in (root / str(year)).rglob('index.html'):
        if old_page not in expected and 'conference_archive: true' in old_page.read_text(encoding='utf-8'):
            old_page.unlink()
    return [item[3] for item in page_data]
