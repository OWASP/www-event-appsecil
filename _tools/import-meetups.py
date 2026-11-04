"""Import a meetup-archiver JSON export into native Jekyll pages.

Usage: python _tools/import-meetups.py [archive.json]
Dependencies: python -m pip install -r _tools/meetup-requirements.txt
"""

import argparse
import base64
import hashlib
import html
import json
from datetime import datetime
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.bundle/meetup-import'))
import bleach
import markdown

TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    'p', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre',
    'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'del',
}
EXTENSIONS = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif',
              'image/webp': '.webp', 'image/avif': '.avif'}


def escaped(value):
    return html.escape(str(value or ''), quote=True)


def readable_datetime_range(start_value, end_value=None):
    start = datetime.fromisoformat(start_value.replace('Z', '+00:00'))
    end = datetime.fromisoformat(end_value.replace('Z', '+00:00')) if end_value else None

    def date_label(moment):
        return f'{moment.strftime("%B")} {moment.day}, {moment.year}'

    def zone_label(moment):
        offset = moment.utcoffset()
        if offset is None:
            return ''
        minutes = int(offset.total_seconds() / 60)
        sign = '+' if minutes >= 0 else '-'
        hours, remainder = divmod(abs(minutes), 60)
        return f' UTC{sign}{hours}' + (f':{remainder:02}' if remainder else '')

    label = f'{date_label(start)}, {start:%H:%M}'
    if end:
        if start.date() == end.date() and start.utcoffset() == end.utcoffset():
            label += f'–{end:%H:%M}'
        else:
            return label + zone_label(start) + f' – {date_label(end)}, {end:%H:%M}' + zone_label(end)
    return label + zone_label(start)


def connection(value):
    return [edge['node'] for edge in (value or {}).get('edges') or []
            if isinstance(edge, dict) and isinstance(edge.get('node'), dict)]


def local_url(path):
    return "{{ '" + path + "' | relative_url }}"


def render_description(text):
    # Sanitize after rendering Markdown. Escape Liquid delimiters so archived
    # text cannot execute Jekyll templates when the generated page is built.
    rendered = markdown.markdown(text or '', extensions=['extra', 'nl2br', 'sane_lists'])
    rendered = re.sub(r'(href=[\"\'])www\.', r'\1https://www.', rendered, flags=re.I)
    clean = bleach.clean(rendered, tags=TAGS,
                         attributes={'a': ['href', 'title'], 'img': ['src', 'alt', 'title'],
                                     'th': ['align'], 'td': ['align']},
                         protocols=['https', 'http', 'mailto'], strip=True)
    return clean.replace('{', '&#123;').replace('}', '&#125;')


def image(photo, event_id, files, warnings):
    source = (photo or {}).get('baseUrl') or ''
    if not source:
        return None
    if not source.startswith('data:'):
        warnings.append(f'{event_id}: image was not embedded in archive; omitted')
        return None
    header, encoded = source.split(',', 1)
    mime = header[5:].split(';')[0].lower()
    if mime not in EXTENSIONS or not header.endswith(';base64'):
        raise ValueError(f'{event_id}: unsupported embedded image type {mime}')
    content = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(content).hexdigest()[:20]
    path = f'assets/img/meetups/{event_id}/{digest}{EXTENSIONS[mime]}'
    files[path] = content
    return '/' + path


def import_archive(source):
    archive = json.loads(source.read_text(encoding='utf-8-sig'))
    if not isinstance(archive.get('metadata'), dict) or not isinstance(archive.get('events'), list):
        raise ValueError('Expected metadata object and events array')
    files, events, warnings, seen = {}, [], [], set()
    for event in archive['events']:
        event_id = str(event['id'])
        if not re.fullmatch(r'[A-Za-z0-9_-]+', event_id) or event_id in seen:
            raise ValueError(f'Unsafe or duplicate event ID: {event_id}')
        seen.add(event_id)
        title = event.get('title') or 'Chapter meetup'
        venues = event.get('venues') or ([event['venue']] if event.get('venue') else [])
        venue_text = '; '.join(', '.join(str(v[k]) for k in ['name', 'address', 'city', 'country']
                                         if v.get(k)) for v in venues if isinstance(v, dict))
        url = f'/chapter/meetups/{event_id}/'
        featured = image(event.get('featuredEventPhoto'), event_id, files, warnings)
        photos = [p for p in (image(photo, event_id, files, warnings)
                             for photo in connection((event.get('photoAlbum') or {}).get('photos'))) if p]
        parts = [f'<p><strong>Date:</strong> <time datetime="{escaped(event["dateTime"])}">{escaped(readable_datetime_range(event["dateTime"], event.get("endTime")))}</time></p>']
        if venue_text:
            parts.append(f'<p><strong>Location:</strong> {escaped(venue_text)}</p>')
        elif event.get('isOnline') or event.get('eventType') == 'ONLINE':
            parts.append('<p>Online event</p>')
        attendance = (event.get('rsvps') or {}).get('totalCount', event.get('going'))
        if attendance is not None:
            parts.append(f'<p><strong>RSVPs:</strong> {escaped(attendance)}</p>')
        if featured:
            src = local_url(featured)
            parts.append(f'<a class="meetup-photo-link meetup-featured-link" href="{src}"><img class="meetup-featured" src="{src}" alt="{escaped(title)}" loading="lazy"></a>')
        parts.append('<div class="meetup-description">' + render_description(event.get('description')) + '</div>')
        speaker = event.get('speakerDetails') or {}
        if speaker.get('name'):
            parts.append('<h2>Speaker</h2><h3>' + escaped(speaker['name']) + '</h3>' + render_description(speaker.get('description')))
        topics = ', '.join(t.get('name') or '' for t in connection(event.get('topics')))
        if topics:
            parts.append(f'<p><strong>Topics:</strong> {escaped(topics)}</p>')
        if photos:
            parts.append('<h2>Photos</h2><div class="meetup-gallery">')
            for i, photo in enumerate(dict.fromkeys(photos), 1):
                src = local_url(photo)
                parts.append(f'<a class="meetup-photo-link" href="{src}"><img src="{src}" alt="{escaped(title)} — photo {i}" loading="lazy"></a>')
            parts.append('</div>')
        # Keep the source as an optional historical link, never as navigation
        # required to read the event. Do not publish attendee names/member IDs.
        original = event.get('eventUrl') or ''
        if urlsplit(original).scheme in ('https', 'http'):
            parts.append(f'<p><a href="{escaped(original)}">Original event listing</a></p>')
        if event.get('howToFindUs'):
            parts.append('<h2>Directions</h2>' + render_description(event['howToFindUs']))
        front = {'layout': 'chapter', 'section': 'chapter', 'title': title, 'permalink': url}
        # A JSON object is valid YAML and safely quotes arbitrary source text.
        page = '---\n' + json.dumps(front, ensure_ascii=False) + '\n---\n' + '\n'.join(parts) + '\n'
        # Neutralize Liquid in source-derived titles/attributes too, retaining
        # only our generated relative_url expressions in the body.
        page = page.replace('{{', '&#123;&#123;').replace('{%', '&#123;%')
        page = re.sub(r'&#123;&#123; (\'[^\']+\' \| relative_url) }}', r'{{ \1 }}', page)
        files[f'chapter/meetups/{event_id}.html'] = page.encode('utf-8')
        events.append({'id': event_id, 'title': title, 'date': event['dateTime'],
                       'url': url, 'location': venue_text, 'attendance': attendance})
    events.sort(key=lambda e: (datetime.fromisoformat(e['date'].replace('Z', '+00:00')).timestamp(), e['id']), reverse=True)
    files['_data/meetups.json'] = (json.dumps({'metadata': archive['metadata'], 'events': events}, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    # Fully validate before writing. The manifest owns only generated files;
    # removing events from a later export also removes their generated assets.
    manifest = ROOT / '_tools/meetup-import-manifest.json'
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    for name, content in files.items():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != content:
            target.write_bytes(content)
    for name in set(previous) - files.keys():
        target = (ROOT / name).resolve()
        if (target.is_relative_to(ROOT / 'chapter/meetups') or
                target.is_relative_to(ROOT / 'assets/img/meetups')) and target.is_file():
            target.unlink()
    manifest.write_text(json.dumps(sorted(files), indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(events)} events and {sum(n.startswith("assets/") for n in files)} local images from {source.name}.')
    for warning in warnings:
        print('Warning:', warning)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', nargs='?', type=Path)
    args = parser.parse_args()
    source = args.archive
    if source is None:
        candidates = list((ROOT.parent / 'meetup-archiver/output').glob('*.json'))
        if not candidates:
            parser.error('No archive found; supply the archive JSON path')
        source = max(candidates, key=lambda p: p.name)
    import_archive(source.resolve())
