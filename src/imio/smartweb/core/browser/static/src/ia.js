// smartweb-slugify.js — aucun import, aucun bundler requis
function injectSuggestStyles() {
  if (document.getElementById("sw-suggest-styles")) return;
  const style = document.createElement("style");
  style.id = "sw-suggest-styles";
  style.textContent = `
  .sw-overlay{position:fixed;inset:0;background:rgba(0,0,0,.2);z-index:9999}
  .sw-panel{position:fixed;max-width:480px;min-width:280px;max-height:60vh;overflow:auto;
    background:#fff;border-radius:10px;box-shadow:0 12px 30px rgba(0,0,0,.25);padding:12px}
  .sw-panel h3{margin:0 0 .5rem 0;font-size:1rem}
  .sw-list{display:flex;flex-direction:column;gap:.5rem}
  .sw-suggest-btn{display:block;width:100%;text-align:left;padding:.5rem .75rem;border-radius:8px;
    border:1px solid #e5e7eb;background:#f9fafb;cursor:pointer;font:inherit}
  .sw-suggest-btn:hover,.sw-suggest-btn:focus{background:#eef2ff;outline:none}
  .sw-actions{display:flex;justify-content:flex-end;margin-top:.75rem}
  .sw-cancel{border:1px solid #e5e7eb;background:#fff;border-radius:8px;padding:.4rem .7rem;cursor:pointer}
  `;
  document.head.appendChild(style);
}

// -- Modale d’affichage des titres
function showSuggestionsModal(titles, { anchorEl, onPick }) {
  injectSuggestStyles();

  // Overlay + panneau
  const overlay = document.createElement("div");
  overlay.className = "sw-overlay";
  overlay.setAttribute("role", "presentation");

  const panel = document.createElement("div");
  panel.className = "sw-panel";
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-modal", "true");
  panel.innerHTML = `
    <h3>Suggestions de titres</h3>
    <div class="sw-list"></div>
    <div class="sw-actions">
      <button type="button" class="sw-cancel">Annuler</button>
    </div>
  `;

  // Liste de boutons (un clic = onPick)
  const list = panel.querySelector(".sw-list");
  titles.forEach((t, i) => {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "sw-suggest-btn";
    b.textContent = t;
    b.addEventListener("click", () => {
      if (typeof onPick === "function") onPick(t);
      close();
    });
    list.appendChild(b);
  });

  // Fermetures
  const previouslyFocused = document.activeElement;
  function close() {
    document.removeEventListener("keydown", onKey);
    overlay.remove();
    if (previouslyFocused && typeof previouslyFocused.focus === "function") previouslyFocused.focus();
  }
  function onKey(e) {
    if (e.key === "Escape") close();
  }
  document.addEventListener("keydown", onKey);
  overlay.addEventListener("click", (e) => { if (e.target === overlay) close(); });
  panel.querySelector(".sw-cancel").addEventListener("click", close);

  overlay.appendChild(panel);
  document.body.appendChild(overlay);

  // Positionner près du bouton "Generate"
  const rect = anchorEl.getBoundingClientRect();
  // D’abord placer hors écran pour mesurer
  panel.style.left = "-9999px";
  panel.style.top = "-9999px";
  // Une fois dans le DOM, on peut mesurer
  requestAnimationFrame(() => {
    const pw = Math.min(480, Math.max(280, Math.floor(window.innerWidth * 0.9)));
    panel.style.maxWidth = pw + "px";

    const ph = Math.min(parseInt(getComputedStyle(panel).maxHeight, 10) || 400, panel.offsetHeight || 400);
    let left = rect.left;
    let top = rect.bottom + 8;

    if (left + pw > window.innerWidth - 8) left = window.innerWidth - pw - 8;
    // Si ça déborde en bas, on l’affiche au-dessus du bouton
    if (top + ph > window.innerHeight - 8) top = rect.top - ph - 8;
    if (top < 8) top = 8;
    if (left < 8) left = 8;

    panel.style.left = left + "px";
    panel.style.top = top + "px";

    // Focus sur le 1er bouton
    const firstBtn = panel.querySelector(".sw-suggest-btn");
    if (firstBtn && typeof firstBtn.focus === "function") firstBtn.focus();
  });
}



document.addEventListener("click", async (ev) => {
  const btn = ev.target.closest(".slug-generate-button");
  if (!btn) return;
  ev.preventDefault();

  const wrap = btn.closest(".slugify-with-button, .pat-slugify-with-button");
  if (!wrap) return;

  const input = wrap.querySelector("input[type='text'], textarea");
  if (!input) return;


  // Où injecter le résultat (par défaut: input du wrapper)
  const targetSel = wrap.dataset.targetSelector || "";
  const targetInput = targetSel ? document.querySelector(targetSel) : input;

  // Options passées via data-attributes sur le wrapper
  const url = wrap.dataset.slugUrl || "";                 // ex: data-slug-url=".../@@slugify"
  const text = tinymce.get('form-widgets-IRichTextBehavior-text').getContent();
  
  // Jeton CSRF (plone.protect)
  const token = wrap.closest("form")
    ?.querySelector('input[name="_authenticator"]')?.value || "";

  try {
    btn.disabled = true;
    const resp = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json",
        "X-CSRF-TOKEN": token
      },
      body: new URLSearchParams({ text }),
      credentials: "same-origin",
    });

    if (!resp.ok) {
      const msg = await resp.text();
      throw new Error(`HTTP ${resp.status} – ${msg}`);
    }

    const data = await resp.json();     // attend {"value": "..."}
    console.log(data);
    if (Array.isArray(data.suggested_titles) && data.suggested_titles.length) {
      showSuggestionsModal(data.suggested_titles, {
        anchorEl: btn,
        onPick: (title) => {
          targetInput.value = title;
          targetInput.dispatchEvent(new Event("input",  { bubbles: true }));
          targetInput.dispatchEvent(new Event("change", { bubbles: true }));
        }
      });
      return; // on sort ici (pas de data.value attendu dans ce cas)
    }
  } catch (e) {
    console.error("Slugify error:", e);
    alert("Erreur lors de la génération du slug.");
  } finally {
    btn.disabled = false;
  }
});
