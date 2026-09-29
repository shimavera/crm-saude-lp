// O único valor público é gerado no build a partir de PUBLIC_CLARITY_ID.
(() => {
  const siteWindow = /** @type {Window & { SAUDECRM_CONFIG?: { clarityId?: string }, clarity?: ((...args: unknown[]) => void) & { q?: unknown[][] } }} */ (window);
  const id = siteWindow.SAUDECRM_CONFIG?.clarityId;
  if (!id || !/^[a-z0-9]{5,30}$/i.test(id) || siteWindow.clarity) return;
  /** @param {...unknown} args */
  function enqueue(...args) { queue.q.push(args); }
  const queue = Object.assign(enqueue, { q: /** @type {unknown[][]} */ ([]) });
  siteWindow.clarity = queue;
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.clarity.ms/tag/${id}`;
  document.head.appendChild(script);
})();
