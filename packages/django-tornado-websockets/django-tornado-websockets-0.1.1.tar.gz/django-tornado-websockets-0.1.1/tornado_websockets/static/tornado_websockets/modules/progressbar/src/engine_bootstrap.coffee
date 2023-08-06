class ProgressBarModuleEngineBootstrap extends ProgressBarModuleEngine

    ###*
    # Bootstrap engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
    # @constructs
    # @extends ProgressBarModuleEngine
    # @see ProgressBarModuleEngine
    ###
    constructor: (container, options) ->
        super container, options
        @_settings = {}

    ###*
    # @memberof ProgressBarModuleEngineBootstrap
    # @see ProgressBarModuleEngine#render
    ###
    render: ->
        @_createElements()
        @_renderElements()

        return

    ###*
    # @memberof ProgressBarModuleEngineBootstrap
    # @see ProgressBarModuleEngine#onInit
    ###
    onInit: (data) ->
        [min, max, value] = [0, 100, 100]

        if data.indeterminate is false
            { min: min, max: max, value: value } = data

        @_config 'indeterminate', data.indeterminate
        @_config 'min', min
        @_config 'max', max
        @_config 'value', value
        @onUpdate value: value

        return

    ###*
    # @memberof ProgressBarModuleEngineBootstrap
    # @see ProgressBarModuleEngine#onUpdate
    ###
    onUpdate: (data) ->
        @_config 'value', data.value
        @_config 'progression', ((@_settings.value / @_settings.max) * 100).toFixed()

        @$progressbar.style.width = @_settings.progression + '%'
        @updateLabel data.label if data.label isnt undefined
        @updateProgression @_settings.progression

        return

    ###*
    # @memberof ProgressBarModuleEngineBootstrap
    # @see ProgressBarModuleEngine#updateLabel
    ###
    updateLabel: (msg) ->
        @$label.textContent = msg

        return

    ###*
    # @memberof ProgressBarModuleEngineBootstrap
    # @see ProgressBarModuleEngine#updateProgression
    ###
    updateProgression: (progression) ->
        @$progression.textContent = @options.progression.format.replace /\{\{ *percent *\}\}/g, progression

        return

    ###*
    # Create HTML elements.
    # @private
    # @memberof ProgressBarModuleEngineBootstrap
    ###
    _createElements: ->
        # Progress wrapper
        @$progress = document.createElement 'div'
        @$progress.classList.add 'progress'

        # Progress bar
        @$progressbar = document.createElement 'div'
        @$progressbar.classList.add 'progress-bar'
        @$progressbar.setAttribute 'role', 'progressbar'

        if @options.progressbar.context in ['info', 'success', 'warning', 'danger']
            @$progressbar.classList.add 'progress-bar-' + @options.progressbar.context

        if @options.progressbar.striped is true
            @$progressbar.classList.add 'progress-bar-striped'
            @$progressbar.classList.add 'active' if @options.progressbar.animated is true

        # Progression (text in progress bar)
        @$progression = document.createElement 'span'
        @$progression.classList.add 'sr-only' if @options.progression.visible is false

        # Label
        @$label = document.createElement 'span'
        @$label.classList.add __ for __ in @options.label.classes
        @$label.style.display = 'none' if @options.label.visible is false

        return

    ###*
    # Render HTML elements.
    # @private
    # @memberof ProgressBarModuleEngineBootstrap
    ###
    _renderElements: ->
        @$progressbar.appendChild @$progression
        @$progress.appendChild @$progressbar
        @$container.appendChild @$progress

        if @options.label.position is 'top'
            @$container.insertBefore @$label, @$progress
        else
            @$container.appendChild @$label

        return

    ###*
    # Configure progress bar with key/value combination.
    # @private
    # @memberof ProgressBarModuleEngineBootstrap
    # @param {*} key - Key of reference.
    # @param {*} value - Value to save.
    ###
    _config: (key, value) ->
        @_settings[key] = value

        switch key
            when 'min', 'max', 'value'
                key = 'now' if key is 'value'
                @$progressbar.setAttribute 'aria-value' + key, value
            when 'indeterminate'
                if value is true
                    @$progressbar.classList.add 'progress-bar-striped'
                    @$progressbar.classList.add 'active'
                    @$progressbar.style.width = '100%'

        return
