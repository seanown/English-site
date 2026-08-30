// Netlify Function: archive ownsean.com form submissions into a Notion database.
// Triggered by a Netlify Forms "Form submission notification" webhook (POST).
//
// Required env var (set in Netlify dashboard):
//   NOTION_TOKEN  = Notion internal integration secret (starts with ntn_)
//
// The target database ID is hardcoded below:
//   ownsean.com — Form Leads  (c6db53ab-2199-459f-bdcb-016c42b25198)
//
// No front-end JS is involved — this runs server-side on Netlify.

const DATABASE_ID = 'c6db53ab-2199-459f-bdcb-016c42b25198';

function rich(value) {
  const text = (value == null ? '' : String(value)).slice(0, 1900);
  return { rich_text: [{ text: { content: text } }] };
}

function title(value) {
  const text = (value == null ? '' : String(value)).slice(0, 200);
  return { title: [{ text: { content: text || 'Anonymous' } }] };
}

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const token = process.env.NOTION_TOKEN;
  if (!token) {
    return { statusCode: 500, body: 'Missing NOTION_TOKEN env var' };
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (e) {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  // Netlify form webhook shape: top-level form_name + data{ field: value }
  const data = body.data || (body.payload && body.payload.data) || {};
  const formName = body.form_name || (body.payload && body.payload.formName) || 'unknown';

  // Honeypot spam check (bot-field is the hidden field on all 3 forms)
  if (data['bot-field']) {
    return { statusCode: 200, body: 'ok (spam filtered)' };
  }

  const email = (data.email || '').toString().trim();
  const name = (data.name || email || 'Anonymous').toString().trim();

  const properties = {
    Name: title(name),
    'Form Type': { select: { name: formName } },
    Organization: rich(data.organization),
    Subject: rich(data.subject),
    Message: rich(data.message),
    'Event Details': rich(data.event_details),
    'Source Page': rich(
      formName === 'speaking' ? 'speaking.html'
      : formName === 'contact' ? 'contact.html'
      : 'index.html#subscribe'
    )
  };
  if (email) properties.Email = { email };

  try {
    const res = await fetch('https://api.notion.com/v1/pages', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + token,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        parent: { database_id: DATABASE_ID },
        properties: properties
      })
    });
    if (!res.ok) {
      const detail = await res.text();
      return { statusCode: 502, body: 'Notion API error ' + res.status + ': ' + detail };
    }
    return { statusCode: 200, body: 'archived' };
  } catch (e) {
    return { statusCode: 500, body: 'Fetch failed: ' + e.message };
  }
};
