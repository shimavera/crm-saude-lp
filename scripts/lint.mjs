import { readFile, readdir } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';

for (const directory of ['api', 'assets', 'scripts', 'tests']) {
  for (const name of await readdir(directory)) {
    if (!/\.(m?js)$/.test(name)) continue;
    const file = `${directory}/${name}`;
    const check = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
    if (check.status !== 0) throw new Error(`JavaScript inválido: ${file}\n${check.stderr}`);
  }
}
const html = await readFile('index.html', 'utf8');
if (/mode\s*:\s*['"]no-cors['"]/.test(html)) throw new Error('Formulário não pode assumir sucesso com resposta opaca.');
if (/https:\/\/script\.google\.com\/macros\//.test(html)) throw new Error('Webhook deve permanecer no servidor.');
if (/x70tisywby/.test(html)) throw new Error('Clarity deve vir da configuração de build.');
console.log('Sintaxe JavaScript e limites do formulário verificados.');
