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
        alias: [{ find: /^leaflet$/, replacement: "leaflet/dist/leaflet" }],
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
                entryFileNames: "js/[name].js",
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
