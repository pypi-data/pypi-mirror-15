class ProgressBarModuleEngineBootstrap extends ProgressBarModuleEngine

    @::defaults =
        label:
            visible: true
            classes: ['progressbar-label']
            position: 'top' # 'bottom'
        progressbar:
            context: 'info' # 'success', 'warning', 'danger'
            striped: false,
            animated: false,
        progression:
            visible: true,
            format: '{{percent}}%'

    ###*
    # Bootstrap engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
    # @constructs
    # @extends ProgressBarModuleEngine
    # @see ProgressBarModuleEngine
    #
    # @prop {Object}  options - Options to use when `type` is `bootstrap`.
    # @prop {Object}  options.label - Options for `label`'s behavior.
    # @prop {Boolean} options.label.visible - Switch on/off `label`'s visibility: `true` by default.
    # @prop {Array}   options.label.classes - Array of CSS classes for `label`'.
    # @prop {String}  options.label.position - Change `label`'s position: `bottom` or `top` by default.
    # @prop {Object}  options.progressbar - Options for `progressbar`'s behavior.
    # @prop {String}  options.progressbar.context - Change `progress bar`'s context: `success`, `warning`, `danger`, or `info` by default.
    # @prop {Boolean} options.progressbar.striped - Switch on/off `progress bar`'s striped effect: `false` by default.
    # @prop {Boolean} options.progressbar.animated - Switch on/off `progress bar`'s animated effect: `false` by default.
    # @prop {Object}  options.progression - Options for `progression`'s behavior.
    # @prop {Boolean} options.progression.visible - Switch on/off `progression`'s visibility: `true` by default.
    # @prop {String}  options.progression.format - Change `progression`'s format: `{{percent}}%` by default
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
