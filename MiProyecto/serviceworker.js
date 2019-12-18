var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
    '/',
    '/static/css/estilos.css',
    '/static/img/logo.png',
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
      fetch(event.request)
      .then((result)=>{
        return caches.open(CACHE_NAME)
        .then(function(c) {
          c.put(event.request.url, result.clone())
          return result;
        })
        
      })
      .catch(function(e){
          return caches.match(event.request)
      })

    );
});

//notificaciones push
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');

var firebaseConfig = {
  apiKey: "AIzaSyDuhvbpwKLxoDNp2C6L4XtSDrYeRSLZp-I",
  authDomain: "floreria-3fb5a.firebaseapp.com",
  databaseURL: "https://floreria-3fb5a.firebaseio.com",
  projectId: "floreria-3fb5a",
  storageBucket: "floreria-3fb5a.appspot.com",
  messagingSenderId: "265018175270",
  appId: "1:265018175270:web:cea75b2355dfaa0a48dbe7"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function(payload){

  let title = payload.notification.title;
  let options = {
      body:payload.notification.body,
      icon:payload.notification.icon
  }

  self.registration.showNotification(title, options);

});
