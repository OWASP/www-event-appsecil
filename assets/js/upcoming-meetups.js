(() => {
  const section = document.querySelector('[data-upcoming-meetups]');
  if (!section) return;

  const status = section.querySelector('[data-meetup-status]');
  const list = section.querySelector('[data-meetup-list]');
  const archive = document.querySelector('[data-meetup-archive]');
  const origin = 'https://owasp.org';
  const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  const dateFormat = new Intl.DateTimeFormat('en-GB', {
    dateStyle: 'full',
    timeStyle: 'short',
    timeZone: 'Asia/Jerusalem',
  });

  const archiveDate = new Intl.DateTimeFormat('en-GB', {
    dateStyle: 'long',
    timeZone: 'Asia/Jerusalem',
  });
  const archiveSortDate = new Intl.DateTimeFormat('sv-SE', {
    dateStyle: 'short',
    timeZone: 'Asia/Jerusalem',
  });
  // Temporary simulation for the fork’s GitHub Pages archive preview.
  const simulateAfterMeetup = archive &&
    window.location.origin === 'https://tghosth.github.io' &&
    /^\/www-event-appsecil\/chapter\/meetups\/?$/.test(window.location.pathname) &&
    new URLSearchParams(window.location.search).get('preview') !== 'live';
  const simulatedTime = Date.parse('2026-12-14T15:31:00Z');
  if (simulateAfterMeetup) {
    const notice = document.createElement('p');
    notice.textContent = 'Simulation · 14 December 2026, 17:31 Israel time';
    section.prepend(notice);
  }

  // OWASP lists this archive pointer as a placeholder meeting.
  const archivePointerId = '07570a68-c926-4fcb-9812-9ce599643b88';

  function append(parent, tag, text) {
    const element = document.createElement(tag);
    element.textContent = text;
    parent.append(element);
    return element;
  }

  async function getJson(path, signal) {
    const response = await fetch(origin + path, { signal, credentials: 'omit' });
    if (!response.ok) throw new Error('OWASP meetings request failed');
    return response.json();
  }

  function addMeeting(parent, meeting, start) {
    const card = document.createElement('article');
    append(card, 'h3', meeting.title);
    const metadata = document.createElement('p');
    const time = append(metadata, 'time', dateFormat.format(start) + ' (Israel time)');
    time.dateTime = new Date(start).toISOString();
    card.append(metadata);
    if (meeting.location) append(card, 'p', meeting.location);

    if (typeof meeting.description === 'string' && meeting.description.trim()) {
      const details = document.createElement('details');
      append(details, 'summary', 'Meeting details');
      const template = document.createElement('template');
      template.innerHTML = meeting.description;
      // Render description text only. Never attach markup supplied by the API.
      for (const node of template.content.childNodes) {
        if (node.nodeType !== Node.TEXT_NODE && !node.matches?.('p,h1,h2,h3,h4,h5,h6,ul,ol,div,blockquote')) continue;
        const text = node.textContent.trim();
        if (text) append(details, 'p', text);
      }
      if (details.childElementCount > 1) card.append(details);
    }

    const action = document.createElement('p');
    const label = meeting.rsvp_enabled || meeting.registration_url
      ? 'Details and RSVP on OWASP'
      : 'View meeting on OWASP';
    const link = append(action, 'a', label);
    link.href = origin + '/meetings/' + meeting.id;
    card.append(action);
    parent.append(card);
  }

  function addPastMeeting(meeting, start, historicalRows) {
    const row = document.createElement('tr');
    const name = append(row, 'td', '');
    const link = append(name, 'a', meeting.title);
    link.href = origin + '/meetings/' + meeting.id;
    const date = append(row, 'td', '');
    const time = append(date, 'time', archiveDate.format(start));
    time.dateTime = new Date(start).toISOString();
    append(row, 'td', meeting.location || '');
    append(row, 'td', '');
    append(row, 'td', '');

    const day = archiveSortDate.format(start);
    const olderRow = historicalRows.find(existing => existing.dataset.meetupDate < day);
    archive.insertBefore(row, olderRow || null);
  }

  async function loadMeetings() {
    status.hidden = false;
    status.textContent = 'Loading upcoming meetings…';

    try {
      const signal = AbortSignal.timeout(8000);
      const { chapter } = await getJson('/api/public/chapters/by-slug/israel', signal);
      if (!uuid.test(chapter?.id)) throw new Error('Missing OWASP chapter ID');

      const params = new URLSearchParams({ chapterId: chapter.id, limit: '200' });
      const { meetings } = await getJson('/api/public/meetings/list?' + params, signal);
      if (!Array.isArray(meetings)) throw new Error('Invalid OWASP meetings response');

      const now = simulateAfterMeetup ? simulatedTime : Date.now();
      const validMeetings = meetings
        .map(meeting => ({ meeting, start: Date.parse(meeting?.start_time) }))
        .filter(({ meeting, start }) =>
          Number.isFinite(start) && meeting.chapter_id === chapter.id && uuid.test(meeting.id) &&
          meeting.id !== archivePointerId && typeof meeting.title === 'string' && meeting.title.trim()
        )
        .sort((a, b) => a.start - b.start);

      if (archive) {
        const historicalRows = Array.from(archive.rows);
        const past = validMeetings.filter(({ start }) => start < now).reverse();
        for (const { meeting, start } of past) addPastMeeting(meeting, start, historicalRows);
      }

      const upcoming = validMeetings.filter(({ start }) => start >= now);

      const cards = document.createDocumentFragment();
      for (const { meeting, start } of upcoming) addMeeting(cards, meeting, start);
      list.replaceChildren(cards);
      status.textContent = upcoming.length ? '' : 'No upcoming meetings are currently listed.';
      status.hidden = upcoming.length > 0;
    } catch {
      status.textContent = 'Upcoming meetings could not be loaded. Check OWASP for the current schedule.';
    }
  }

  loadMeetings();
})();
