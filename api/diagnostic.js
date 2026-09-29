/** @typedef {{ method?: string, headers: Record<string, string | string[] | undefined>, body?: unknown }} Request */
/** @typedef {{ setHeader: (key: string, value: string) => void, status: (code: number) => Response, json: (data: object) => unknown }} Response */

const VOLUMES = ['Até 20 por dia', 'De 20 a 50 por dia', 'De 50 a 150 por dia', 'Mais de 150 por dia'];
const TEAMS = ['A recepção', 'O próprio profissional', 'Mais de uma pessoa', 'Cada pessoa responde quando consegue', 'Já usamos alguma automação'];
const PAINS = ['Demoramos para responder', 'O paciente para de responder', 'A equipe esquece os follow-ups', 'Temos conversas espalhadas', 'Não sabemos quais contatos estão mais quentes'];
const MAX_BODY_BYTES = 16384;
const DELIVERY_TIMEOUT_MS = 30000;

/** @param {unknown} value @param {number} max */
function field(value, max) {
  return typeof value === 'string' && value.length <= max ? value.trim() : '';
}

/** O destino é uma planilha; prefixo de texto evita fórmulas em campos livres.
 * @param {string} value */
function sheetText(value) {
  return /^[=+@-]/.test(value) ? `'${value}` : value;
}

/** @param {unknown} raw */
export function validateLead(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return { error: 'invalid_payload' };
  const input = /** @type {Record<string, unknown>} */ (raw);
  if (input.company_website) return { error: 'invalid_payload' };
  const name = field(input.name, 120);
  const email = field(input.email, 254).toLowerCase();
  const whatsapp = field(input.whatsapp, 40);
  const phoneDigits = whatsapp.replace(/\D/g, '');
  if (name.length < 2 || /[\r\n<>]/.test(name) || /^[=+@-]/.test(name)) return { error: 'invalid_name' };
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || /^[=+@-]/.test(email)) return { error: 'invalid_email' };
  if (!/^[\d\s()+.-]+$/.test(whatsapp) || !/^(?:55)?[1-9]\d\d{8,9}$/.test(phoneDigits)) return { error: 'invalid_whatsapp' };
  const volume = field(input.volume, 100), team = field(input.team, 100), pain = field(input.pain, 150);
  if (!VOLUMES.includes(volume) || !TEAMS.includes(team) || !PAINS.includes(pain)) return { error: 'invalid_answers' };
  if (input.consent !== true) return { error: 'consent_required' };
  let landingPage = '';
  try {
    const url = new URL(field(input.landingPage, 2000));
    if (['https:', 'http:'].includes(url.protocol)) landingPage = `${url.origin}${url.pathname}`;
  } catch { /* URL é opcional; parâmetros de campanha seguem campos próprios. */ }
  /** @type {Record<string, string | boolean>} */
  const payload = { name, email, whatsapp: sheetText(whatsapp), volume, team, pain, consent: true, sentAt: new Date().toISOString(), landingPage };
  for (const key of ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid']) {
    payload[key] = sheetText(field(input[key], 500));
  }
  return { payload };
}

/** @param {Request} req @param {Response} res */
export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, error: 'method_not_allowed' });
  }
  const origin = req.headers.origin;
  if (typeof origin === 'string') {
    try {
      if (new URL(origin).host !== req.headers.host) return res.status(403).json({ ok: false, error: 'invalid_origin' });
    } catch { return res.status(403).json({ ok: false, error: 'invalid_origin' }); }
  }
  if (!String(req.headers['content-type'] || '').toLowerCase().startsWith('application/json')) {
    return res.status(415).json({ ok: false, error: 'unsupported_media_type' });
  }
  let body = req.body;
  try {
    const serialized = typeof body === 'string' ? body : JSON.stringify(body);
    if (!serialized || Buffer.byteLength(serialized) > MAX_BODY_BYTES) return res.status(413).json({ ok: false, error: 'payload_too_large' });
    if (typeof body === 'string') body = JSON.parse(body);
  } catch { return res.status(400).json({ ok: false, error: 'invalid_payload' }); }
  const result = validateLead(body);
  if (result.error) return res.status(400).json({ ok: false, error: result.error });
  const webhook = process.env.LEAD_WEBHOOK_URL;
  try {
    const url = new URL(webhook || '');
    if (url.protocol !== 'https:' || url.hostname !== 'script.google.com' || !/^\/macros\/s\/[^/]+\/exec$/.test(url.pathname)) throw new Error('Invalid endpoint');
  } catch { return res.status(503).json({ ok: false, error: 'service_unavailable' }); }
  const startedAt = Date.now();
  let failureReason = 'upstream_network';
  let upstreamStatus = 0;
  try {
    const response = await fetch(/** @type {string} */ (webhook), {
      method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify(result.payload), signal: AbortSignal.timeout(DELIVERY_TIMEOUT_MS), redirect: 'follow',
    });
    upstreamStatus = response.status;
    failureReason = 'upstream_http';
    if (!response.ok) throw new Error('Upstream failed');
    failureReason = 'upstream_json';
    const acknowledgment = await response.json();
    failureReason = 'upstream_ack';
    if (!acknowledgment || acknowledgment.ok !== true) throw new Error('Missing acknowledgment');
    return res.status(200).json({ ok: true });
  } catch (error) {
    const timedOut = error instanceof Error && ['TimeoutError', 'AbortError'].includes(error.name);
    // Somente metadados operacionais; nunca endpoint, resposta ou dados pessoais.
    console.warn('[diagnostic] delivery_unconfirmed', {
      reason: timedOut ? 'upstream_timeout' : failureReason,
      duration_ms: Date.now() - startedAt,
      upstream_status: upstreamStatus,
    });
    return res.status(502).json({ ok: false, error: 'delivery_unconfirmed' });
  }
}
