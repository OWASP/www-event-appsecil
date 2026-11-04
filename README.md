# AppSec Israel

Jekyll website for the AppSec Israel conference and OWASP Israel chapter.
Live at https://appsecil.org/.

## Contributing

Contributions are welcome through pull requests. See the
[Jekyll documentation](https://jekyllrb.com/docs/home/) for help working with the site.

## Local preview

With Ruby 4 installed on Windows, run from the repository root:

```powershell
.\preview.bat
```

The launcher installs missing dependencies and starts the site at
`http://127.0.0.1:4000/`. It rebuilds when files change; refresh the browser to
see updates. Press Ctrl+C to stop.

```powershell
.\preview.bat -Build       # Build without starting the server
.\preview.bat -Port 4001   # Use another port
```

The Windows preview uses `_tools/Gemfile.preview` for Ruby 4 compatibility.
The production build uses `Gemfile`.

To check a build hosted under a project path:

```sh
bundle exec jekyll build --baseurl /www-event-appsecil
```

## Maintaining the site

- `_config.yml`: current conference year and Jekyll settings.
- `_data/year-2027/config.yml`: current conference dates and venue.
- `2027/index.md`: current conference overview; other pages are in `2027/`.
- `_data/site-menu.yml`: shared navigation.
- `chapter/`: chapter information and resources.
- `conferences/`: conference history; past conference pages live in year folders.

## Importing chapter meetups

Export events using the sibling `meetup-archiver` project. Its JSON format is
documented in `../meetup-archiver/ARCHIVE_FORMAT.md`.

Install dependencies once:

```powershell
python -m pip install --target .bundle/meetup-import -r _tools/meetup-requirements.txt
```

Import the latest timestamped JSON export from the sibling project's `output`
folder, or provide an explicit path:

```powershell
python _tools/import-meetups.py
python _tools/import-meetups.py ../meetup-archiver/output/your-archive.json
```

A new import **replaces the imported event set**, so use a complete export to
retain all events. Edit the importer/templates rather than generated event pages.

Commit the generated files together:

- `chapter/meetups/`
- `_data/meetups.json`
- `assets/img/meetups/`
- `_tools/meetup-import-manifest.json`

Historical labels, recording links, and attendance notes are maintained in
`_data/meetup-notes.json`.

Validate importer changes and preview the archive:

```powershell
python -m unittest discover -s _tools -p test_import_meetups.py
.\preview.bat
```

Open `http://127.0.0.1:4000/chapter/meetups/` to review the result.
