import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, access } from 'node:fs/promises';
import { createHash } from 'node:crypto';

test('arquivo preserva bytes das dependências capturadas da produção', async () => {
  const manifest = JSON.parse(await readFile('docs/lp-v1-preservation.json', 'utf8'));
  for (const asset of manifest.preserved_assets) {
    const bytes = await readFile(`lp-v1${asset.path}`);
    assert.equal(bytes.length, asset.bytes, asset.path);
    assert.equal(createHash('sha256').update(bytes).digest('hex'), asset.sha256, asset.path);
  }
});

test('LP anterior mantém recursos isolados, SEO de arquivo e envio confirmado sem webhook exposto', async () => {
  const html = await readFile('lp-v1/index.html', 'utf8');
  assert.match(html, /name="robots" content="noindex, follow"/);
  assert.match(html, /rel="canonical" href="https:\/\/saudecrm\.com\/lp-v1\/"/);
  assert.match(html, /action="\/api\/diagnostic" method="post"/);
  assert.match(html, /!response\.ok \|\| acknowledgment\.ok !== true/);
  assert.doesNotMatch(html, /https:\/\/script\.google\.com\/macros\//);
  assert.doesNotMatch(html, /mode:\s*['"]no-cors['"]/);
  const refs = [...html.matchAll(/(?:src|href|poster)=["'](\/lp-v1\/[^"']+)["']/g)].map(match => match[1]);
  for (const path of refs) {
    // A configuração pública é gerada no build, não armazenada no código-fonte.
    if (path.endsWith('/assets/site-config.js')) continue;
    await access(path.slice(1));
  }
});
