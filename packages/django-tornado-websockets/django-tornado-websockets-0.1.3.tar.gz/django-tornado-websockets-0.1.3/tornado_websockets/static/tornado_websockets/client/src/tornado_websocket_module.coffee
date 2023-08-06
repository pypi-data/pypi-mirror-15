class TornadoWebSocketModule

    constructor: (websocket, prefix = '') ->

        if websocket not instanceof TornadoWebSocket
            throw new TypeError "Parameter `websocket` should be an instance of TornadoWebSocket,
                                 got #{typeof websocket} instead."

        @websocket = websocket
        @prefix = "" + prefix

    ###*
    # Shortcut for `TornadoWebSocket.on` method, with prefixed event support.
    #
    # @param {String} event - Event name prefixed by `TornadoWebSocketModule.prefix`.
    # @param {Function} callback - Function to execute when event `event` is received.
    # @memberof TornadoWebSocketModule
    # @see http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#TornadoWebSocket.on
    ###
    on: (event, callback) ->
        @websocket.on @prefix + event, callback

    ###*
    # Shortcut for `TornadoWebSocket.emit` method, with prefixed event support.
    #
    # @param {String} event - Event name prefixed by `TornadoWebSocketModule.prefix`.
    # @param {Object|*} data - Data to send.
    # @memberof TornadoWebSocketModule
    # @see http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#TornadoWebSocket.emit
    ###
    emit: (event, data = {}) ->
        @websocket.emit @prefix + event, data

