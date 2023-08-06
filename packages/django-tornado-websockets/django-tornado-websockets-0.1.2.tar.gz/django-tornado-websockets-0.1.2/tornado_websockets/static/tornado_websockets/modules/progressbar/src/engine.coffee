class ProgressBarModuleEngine

    ###*
    # Interface for classes that represent a {@link ProgressBarModule#engine}.
    # @interface
    # @constructs
    # @param {HTMLElement} $container - HTML container for the progress bar.
    # @param {Object} options - Options from ProgressBarModule.
    ###
    constructor: ($container, options) ->
        if $container is undefined or $container not instanceof HTMLElement
            throw new TypeError "You must pass an HTML element as container during `ProgressBarModuleEngine` instantiation."

        if options not instanceof Object
            throw new TypeError "You must pass an Object as options during `ProgressBarModuleEngine` instantiation."

        @$container = $container
        @options = options

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

