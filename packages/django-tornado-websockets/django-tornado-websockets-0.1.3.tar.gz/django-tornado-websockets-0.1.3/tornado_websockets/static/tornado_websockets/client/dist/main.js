/**
 * https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Objets_globaux/Object/assign
 */
if (typeof Object.assign != 'function') {
    (function() {
        Object.assign = function(target) {
            'use strict';
            if (target === undefined || target === null) {
                throw new TypeError('Cannot convert undefined or null to object');
            }

            var output = Object(target);
            for (var index = 1; index < arguments.length; index++) {
                var source = arguments[index];
                if (source !== undefined && source !== null) {
                    for (var nextKey in source) {
                        if (Object.prototype.hasOwnProperty.call(source, nextKey)) {
                            output[nextKey] = source[nextKey];
                        }
                    }
                }
            }
            return output;
        };
    })();
}
var TornadoWebSocket;

TornadoWebSocket = (function() {

    /**
     * Initialize a new WebSocket object with given options.
     * @param {String}  path            Url of a django-tornado-websockets application
     * @param {Object}  options         Object options
     * @param {String}  options.host    Host used for connection
     * @param {Number}  options.port    Port user for connection
     * @param {Boolean} options.secure  Using 'ws' or 'wss' protocol
     */
    function TornadoWebSocket(path, options) {
        if (!(this instanceof TornadoWebSocket)) {
            return new TornadoWebSocket(path, options);
        }
        if (path === void 0) {
            throw new ReferenceError("You must pass 'path' parameter during 'TornadoWebSocket' instantiation.");
        }

        /**
         * WebSocket instance
         * @type {WebSocket}
         */
        this.websocket = null;

        /**
         * Configuration values
         * @type {Object}
         * @private
         */
        this.options = Object.assign({}, {
            host: location.hostname || 'localhost',
            port: 8000,
            secure: false
        }, options);

        /**
         * Path of a django-tornado-websockets application
         * @type {String}
         * @private
         */
        this.path = path.trim();
        this.path = this.path[0] === '/' ? this.path : '/' + this.path;

        /**
         * Generated URL by path and configuration values
         * @type {String}
         * @private
         */
        this.url = this.buildUrl();

        /**
         * Events defined by the user
         * @type {Object}
         * @private
         */
        this.events = {};
        this.connect();
    }


    /**
     * Initialize a new WebSocket connection and bind 'open', 'close', 'error' and 'message' events.
     */

    TornadoWebSocket.prototype.connect = function() {
        this.websocket = new WebSocket(this.url);
        this.websocket.onopen = (function(_this) {
            return function(event) {
                return console.info('New connection', event);
            };
        })(this);
        this.websocket.onclose = (function(_this) {
            return function(event) {
                return console.info('Connection closed', event);
            };
        })(this);
        this.websocket.onerror = (function(_this) {
            return function(event) {
                return console.info('Error', event);
            };
        })(this);
        this.websocket.onmessage = (function(_this) {
            return function(event) {
                var callback, data, e, error, passed_data, passed_event;
                try {
                    data = JSON.parse(event.data);
                } catch (error) {
                    e = error;
                    console.warn("Can not parse invalid JSON: ", event.data);
                    return;
                }
                passed_event = data.event;
                passed_data = data.data;
                if (passed_event === void 0 || typeof passed_event !== 'string') {
                    console.warn("Can not get passed event from JSON data.");
                    return;
                }
                if (passed_data === void 0 || typeof passed_data !== 'object') {
                    console.warn("Can not get passed data from JSON data.");
                    return;
                }
                callback = _this.events[passed_event];
                if (callback === void 0 || typeof callback !== 'function') {
                    console.warn("Passed event « " + passed_event + " » is not binded.");
                    return;
                }
                return callback(passed_data);
            };
        })(this);
    };


    /**
     * Bind a function to an event.
     * @param {String}    event     Event name
     * @param {Function}  callback  Function to execute when event `event` is sent by the server
     */

    TornadoWebSocket.prototype.on = function(event, callback) {
        if (typeof callback !== 'function') {
            throw new TypeError("You must pass a function for 'callback' parameter.");
        }
        if (event === 'open' || event === 'close' || event === 'error') {
            this.websocket['on' + event] = callback;
        } else {
            this.events[event] = callback;
        }
    };


    /**
     * Emit a couple event/data to WebSocket server.
     * If value of data parameter is not an object, it is put into a `{message: data}` object.
     * @param {String}    event  Event name
     * @param {Object|*}  data   Data to send
     */

    TornadoWebSocket.prototype.emit = function(event, data) {
        if (data == null) {
            data = {};
        }
        if (typeof data !== 'object') {
            data = {
                message: data
            };
        }
        data = JSON.stringify({
            event: event,
            data: data
        });
        return this.websocket.send(data);
    };


    /**
     * Return an URL built from `this.options`.
     * Path is auto-prefixed by "/ws".
     * @returns {String}
     */

    TornadoWebSocket.prototype.buildUrl = function() {
        var protocol;
        protocol = this.options.secure ? 'wss' : 'ws';
        return protocol + "://" + this.options.host + ":" + this.options.port + "/ws" + this.path;
    };

    return TornadoWebSocket;

})();
var TornadoWebSocketModule;

TornadoWebSocketModule = (function() {
    function TornadoWebSocketModule(websocket, prefix) {
        if (prefix == null) {
            prefix = '';
        }
        if (!(websocket instanceof TornadoWebSocket)) {
            throw new TypeError("Parameter `websocket` should be an instance of TornadoWebSocket, got " + (typeof websocket) + " instead.");
        }
        this.websocket = websocket;
        this.prefix = "" + prefix;
    }


    /**
     * Shortcut for `TornadoWebSocket.on` method, with prefixed event support.
     *
     * @param {String} event - Event name prefixed by `TornadoWebSocketModule.prefix`.
     * @param {Function} callback - Function to execute when event `event` is received.
     * @memberof TornadoWebSocketModule
     * @see http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#TornadoWebSocket.on
     */

    TornadoWebSocketModule.prototype.on = function(event, callback) {
        return this.websocket.on(this.prefix + event, callback);
    };


    /**
     * Shortcut for `TornadoWebSocket.emit` method, with prefixed event support.
     *
     * @param {String} event - Event name prefixed by `TornadoWebSocketModule.prefix`.
     * @param {Object|*} data - Data to send.
     * @memberof TornadoWebSocketModule
     * @see http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#TornadoWebSocket.emit
     */

    TornadoWebSocketModule.prototype.emit = function(event, data) {
        if (data == null) {
            data = {};
        }
        return this.websocket.emit(this.prefix + event, data);
    };

    return TornadoWebSocketModule;

})();