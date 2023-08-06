# django-tornado-websockets-client

[![Build Status](https://travis-ci.org/Kocal/django-tornado-websockets-client.svg?branch=master)](https://travis-ci.org/Kocal/django-tornado-websockets-client) 
[![Coverage Status](https://coveralls.io/repos/github/Kocal/django-tornado-websockets-client/badge.svg?branch=master)](https://coveralls.io/github/Kocal/django-tornado-websockets-client?branch=master) 
[![npm version](https://badge.fury.io/js/django-tornado-websockets-client.svg)](https://badge.fury.io/js/django-tornado-websockets-client)

JavaScript's WebSocket wrapper for [django-tornado-websockets](https://github.com/Kocal/django-tornado-websockets) project, used as a submodule.

## Usage

*In a next version of django-tornado-websockets you will be able to use
a Django tag to automatically link tornado_websocket.js on your page.*

1. Link `dist/tornado_websocket.js` file in your HTML page,
2. Or link `dist/main[.min].js` file for lodash and tornado_websockets support,

### Echo server

```js
var ws = new TornadoWebSocket('/echo', {
    // options
    host: 'my_host.fr', // 'localhost' by default
    port: 8888,         // '8000' by default
    secure: true,       // 'false' by default
});

// bind events
ws.on('open', (event) =>
    console.log('Connection: OK', event);

    ws.emit('message', { message: 'My message' });
    ws.on('message', (data) => {
        console.log(`Got message: ${data.message}`);
    });
});

ws.on('close', (event) => {
    console.log('Connection: CLOSED', event);
});

ws.on('error', (event) => {
    console.log('Connection: ERROR', event);
});
```

## Run unit tests

1. Setup your `django-tornado-websockets` WebSocket application and [run Tornado server](http://django-tornado-websockets.readthedocs.io/en/stable/usage.html#run-tornado-server),
2. `$ npm install`,
3. `$ npm test`.

## Run examples

Examples are made with ES2016, so use a modern browser please. :^)

1. `cd examples`,
2. `python -m SimpleHTTPServer 8000` or `php -S 0.0.0.0:8000`,
3. Open your browser at http://localhost:8000 and profit.

## Gulp

To compile CoffeeScript:
```bash
$ gulp scripts
```

To watch CoffeeScript file and run « scripts » task:
```bash
$ gulp
```
 
