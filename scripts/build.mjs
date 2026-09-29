import { access, cp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';

const clarityId = process.env.PUBLIC_CLARITY_ID?.trim() || '';
if (clarityId && !/^[a-z0-9]{5,30}$/i.test(clarityId)) {
  throw new Error('PUBLIC_CLARITY_ID inválido.');
}
await mkdir('assets', { recursive: true });
await writeFile('assets/site-config.js', `window.SAUDECRM_CONFIG = Object.freeze(${JSON.stringify({ clarityId })});\n`);
const html = await readFile('index.html', 'utf8');
for (const match of html.matchAll(/(?:src|href)="(\/assets\/[^"?#]+)(?:[?#][^"]*)?"/g)) {
  await access(`.${match[1]}`);
}
// Publicar somente arquivos de conteúdo; fontes server-side, testes e docs ficam fora.
await rm('dist', { recursive: true, force: true });
await mkdir('dist');
const directories = new Set(['assets', 'blog', 'fonts', 'materiais']);
for (const entry of await readdir('.', { withFileTypes: true })) {
  if ((entry.isDirectory() && directories.has(entry.name)) ||
      (entry.isFile() && /\.(html|txt|xml|webp|png|jpe?g|svg|ico|mp4)$/.test(entry.name))) {
    await cp(entry.name, `dist/${entry.name}`, { recursive: true });
  }
}
console.log(`Configuração pública gerada. Clarity ${clarityId ? 'configurado' : 'não configurado'}.`);
