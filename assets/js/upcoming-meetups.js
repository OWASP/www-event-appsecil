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
  // OWASP lists this archive pointer as a placeholder meeting.
  const archivePointerId = '07570a68-c926-4fcb-9812-9ce599643b88';

  function append(parent, tag, text) {
    const element = document.createElement(tag);
    element.textContent = text;
    parent.append(element);
    return element;
  }

  async function getJson(path) {
    const response = await fetch(origin + path, { signal: AbortSignal.timeout(8000), credentials: 'omit' });
    if (!response.ok) throw new Error('OWASP meetings request failed');
    return response.json();
  }

  async function getChapterMeetings(chapterId) {
    const pageSize = 50;
    const params = new URLSearchParams({ chapterId, limit: String(pageSize) });
    const maxPageSize = 1000;
    let limit = pageSize;
    const byId = new Map();
    while (true) {
      const { meetings } = await getJson('/api/public/meetings/list?' + params);
      if (!Array.isArray(meetings)) throw new Error('Invalid OWASP meetings response');
      for (const meeting of meetings) {
        if (meeting?.chapter_id === chapterId && uuid.test(meeting.id)) byId.set(meeting.id, meeting);
      }
      if (meetings.length < limit) return { meetings: Array.from(byId.values()), complete: true };

      // The inclusive cursor repeats meetings at the boundary. Increase the
      // limit when an entire page shares that timestamp so the cursor can advance.
      const from = meetings[meetings.length - 1]?.start_time;
      const previous = params.get('from');
      const boundary = Date.parse(from);
      if (!Number.isFinite(boundary) || (previous && boundary < Date.parse(previous))) {
        return { meetings: Array.from(byId.values()), complete: false };
      }
      if (from === previous) {
        if (limit === maxPageSize) return { meetings: Array.from(byId.values()), complete: false };
        limit = Math.min(limit * 2, maxPageSize);
      } else {
        params.set('from', from);
        limit = pageSize;
      }
      params.set('limit', String(limit));
    }
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
      details.className = 'meeting-details';
      const summary = append(details, 'summary', '');
      append(summary, 'span', 'Show meeting details').className = 'meeting-details__show';
      append(summary, 'span', 'Hide meeting details').className = 'meeting-details__hide';
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
    const day = archiveSortDate.format(start);
    const title = meeting.title.trim().toLowerCase();
    const alreadyArchived = historicalRows.some(existing => {
      const id = existing.dataset.meetupId;
      if (uuid.test(id)) return id.toLowerCase() === meeting.id.toLowerCase();
      return existing.dataset.meetupDate === day &&
        [existing.dataset.meetupTitle, existing.cells[0].textContent]
          .some(name => name?.trim().toLowerCase() === title);
    });
    if (alreadyArchived) return;

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

    const olderRow = historicalRows.find(existing => existing.dataset.meetupDate < day);
    archive.insertBefore(row, olderRow || null);
  }

  async function loadMeetings() {
    status.hidden = false;
    status.textContent = 'Loading upcoming meetings…';

    try {
      const { chapter } = await getJson('/api/public/chapters/by-slug/israel');
      if (!uuid.test(chapter?.id)) throw new Error('Missing OWASP chapter ID');

      const { meetings, complete } = await getChapterMeetings(chapter.id);
      const now = Date.now();
      const validMeetings = meetings
        .map(meeting => {
          const start = Date.parse(meeting.start_time);
          const minutes = Number(meeting.duration_minutes);
          const end = Number.isFinite(minutes) && minutes > 0 ? start + minutes * 60000 : start;
          return { meeting, start, end };
        })
        .filter(({ meeting, start }) =>
          Number.isFinite(start) &&
          meeting.id !== archivePointerId && typeof meeting.title === 'string' && meeting.title.trim()
        )
        .sort((a, b) => a.start - b.start);

      if (archive) {
        const historicalRows = Array.from(archive.rows);
        const past = validMeetings.filter(({ end }) => end < now).reverse();
        for (const { meeting, start } of past) addPastMeeting(meeting, start, historicalRows);
      }

      const upcoming = validMeetings.filter(({ end }) => end >= now);

      const cards = document.createDocumentFragment();
      for (const { meeting, start } of upcoming) addMeeting(cards, meeting, start);
      list.replaceChildren(cards);
      if (!complete) {
        status.textContent = 'Some meetings could not be loaded. Check OWASP for the full schedule.';
      } else {
        status.textContent = upcoming.length ? '' : 'No upcoming meetings are currently listed.';
        status.hidden = upcoming.length > 0;
      }
    } catch {
      status.textContent = 'Upcoming meetings could not be loaded. Check OWASP for the current schedule.';
    }
  }

  loadMeetings();
})();
