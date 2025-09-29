// --- CSRF helper -------------------------------------------------------------
function getCsrfTokenSync() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta && meta.content) return meta.content;
  try {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "@@authenticator", false);
    xhr.send(null);
    const m = /value="([^"]+)"/.exec(xhr.responseText);
    return m ? m[1] : "";
  } catch (e) { return ""; }
}

// --- HTTP helper -------------------------------------------------------------
async function postProcess(url, payload) {
  const token = getCsrfTokenSync();
  const resp = await fetch(url, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRF-TOKEN": token
    },
    credentials: "same-origin",
    body: JSON.stringify(payload)
  });
  if (!resp.ok) {
    const txt = await resp.text().catch(() => "");
    throw new Error("HTTP " + resp.status + " – " + txt);
  }
  const ct = resp.headers.get("Content-Type") || "";
  return ct.includes("application/json") ? resp.json() : { html: await resp.text() };
}

// --- UI helpers (spinner + disable button) -----------------------------------
function startProcessingUI(editor, btnApi) {
  if (btnApi) btnApi.setEnabled(false);
  editor.setProgressState?.(true); // spinner intégré TinyMCE
}
function stopProcessingUI(editor, btnApi) {
  editor.setProgressState?.(false);
  if (btnApi) btnApi.setEnabled(true);
}
async function withProcessingUI(editor, btnApi, fn) {
  try {
    startProcessingUI(editor, btnApi);
    await fn();
    stopProcessingUI(editor, btnApi);
    editor.notificationManager.open({ text: "Terminé", type: "success", timeout: 1800 });
  } catch (e) {
    console.error("[tinymce-process] error:", e);
    stopProcessingUI(editor, btnApi);
    editor.notificationManager.open({ text: "Échec du traitement", type: "error", timeout: 2500 });
  }
}

// --- Plugins -----------------------------------------------------------------
(function () {
  if (!window.tinymce) return;

  // ===== Plugin 1 : text_expand =====
  tinymce.PluginManager.add("text_expand", function (editor) {
    let btnApi = null;

    editor.addCommand("textExpandRun", async function () {
      await withProcessingUI(editor, btnApi, async () => {
        const html = editor.getContent({ format: "html" });
        const data = await postProcess("@@process-textexpand", { html });
        if (!data || typeof data.html !== "string") throw new Error("Réponse invalide");
        editor.undoManager.transact(() => editor.setContent(data.html));
      });
    });

    editor.ui.registry.addButton("text_expand", {
      text: "Text expand",
      tooltip: "Process text expand",
      onAction: () => editor.execCommand("textExpandRun"),
      onSetup: (api) => { btnApi = api; return () => (btnApi = null); }
    });
  });

  // ===== Plugin 2 : suggest_titles =====
  tinymce.PluginManager.add("suggest_titles", function (editor) {
    let btnApi = null;

    editor.addCommand("suggestTitlesRun", async function () {
      await withProcessingUI(editor, btnApi, async () => {
        const html = editor.getContent({ format: "html" });
        const data = await postProcess("@@process-suggesttitles", { html });
        if (!data || typeof data.html !== "string") throw new Error("Réponse invalide");
        editor.undoManager.transact(() => editor.setContent(data.html));
      });
    });

    editor.ui.registry.addButton("suggest_titles", {
      text: "Suggest titles",
      tooltip: "Proposer des titres",
      onAction: () => editor.execCommand("suggestTitlesRun"),
      onSetup: (api) => { btnApi = api; return () => (btnApi = null); }
    });
  });

  // Menu bouton "IA" dans la toolbar façon Antoine B.
  tinymce.PluginManager.add("ia", function (editor) {
    editor.ui.registry.addMenuButton("ia", {
      text: "IA",
      tooltip: "Outils IA",
      fetch: (callback) => {
        callback([
          {
            type: "menuitem",
            text: "Text expand",
            onAction: () => editor.execCommand("textExpandRun"),
          },
          {
            type: "menuitem",
            text: "Suggest titles",
            onAction: () => editor.execCommand("suggestTitlesRun"),
          },
        ]);
      },
    });
  });

  // Menu bouton "IA" dans la toolbar façon Seb
  tinymce.PluginManager.add("ia_menuitems", function (editor) {
    editor.ui.registry.addMenuItem("ia_text_expand", {
      text: "Text expand",
      onAction: () => editor.execCommand("textExpandRun"),
    });
    editor.ui.registry.addMenuItem("ia_suggest_titles", {
      text: "Suggest titles",
      onAction: () => editor.execCommand("suggestTitlesRun"),
    });
  });


})();
