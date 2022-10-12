const cacheName = "v1";
const cacheAssets = [
    "/module/python/",
    "http://127.0.0.1:4444/magnan/modules/python/main.css",
    "http://127.0.0.1:4444/magnan/modules/python/main.js",
    "http://127.0.0.1:4444/magnan/js/lib/api.module.js"
];

self.addEventListener("install", e => {
    console.log("Service Worker installed");
    e.waitUntil(
        caches.open(cacheName)
            .then(cache => {
                console.log("Caching files...");
                cache.addAll(cacheAssets);
            })
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", e => {
    console.log("Service Worker activated");
    e.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== cacheName){
                        console.log("Deleting cache...");
                        return caches.delete(cache);
                    }
                })
            )
        })
    );
});

self.addEventListener("fetch", e => {
    console.log("Got fetch request");
    e.respondWith(
        fetch(e.request)
            .then(res => {
                console.log("creating a res clone...");
                const resClone = res.clone();
                caches
                    .open(cacheName)
                    .then(cache => {
                        cache.put(e.request, resClone);
                    });
                return res;
            })
            .catch(err => caches.match(e.request).then(res => res))
    );
}); 
