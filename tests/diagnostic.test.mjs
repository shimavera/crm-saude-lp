import test from 'node:test';
import assert from 'node:assert/strict';
import handler, { validateLead } from '../api/diagnostic.js';

const lead = {
  name: 'Teste Automatizado', email: 'qa@example.com', whatsapp: '(11) 99999-0000',
  volume: 'Até 20 por dia', team: 'A recepção', pain: 'Demoramos para responder', consent: true,
  landingPage: 'https://saudecrm.com/?utm_source=teste&private=remove', utm_source: 'teste', gclid: 'test-click', fbclid: 'meta-click',
};

async function invoke(body = lead, overrides = {}) {
  const output = { status: 0, headers: {}, data: undefined };
  const res = {
    setHeader(key, value) { output.headers[key] = value; },
    status(code) { output.status = code; return res; },
    json(data) { output.data = data; return output; },
  };
  await handler({ method: 'POST', headers: { host: 'saudecrm.com', origin: 'https://saudecrm.com', 'content-type': 'application/json' }, body, ...overrides }, res);
  return output;
}

test('normaliza campos e preserva atribuição sem repassar parâmetros arbitrários da URL', () => {
  const result = validateLead({ ...lead, name: '  Teste QA  ', email: 'QA@EXAMPLE.COM', arbitrary: 'drop' });
  assert.equal(result.payload.name, 'Teste QA');
  assert.equal(result.payload.email, 'qa@example.com');
  assert.equal(result.payload.landingPage, 'https://saudecrm.com/');
  assert.equal(result.payload.gclid, 'test-click');
  assert.equal(result.payload.fbclid, 'meta-click');
  assert.equal(result.payload.arbitrary, undefined);
});

test('rejeita consentimento falso/string, telefone incompleto, injeções, enums e honeypot', () => {
  for (const invalid of [
    { consent: false }, { consent: 'true' }, { name: '<script>' }, { whatsapp: '123' },
    { email: 'invalid' }, { team: 'invented' }, { company_website: 'spam' }, { name: 'a'.repeat(121) },
  ]) assert.ok(validateLead({ ...lead, ...invalid }).error);
});

test('impede fórmulas em campos de planilha e mantém telefone internacional como texto', () => {
  assert.equal(validateLead({ ...lead, name: '=IMPORTXML("x")' }).error, 'invalid_name');
  assert.equal(validateLead({ ...lead, email: '=test@example.com' }).error, 'invalid_email');
  const { payload } = validateLead({ ...lead, name: 'João Clínica', whatsapp: '+55 11 99999-0000', utm_source: '  =IMPORTXML("x")', utm_medium: '@SUM(A1)' });
  assert.equal(payload.name, 'João Clínica');
  assert.equal(payload.whatsapp, "'+55 11 99999-0000");
  assert.equal(payload.utm_source, '\'=IMPORTXML("x")');
  assert.equal(payload.utm_medium, "'@SUM(A1)");
});

test('valida método, origem, content type e tamanho antes de encaminhar', async () => {
  assert.equal((await invoke(lead, { method: 'GET' })).status, 405);
  assert.equal((await invoke(lead, { headers: { origin: 'https://other.example', host: 'saudecrm.com' } })).status, 403);
  assert.equal((await invoke(lead, { headers: { 'content-type': 'text/plain' } })).status, 415);
  assert.equal((await invoke('x'.repeat(16385))).status, 413);
  assert.equal((await invoke('{invalid')).status, 400);
  assert.equal((await invoke({ ...lead, consent: false })).status, 400);
});

test('sem configuração válida, retorna indisponível e nunca faz envio', async (t) => {
  const old = process.env.LEAD_WEBHOOK_URL;
  t.after(() => { if (old === undefined) delete process.env.LEAD_WEBHOOK_URL; else process.env.LEAD_WEBHOOK_URL = old; });
  let calls = 0;
  t.mock.method(globalThis, 'fetch', async () => { calls++; });
  for (const value of ['', 'https://attacker.example/endpoint']) {
    process.env.LEAD_WEBHOOK_URL = value;
    assert.equal((await invoke()).status, 503);
  }
  assert.equal(calls, 0);
});

test('confirma somente JSON ok:true; falhas e respostas ambíguas não produzem sucesso', async (t) => {
  const old = process.env.LEAD_WEBHOOK_URL;
  process.env.LEAD_WEBHOOK_URL = 'https://script.google.com/macros/s/test-only/exec';
  t.after(() => { if (old === undefined) delete process.env.LEAD_WEBHOOK_URL; else process.env.LEAD_WEBHOOK_URL = old; });
  let reply = { ok: true, json: async () => ({ ok: true, private: 'never echo' }) };
  let forwarded;
  t.mock.method(globalThis, 'fetch', async (_url, options) => { forwarded = JSON.parse(options.body); return reply; });
  assert.deepEqual((await invoke()).data, { ok: true });
  assert.equal(forwarded.consent, true);
  assert.equal(forwarded.company_website, undefined);
  for (const failed of [
    { ok: false, json: async () => ({ ok: true }) },
    { ok: true, json: async () => ({ ok: false }) },
    { ok: true, json: async () => ({ status: 'success' }) },
    { ok: true, json: async () => { throw new SyntaxError('HTML'); } },
  ]) {
    reply = failed;
    const response = await invoke();
    assert.equal(response.status, 502);
    assert.deepEqual(response.data, { ok: false, error: 'delivery_unconfirmed' });
  }
});
