(() => {
  'use strict';

  let activeContainer = null;
  let activeSourceSelector = null;

  // ---------- Utils ---------------------------------------------------------

  function getRichTextHtml() {
    try {
      if (window.tinymce) {
        const ed =
          tinymce.get('form-widgets-IRichTextBehavior-text') ||
          (tinymce.editors && tinymce.editors.find(e => e?.id?.includes('IRichTextBehavior'))) ||
          tinymce.activeEditor;
        const html = ed?.getContent?.();
        if (html) return html;
      }
    } catch {}
    const ta =
      document.querySelector('#form-widgets-IRichTextBehavior-text') ||
      document.querySelector('textarea[name="form.widgets.IRichTextBehavior.text"]');
    return ta?.value || '';
  }

  function normalizeTitles(data) {
    if (typeof data === 'string') {
      try { data = JSON.parse(data); } catch { return [data.trim()].filter(Boolean); }
    }
    if (Array.isArray(data)) {
      return Array.from(new Set(data.map(t => String(t).trim()).filter(Boolean)));
    }
    if (data && typeof data === 'object') {
      let arr = [];
      if (Array.isArray(data.suggested_titles)) {
        arr = data.suggested_titles;
      } else if (Array.isArray(data.titles)) {
        arr = data.titles;
      } else {
        const firstArray = Object.values(data).find(v => Array.isArray(v));
        if (firstArray) arr = firstArray;
      }
      return Array.from(new Set(arr.map(t => String(t).trim()).filter(Boolean)));
    }
    return [];
  }

  function buildListHTML(titles) {
    if (!titles.length) return '<p>No suggestion.</p>';

    const ul = document.createElement('ul');
    ul.className = 'list-group ia-suggest-ul';
    ul.setAttribute('role', 'listbox');
    ul.setAttribute('aria-label', 'Title suggestions');

    for (const t of titles) {
      const li = document.createElement('li');
      li.className = 'list-group-item list-group-item-action ia-suggest-item';
      li.setAttribute('role', 'option');
      li.setAttribute('tabindex', '0');
      li.setAttribute('data-title', t);
      li.textContent = t;
      ul.appendChild(li);
    }

    const wrap = document.createElement('div');
    wrap.appendChild(ul);
    return wrap.innerHTML;
  }

  function mirrorIntoOpenModal(listHTML, tries = 24) {
    const lists = document.querySelectorAll(
      '.modal.show .ia-suggest-list, .plone-modal .ia-suggest-list, .plone-modal-container .ia-suggest-list'
    );
    if (lists.length) {
      lists.forEach(el => (el.innerHTML = listHTML));
      return;
    }
    if (tries > 0) requestAnimationFrame(() => mirrorIntoOpenModal(listHTML, tries - 1));
  }

  async function fetchSuggestions(slugUrl, textHtml) {
    const headers = { Accept: 'application/json' };
    const token = document.querySelector('input[name="_authenticator"]')?.value || '';
    const body = new URLSearchParams({ text: textHtml });

    try {
      const res = await fetch(slugUrl, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          ...headers,
          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
          ...(token ? { 'X-CSRF-TOKEN': token } : {}),
        },
        body: body.toString(),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      const url = slugUrl + (slugUrl.includes('?') ? '&' : '?') + 'text=' + encodeURIComponent(textHtml);
      const res = await fetch(url, { credentials: 'same-origin', headers });
      if (!res.ok) throw e;
      return await res.json();
    }
  }

  // ---------- Fermeture locale ciblant .modal et .modal-wrapper --------------

  function isVisible(el) {
    if (!el) return false;
    const rects = el.getClientRects?.();
    return (el.offsetParent !== null) || (rects && rects.length > 0);
  }

  function closeModal(fromEl) {
    // Modale et wrapper les plus proches de l'élément qui a été cliqué
    const modal =
      fromEl?.closest('.modal') ||
      document.querySelector('.modal.show') ||
      document.querySelector('.modal');

    if (!modal) return;
    const wrapper = modal.closest('.modal-wrapper');

    // 1) Fermer via les contrôles internes
    let closer =
      modal.querySelector('.modal-close, .plone-modal-close') ||
      modal.querySelector('[data-bs-dismiss="modal"], [data-dismiss="modal"]');

    if (closer) closer.click();

    // 2) API Bootstrap si dispo
    try {
      if (window.bootstrap?.Modal) {
        const inst = window.bootstrap.Modal.getInstance(modal) || new window.bootstrap.Modal(modal);
        inst.hide();
      }
    } catch {}

    // 3) Coup d'ESC pour aider certains thèmes
    setTimeout(() => {
      if (modal.classList.contains('show') || isVisible(modal)) {
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
      }
    }, 50);

    // 4) Si encore visible → masquer juste cette modale + retirer son wrapper
    setTimeout(() => {
      if (modal.classList.contains('show') || isVisible(modal)) {
        modal.classList.remove('show');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
      }
      if (wrapper && wrapper.parentNode) {
        wrapper.remove(); // <- ton cas : .modal-wrapper restait en place
      }
      // Nettoyage léger (local)
      const parent = (wrapper && wrapper.parentNode) || document.body;
      parent.querySelectorAll('.modal-backdrop, .plone-modal-backdrop, .plone-modal-overlay, .backdrop, .backdrop-active')
        .forEach(n => n.remove());
      document.body.classList.remove('modal-open');
      document.body.style.removeProperty('padding-right');
      document.querySelectorAll('[inert]').forEach(n => n.removeAttribute('inert'));
    }, 150);
  }

  function fillInputAndClose(title, fromEl) {
    const selector = activeSourceSelector || activeContainer?.dataset.sourceSelector || '#form-widgets-title';
    const input = document.querySelector(selector) || activeContainer?.querySelector('input[type="text"]');
    if (input) {
      input.value = title;
      input.dispatchEvent(new Event('input',  { bubbles: true }));
      input.dispatchEvent(new Event('change', { bubbles: true }));
      input.focus();
    }
    closeModal(fromEl || document.body);
  }

  // ---------- 1) Trigger: mémoriser + fetch + afficher ----------------------

  document.addEventListener('click', (ev) => {
    const trigger = ev.target.closest('a.suggestedtitles-generate-button.pat-plone-modal');
    if (!trigger) return;

    activeContainer = trigger.closest('.suggestedtitles-with-button') || null;
    activeSourceSelector = activeContainer?.dataset.sourceSelector || '#form-widgets-title';

    const slugUrl = activeContainer?.dataset.slugUrl;
    if (!slugUrl) return;

    const targetSel    = trigger.getAttribute('href'); // "#ia-suggest-modal"
    const templateRoot = targetSel ? document.querySelector(targetSel) : null;
    const templateList = templateRoot ? templateRoot.querySelector('.ia-suggest-list') : null;

    if (templateList) templateList.textContent = 'Loading…';

    const textHtml = getRichTextHtml();

    fetchSuggestions(slugUrl, textHtml)
      .then((data) => {
        const titles   = normalizeTitles(data);
        const listHTML = buildListHTML(titles);
        if (templateList) templateList.innerHTML = listHTML;
        mirrorIntoOpenModal(listHTML);
      })
      .catch((err) => {
        // (${String(err)})
        const errorHTML = `<div class="alert alert-warning">Not possible to get suggestions.</div>`;
        if (templateList) templateList.innerHTML = errorHTML;
        mirrorIntoOpenModal(errorHTML);
      });
  }, true); // capture pour précéder l'ouverture pat-plone-modal

  // ---------- 2) Sélection d’un titre (clic/pointer + clavier) --------------

  function handlePickEvent(ev) {
    const item = ev.target.closest('.ia-suggest-item');
    if (!item) return;
    if (ev.type === 'click' || ev.type === 'pointerup') ev.stopPropagation();
    const title = item.getAttribute('data-title') || item.textContent.trim();
    if (!title) return;
    fillInputAndClose(title, item);
  }
  document.addEventListener('click', handlePickEvent, true);
  document.addEventListener('pointerup', handlePickEvent, true);

  function handleKey(ev) {
    if (ev.key !== 'Enter' && ev.key !== ' ') return;
    const item = ev.target.closest('.ia-suggest-item');
    if (!item) return;
    ev.preventDefault();
    ev.stopPropagation();
    const title = item.getAttribute('data-title') || item.textContent.trim();
    if (!title) return;
    fillInputAndClose(title, item);
  }
  document.addEventListener('keydown', handleKey, true);

  // ---------- 3) Nettoyage à la fermeture (si event dispo) ------------------

  document.addEventListener('hidden.bs.modal', () => {
    activeContainer = null;
    activeSourceSelector = null;
  }, true);

})();
