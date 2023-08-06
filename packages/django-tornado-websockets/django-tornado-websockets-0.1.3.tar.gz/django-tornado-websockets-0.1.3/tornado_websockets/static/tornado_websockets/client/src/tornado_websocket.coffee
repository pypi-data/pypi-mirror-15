class TornadoWebSocket
    ###*
    # Initialize a new WebSocket object with given options.
    # @param {String}  path            Url of a django-tornado-websockets application
    # @param {Object}  options         Object options
    # @param {String}  options.host    Host used for connection
    # @param {Number}  options.port    Port user for connection
    # @param {Boolean} options.secure  Using 'ws' or 'wss' protocol
    ###
    constructor: (path, options) ->
        if this not instanceof TornadoWebSocket
            return new TornadoWebSocket path, options

        if path is undefined
            throw new ReferenceError "You must pass 'path' parameter during 'TornadoWebSocket' instantiation."

        ###*
        # WebSocket instance
        # @type {WebSocket}
        ###
        @websocket = null

        ###*
        # Configuration values
        # @type {Object}
        # @private
        ###
        @options = Object.assign {}, {
            host: location.hostname || 'localhost',
            port: 8000,
            secure: false,
        }, options

        ###*
        # Path of a django-tornado-websockets application
        # @type {String}
        # @private
        ###
        @path = path.trim()
        @path = if @path[0] is '/' then @path else '/' + @path

        ###*
        # Generated URL by path and configuration values
        # @type {String}
        # @private
        ###
        @url = @buildUrl()

        ###*
        # Events defined by the user
        # @type {Object}
        # @private
        ###
        @events = {}

        @connect()

    ###*
    # Initialize a new WebSocket connection and bind 'open', 'close', 'error' and 'message' events.
    ###
    connect: ->
        @websocket = new WebSocket @url

        @websocket.onopen = (event) =>
            console.info 'New connection', event

        @websocket.onclose = (event) =>
            console.info 'Connection closed', event

        @websocket.onerror = (event) =>
            console.info 'Error', event

        @websocket.onmessage = (event) =>
            try
                data = JSON.parse event.data
            catch e
                console.warn "Can not parse invalid JSON: ", event.data
                return

            passed_event = data.event
            passed_data = data.data

            if passed_event is undefined or typeof passed_event isnt 'string'
                console.warn "Can not get passed event from JSON data."
                return

            if passed_data is undefined or typeof passed_data isnt 'object'
                console.warn "Can not get passed data from JSON data."
                return

            callback = @events[passed_event]

            if callback is undefined or typeof callback isnt 'function'
                console.warn "Passed event « #{passed_event} » is not binded."
                return

            callback passed_data

        return

    ###*
    # Bind a function to an event.
    # @param {String}    event     Event name
    # @param {Function}  callback  Function to execute when event `event` is sent by the server
    ###
    on: (event, callback) ->
        if typeof callback isnt 'function'
            throw new TypeError "You must pass a function for 'callback' parameter."

        if event in ['open', 'close', 'error']
            @websocket['on' + event] = callback
        else
            @events[event] = callback

        return

    ###*
    # Emit a couple event/data to WebSocket server.
    # If value of data parameter is not an object, it is put into a `{message: data}` object.
    # @param {String}    event  Event name
    # @param {Object|*}  data   Data to send
    ###
    emit: (event, data = {}) ->
        if typeof data isnt 'object'
            data =
                message: data

        data = JSON.stringify
            event: event,
            data: data

        @websocket.send data

    ###*
    # Return an URL built from `this.options`.
    # Path is auto-prefixed by "/ws".
    # @returns {String}
    ###
    buildUrl: ->
        protocol = if @options.secure then 'wss' else 'ws'

        return "#{protocol}://#{@options.host}:#{@options.port}/ws#{@path}"
