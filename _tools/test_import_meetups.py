import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('import_meetups', Path(__file__).with_name('import-meetups.py'))
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)


class ImportMeetupsTests(unittest.TestCase):
    def test_schemeless_web_links_are_absolute(self):
        rendered = importer.render_description('[Tickets](www.eventbrite.com/e/594694937567/)')
        self.assertIn('href="https://www.eventbrite.com/e/594694937567/"', rendered)

    def test_markdown_is_sanitized_and_liquid_is_inert(self):
        rendered = importer.render_description('**Talk** <img src="x" onerror="alert(1)"> '
                                               '[bad](javascript:alert) {{ site.title }} {% include x %}')
        self.assertIn('<strong>Talk</strong>', rendered)
        self.assertNotIn('onerror', rendered)
        self.assertNotIn('javascript:', rendered)
        self.assertNotIn('{{', rendered)
        self.assertNotIn('{%', rendered)

    def test_nulls_local_photos_repeat_import_and_removed_events(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '_tools').mkdir()
            source = root / 'source.json'
            event = {'id': '123', 'title': 'Talk', 'dateTime': '2026-06-02T17:30:00+03:00',
                     'venues': None, 'eventHosts': None, 'rsvps': None, 'topics': None,
                     'description': None, 'photoAlbum': None, 'speakerDetails': None,
                     'featuredEventPhoto': {'baseUrl': 'data:image/png;base64,aGVsbG8='}}
            source.write_text(json.dumps({'metadata': {}, 'events': [event]}))
            with patch.object(importer, 'ROOT', root):
                importer.import_archive(source)
                page = root / 'chapter/meetups/123.html'
                before = page.read_bytes()
                original_mtime = page.stat().st_mtime_ns
                importer.import_archive(source)
                self.assertEqual(before, page.read_bytes())
                self.assertEqual(original_mtime, page.stat().st_mtime_ns)
                self.assertIn(b'June 2, 2026, 17:30 UTC+3', before)
                self.assertEqual(1, len(list(root.glob('assets/img/meetups/123/*.png'))))
                manual = root / 'chapter/meetups/manual.html'
                manual.write_text('Keep this')
                source.write_text(json.dumps({'metadata': {}, 'events': []}))
                importer.import_archive(source)
                self.assertFalse(page.exists())
                self.assertTrue(manual.exists())
                self.assertFalse(list(root.glob('assets/img/meetups/123/*.png')))

    def test_duplicate_or_unsafe_ids_do_not_write_pages(self):
        for ids in [('123', '123'), ('../escape',)]:
            with self.subTest(ids=ids), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / 'source.json'
                source.write_text(json.dumps({'metadata': {}, 'events': [
                    {'id': value, 'dateTime': '2026-01-01T18:00:00+02:00'} for value in ids]}))
                with patch.object(importer, 'ROOT', root), self.assertRaises(ValueError):
                    importer.import_archive(source)
                self.assertFalse((root / 'chapter').exists())


if __name__ == '__main__':
    unittest.main()
