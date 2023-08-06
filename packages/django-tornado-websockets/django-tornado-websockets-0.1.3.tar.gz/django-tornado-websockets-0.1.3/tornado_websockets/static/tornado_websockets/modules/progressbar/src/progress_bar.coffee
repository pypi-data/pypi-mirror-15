class ProgressBarModule extends TornadoWebSocketModule

    ###*
    # Initialize a new ProgressBarModule object with given parameters.
    #
    # @constructs
    # @param {TornadoWebSocket} websocket - A TornadoWebSocket instance.
    # @param {ProgressBarModuleEngine} engine - An instance that implement ProgressBarModuleEngineInterface.
    # @param {string} prefix - String that will prefix events name for TornadoWebSocket's on/emit methods.
    # @example
    # var websocket = new TornadoWebSocket('/my_progressbar');
    # var $container = document.querySelector('#container');
    # var engine = new ProgressBarModuleEngineBootstrap($container, {
    #     progressbar: {
    #         animated: true,
    #         striped: true,
    #     }
    # });
    #
    # var progress = new ProgressBarModule(websocket, engine, 'my_prefix');
    #
    # websocket.on('open', function() {
    #
    #     // emit 'event'
    #     websocket.emit('event ...');
    #
    #     // emit 'my_prefix_event'
    #     progress.emit('event ...');
    #
    #     progress.on('before_init', function() {
    #         // Is called before progress bar initialization
    #     });
    #
    #     progress.on('after_init', function() {
    #         // Is called after progress bar initialization
    #     });
    #
    #     progress.on('before_update', function() {
    #         // Is called before progress bar updating
    #     });
    #
    #     progress.on('after_update', function() {
    #         // Is called after progress bar updating
    #     });
    #
    #     progress.on('done', function() {
    #         // Is called when progression is done
    #     });
    # });
    #
    ###
    constructor: (websocket, engine, prefix = 'module_progressbar_') ->
        if this not instanceof ProgressBarModule
            return new ProgressBarModule websocket, engine

        if websocket not instanceof TornadoWebSocket
            throw new TypeError "Parameter `websocket` should be an instance of TornadoWebSocket,
                                 got #{typeof websocket} instead."

        if engine not instanceof ProgressBarModuleEngine
            throw new TypeError "Parameter `engine` should be an instance of ProgressBarModuleEngine,
                                got #{typeof engine} instead."

        super websocket, prefix

        ###*
        # @prop {ProgressBarModuleEngine} engine - Progress bar engine implementing this interface.
        # @public
        ###
        @engine = engine

        @init()

        return

    ###*
    # Is automatically called at the end of the current object instantiation. Binds `init` and `update` events and
    # render the progress bar from defined engine.
    #
    # @memberof ProgressBarModule
    ###
    init: ->
        @on 'init', (data) =>
            @engine.onInit.apply @engine, [data]

        @on 'update', (data) =>
            @engine.onUpdate.apply @engine, [data]

        @engine.render()
        return
