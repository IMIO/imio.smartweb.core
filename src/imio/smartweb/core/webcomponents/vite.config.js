const path = require("path");
const { defineConfig } = require("vite");
const react = require("@vitejs/plugin-react");

// Watch .pt templates under this package and trigger a full page reload,
// mirroring webpack-dev-server's `devServer.watchFiles` behaviour. Scoped to
// this directory only (not the whole buildout, which includes node_modules,
// .venv, .git and var/ — watching those pegged the CPU).
function watchPtTemplates() {
    return {
        name: "watch-pt-templates",
        configureServer(server) {
            const watched = path.resolve(__dirname);
            server.watcher.add(`${watched}/**/*.pt`, {
                ignored: ["**/node_modules/**", "**/build/**", "**/.git/**"],
            });
            server.watcher.on("change", (file) => {
                if (file.endsWith(".pt")) {
                    server.ws.send({ type: "full-reload" });
                }
            });
        },
    };
}

module.exports = defineConfig(({ mode, command }) => ({
    plugins: [react(), watchPtTemplates()],
    // The built bundle is served from an arbitrary, deep Plone path
    // (++plone++imio.smartweb.webcomponents/js/...), not from the site
    // root. A relative base makes Vite resolve chunk/CSS URLs relative to
    // the entry script's own location instead of the origin root. Keep
    // the default "/" for the dev server so it still matches its own
    // paths (http://localhost:2000/src/index.jsx etc).
    base: command === "build" ? "./" : "/",
    // Library mode doesn't statically replace process.env.NODE_ENV like a
    // regular Vite app build does, so dependencies (e.g. react-dom) that
    // branch on it at runtime are left with a bare, undefined `process`
    // reference in the browser. Force the substitution ourselves.
    define: {
        "process.env.NODE_ENV": JSON.stringify(
            mode === "production" ? "production" : "development"
        ),
    },
    resolve: {
        alias: [
            { find: /^leaflet$/, replacement: "leaflet/dist/leaflet" },
            // moment's package.json declares a legacy "jsnext:main":
            // "./dist/moment.js", which Vite's resolver prefers over "main"
            // for bare `import moment from "moment"` (used by every
            // widget). But the locale files (node_modules/moment/locale/
            // fr.js, etc., pulled in by the side-effect imports in
            // index.jsx) reach moment's core via a plain relative
            // `require("../moment")`, which ignores package.json entirely
            // and resolves to the sibling "./moment.js" instead. Those are
            // two different files on disk, so two independent module
            // instances with two independent locale registries: fr/nl/de
            // get registered on "./moment.js", while every widget calling
            // `moment.locale(...)`/`.fromNow()` runs against "./dist/
            // moment.js", which never saw the registration — so dates
            // silently render in English regardless of the locale imports.
            // Forcing the bare specifier to the exact same file the
            // relative `require` already uses removes the ambiguity.
            {
                find: /^moment$/,
                replacement: path.resolve(__dirname, "node_modules/moment/moment.js"),
            },
        ],
    },
    build: {
        outDir: "build",
        emptyOutDir: mode === "production",
        minify: mode === "production",
        sourcemap: mode !== "production",
        chunkSizeWarningLimit: 750,
        // Library mode (build.lib) forces a single combined CSS output,
        // which would merge every widget's styles into one file loaded
        // on every page. Use a plain multi-chunk build instead so each
        // lazy-loaded widget chunk keeps its own CSS, only injected when
        // that widget actually mounts (mirrors the old webpack behaviour).
        cssCodeSplit: true,
        // Every lazy-loaded widget chunk imports shared symbols (React's
        // jsx runtime, moment, ...) back from the entry chunk via a
        // relative, Rollup-generated URL (e.g. "../smartweb-webcomponents-
        // compiled-<hash>.js"). The entry's own filename must therefore be
        // the single source of truth for that URL everywhere it's
        // referenced -- both here and in the <script> tag that loads it
        // (see viewlets/webcomponents.py, which resolves it from the
        // manifest below). Appending an ad-hoc cache-busting token to only
        // the <script> tag's URL (e.g. "?v=...") would make the browser
        // treat that as a *different* module than the one chunks import,
        // fetching and re-executing the entry's top-level code twice and
        // throwing "already defined as a custom element". Content-hashing
        // the entry filename itself keeps both references in sync AND
        // busts the cache on every content change, same as the chunks.
        manifest: true,
        rollupOptions: {
            // Named as an object so the entry chunk (and its associated
            // eager CSS asset) both get a stable, predictable `[name]`
            // ("smartweb-webcomponents-compiled") instead of the default
            // name derived from the source filename ("index").
            input: {
                "smartweb-webcomponents-compiled": path.resolve(__dirname, "./src/index.jsx"),
            },
            output: {
                format: "es",
                entryFileNames: "js/[name]-[hash].js",
                chunkFileNames: "js/chunks/[name]-[hash].js",
                assetFileNames: (assetInfo) => {
                    if (assetInfo.names?.some((name) => name.endsWith(".css"))) {
                        const base = assetInfo.names[0].replace(/\.css$/, "");
                        return base === "smartweb-webcomponents-compiled"
                            ? "css/smartweb-webcomponents-compiled.css"
                            : "css/chunks/[name]-[hash][extname]";
                    }
                    return "assets/[name]-[hash][extname]";
                },
            },
        },
    },
    server: {
        port: 2000,
        cors: true,
        proxy: {
            "^(?!/@vite|/@react-refresh|/src/|/node_modules/).*": {
                target: "http://localhost:8080",
            },
        },
    },
}));
