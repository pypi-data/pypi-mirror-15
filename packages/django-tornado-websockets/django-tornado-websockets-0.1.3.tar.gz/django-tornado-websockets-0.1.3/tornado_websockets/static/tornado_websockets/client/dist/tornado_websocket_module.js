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