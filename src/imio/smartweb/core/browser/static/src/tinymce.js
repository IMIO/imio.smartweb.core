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

(function () {
  if (!window.tinymce) return;

  async function postProcess(url, html) {
    const token = getCsrfTokenSync();
    const resp = await fetch(url, {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=utf-8",
        "X-CSRF-TOKEN": token
      },
      body: JSON.stringify({ html })
    });
    if (!resp.ok) throw new Error("HTTP " + resp.status);
    return resp.json();
  }

  tinymce.PluginManager.add("process", function (editor) {
    editor.addCommand("processRun", async function () {
      const html = editor.getContent({ format: "html" });
      try {
        // URL relative au contexte courant (le document en édition)
        const data = await postProcess("@@process-text", html);
        if (data && typeof data.html === "string") {
          editor.setContent(data.html);
          editor.notificationManager.open({ text: "Texte traité", type: "success", timeout: 2000 });
        } else {
          throw new Error("Réponse invalide");
        }
      } catch (e) {
        console.error(e);
        editor.notificationManager.open({ text: "Échec du traitement", type: "error", timeout: 3000 });
      }
    });

    editor.ui.registry.addButton("process", {
      text: "Process",
      tooltip: "Process text",
      onAction: () => editor.execCommand("processRun"),
    });
  });
})();