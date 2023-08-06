class ProgressBarModuleEngineHtml5 extends ProgressBarModuleEngine

    ###*
    # HTML5 engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
    # @constructs
    # @extends ProgressBarModuleEngine
    # @see ProgressBarModuleEngine
    ###
    constructor: (container, options) ->
        super container, options
        @_settings = {}

    ###*
    # @memberof ProgressBarModuleEngineHtml5
    # @see ProgressBarModuleEngine#render
    ###
    render: ->
        @_createElements()
        @_renderElements()

        return

    ###*
    # @memberof ProgressBarModuleEngineHtml5
    # @see ProgressBarModuleEngine#onInit
    ###
    onInit: (data) ->
        if data.indeterminate
            @_config 'indeterminate', true
        else
            { min: min, max: max, value: value } = data
            @_config 'min', min
            @_config 'max', max
            @_config 'value', value
            @onUpdate value: value

    ###*
    # @memberof ProgressBarModuleEngineHtml5
    # @see ProgressBarModuleEngine#onUpdate
    ###
    onUpdate: (data) ->
        @_config 'value', data.value
        @_config 'progression', ((@_settings.value / @_settings.max) * 100).toFixed()

        @updateLabel data.label if data.label isnt undefined
        @updateProgression @_settings.progression

        return

    ###*
    # @memberof ProgressBarModuleEngineHtml5
    # @see ProgressBarModuleEngine#updateLabel
    ###
    updateLabel: (msg) ->
        @$label.textContent = msg

        return

    ###*
    # @memberof ProgressBarModuleEngineHtml5
    # @see ProgressBarModuleEngine#updateProgression
    ###
    updateProgression: (progression) ->
        @$progression.textContent = @options.progression.format.replace /\{\{ *percent *\}\}/g, progression

        return

    ###*
    # Create HTML elements.
    # @private
    # @memberof ProgressBarModuleEngineHtml5
    ###
    _createElements: ->
        @$progress = document.createElement 'div'
        @$progress.classList.add 'progress'

        @$progressbar = document.createElement 'progress'
        @$progressbar.classList.add 'progress-bar'

        # Progression (text aside progress bar)
        @$progression = document.createElement 'span'
        @$progression.style.display = 'none' if @options.progression.visible is false

        # Label
        @$label = document.createElement 'span'
        @$label.classList.add __ for __ in @options.label.classes
        @$label.style.display = 'none' if @options.label.visible is false

        return

    ###*
    # Render HTML elements.
    # @private
    # @memberof ProgressBarModuleEngineHtml5
    ###
    _renderElements: ->
        @$progress.appendChild @$progressbar
        @$container.appendChild @$progress

        if @options.label.position is 'top'
            @$container.insertBefore @$label, @$progress
        else
            @$container.appendChild @$label

        if @options.progression.position is 'left'
            @$progressbar.parentNode.insertBefore @$progression, @$progressbar
        else
            # insertAfter
            @$progressbar.parentNode.insertBefore @$progression, @$progressbar.nextSibling

        return

    ###*
    # Configure progress bar with key/value combination.
    # @private
    # @memberof ProgressBarModuleEngineHtml5
    # @param {*} key - Key of reference.
    # @param {*} value - Value to save.
    ###
    _config: (key, value) ->
        @_settings[key] = value

        switch key
            when 'min', 'max', 'value'
                @$progressbar.setAttribute key, value
            when 'indeterminate'
                if value is true
                    @$progressbar.removeAttribute 'min'
                    @$progressbar.removeAttribute 'max'
                    @$progressbar.removeAttribute 'value'

        return
