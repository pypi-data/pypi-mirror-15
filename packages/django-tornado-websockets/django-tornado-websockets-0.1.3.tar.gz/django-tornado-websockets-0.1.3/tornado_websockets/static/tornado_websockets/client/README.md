# django-tornado-websockets-client

[![Build Status](https://travis-ci.org/Kocal/dtws-client.svg?branch=master)](https://travis-ci.org/Kocal/dtws-client)
[![Coverage Status](https://coveralls.io/repos/github/Kocal/dtws-client/badge.svg?branch=master)](https://coveralls.io/github/Kocal/dtws-client?branch=master)
[![npm version](https://badge.fury.io/js/django-tornado-websockets-client.svg)](https://badge.fury.io/js/django-tornado-websockets-client)

JavaScript's WebSocket wrapper for [django-tornado-websockets](https://github.com/Kocal/django-tornado-websockets) project, used as a submodule.

## Documentation

- Stable: http://django-tornado-websockets.readthedocs.io/en/stable/usage.html#using-websockets-client-side
- Latest: http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#using-websockets-client-side
- Develop: http://django-tornado-websockets.readthedocs.io/en/develop/usage.html#using-websockets-client-side

## Running unit tests

1. Setup your `django-tornado-websockets` WebSocket application and [run Tornado server](http://django-tornado-websockets.readthedocs.io/en/stable/usage.html#run-tornado-server),
2. `$ npm install`,
3. `$ npm test`.

## Running examples

Examples are made with ES2016, so use a modern browser please. :^)

1. `cd examples`,
2. `python -m SimpleHTTPServer 8000` or `php -S 0.0.0.0:8000`,
3. Open your browser at http://localhost:8000 and profit.

## Misc

### Gulp

To compile CoffeeScript:
```bash
$ gulp scripts
```

To watch CoffeeScript file and run « scripts » task:
```bash
$ gulp
```
 
