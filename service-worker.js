const CACHE_NAME = "overforsel-cache-v1";
const urlsToCache = [
    "/",
    "/static/style.css",
    "/static/manifest.json",
    "/static/icon-192.png",
    "/static/icon-512.png",
    "/service-worker.js" // Sørger for at cache service worker korrekt
];

// 📌 Installer Service Worker og cache nødvendige filer
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

// 📌 Aktiver ny Service Worker og slet gammel cache
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log("Sletter gammel cache:", cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

// 📌 Intercept fetch requests for at levere cachet indhold offline
self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request).catch(() => {
                console.error("Netværksfejl, og ingen cache fundet:", event.request.url);
                return new Response("Du er offline, og denne ressource er ikke cachet.", {
                    status: 503,
                    statusText: "Service Unavailable"
                });
            });
        })
    );
});
