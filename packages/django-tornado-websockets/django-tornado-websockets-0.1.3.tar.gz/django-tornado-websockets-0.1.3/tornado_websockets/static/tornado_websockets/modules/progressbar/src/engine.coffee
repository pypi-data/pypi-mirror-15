class ProgressBarModuleEngine

    ###*
    # Defaults options for an engine.
    # @memberof ProgressBarModuleEngine
    # @param {Object} - Defaults options.
    ###
    @::defaults = {}

    ###*
    # Interface for classes that represent a {@link ProgressBarModule#engine}.
    # @interface
    # @constructs
    # @param {HTMLElement} $container - HTML container for the progress bar.
    # @param {Object} options - Options from ProgressBarModule.
    ###
    constructor: ($container, options) ->
        if $container is undefined or $container not instanceof HTMLElement
            throw new TypeError "Parameter `$container` should be an instance of HTMLElement,
                                 got #{typeof $container} instead."

        if options not instanceof Object
            throw new TypeError "Parameter `options` should be an Object, got #{typeof options} instead."

        @$container = $container
        @options = deepmerge @defaults, options

    ###*
    # Make and display an HTML render to the user.
    # @memberof ProgressBarModuleEngine
    ###
    render: -> throw new Error '`render` method should be overridden.'

    ###*
    # Called when receive `init` progress bar's websocket event.
    # @memberof ProgressBarModuleEngine
    # @param {Object} data - Data sent by the server.
    ###
    onInit: (data) -> throw new Error '`onInit` method should be overridden.'

    ###*
    # Called when receive `update` progress bar's websocket event.
    # @memberof ProgressBarModuleEngine
    # @param {Object} data - Data sent by the server.
    ###
    onUpdate: (data) -> throw new Error '`onUpdate` method should be overridden.'

    ###*
    # Update label.
    # @memberof ProgressBarModuleEngine
    # @param {String} label - Label to display.
    ###
    updateLabel: (label) -> throw new Error '`updateLabel` method should be overridden.'

    ###*
    # Update progression.
    # @memberof ProgressBarModuleEngine
    # @param {Number} progression - Progression to display.
    ###
    updateProgression: (progression) -> throw new Error '`updateProgression` method should be overridden.'

