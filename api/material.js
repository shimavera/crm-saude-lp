// Captura de lead dos materiais ricos (lead magnets) do blog.
// Insere no Supabase do SaudeCRM via service role (chave nunca exposta ao cliente)
// e devolve a URL do material para download.

const MATERIAIS = {
  atendimento: { url: '/materiais/planilha-de-atendimento-saudecrm.xlsx', nome: 'Planilha de Atendimento' },
  metricas:    { url: '/materiais/planilha-de-metricas-saudecrm.xlsx',    nome: 'Planilha de Métricas' },
  recepcao:    { url: '/materiais/treinamento-recepcao-spin-selling-saudecrm.pdf', nome: 'Treinamento da Recepção (SPIN Selling)' },
  marketing:   { url: '/materiais/checklist-o-que-cobrar-do-marketing-saudecrm.pdf', nome: 'Checklist: O Que Cobrar do Marketing' },
};

const isEmail = (s) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  const SUPABASE_URL = process.env.SUPABASE_URL;
  const SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
  if (!SUPABASE_URL || !SERVICE_KEY) {
    return res.status(500).json({ error: 'server_misconfigured' });
  }

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  const nome = (body?.nome || '').toString().trim().slice(0, 120);
  const email = (body?.email || '').toString().trim().slice(0, 160).toLowerCase();
  const whatsapp = (body?.whatsapp || '').toString().trim().slice(0, 40);
  const material = (body?.material || '').toString().trim();

  if (!nome || nome.length < 2) return res.status(400).json({ error: 'nome_invalido' });
  if (!isEmail(email)) return res.status(400).json({ error: 'email_invalido' });
  const mat = MATERIAIS[material];
  if (!mat) return res.status(400).json({ error: 'material_invalido' });

  try {
    const r = await fetch(`${SUPABASE_URL}/rest/v1/lp_material_leads`, {
      method: 'POST',
      headers: {
        'apikey': SERVICE_KEY,
        'Authorization': `Bearer ${SERVICE_KEY}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal',
      },
      body: JSON.stringify({
        nome, email, whatsapp, material,
        origem: 'lp-blog',
        user_agent: (req.headers['user-agent'] || '').toString().slice(0, 300),
      }),
    });
    // Não bloqueia o download se o registro falhar — mas loga.
    if (!r.ok) console.error('[material] supabase insert falhou:', r.status, await r.text());
  } catch (err) {
    console.error('[material] erro ao registrar lead:', err);
  }

  // Entrega o material independentemente (UX: usuário já deixou o contato).
  return res.status(200).json({ ok: true, url: mat.url, nome: mat.nome });
}
