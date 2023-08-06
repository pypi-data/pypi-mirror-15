var ProgressBarModuleEngineBootstrap,
  extend = function(child, parent) {
    for (var key in parent) {
      if (hasProp.call(parent, key)) child[key] = parent[key];
    }

    function ctor() {
      this.constructor = child;
    }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor();
    child.__super__ = parent.prototype;
    return child;
  },
  hasProp = {}.hasOwnProperty;

ProgressBarModuleEngineBootstrap = (function(superClass) {
  extend(ProgressBarModuleEngineBootstrap, superClass);

  ProgressBarModuleEngineBootstrap.prototype.defaults = {
    label: {
      visible: true,
      classes: ['progressbar-label'],
      position: 'top'
    },
    progressbar: {
      context: 'info',
      striped: false,
      animated: false
    },
    progression: {
      visible: true,
      format: '{{percent}}%'
    }
  };


  /**
   * Bootstrap engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
   * @constructs
   * @extends ProgressBarModuleEngine
   * @see ProgressBarModuleEngine
   *
   * @prop {Object}  options - Options to use when `type` is `bootstrap`.
   * @prop {Object}  options.label - Options for `label`'s behavior.
   * @prop {Boolean} options.label.visible - Switch on/off `label`'s visibility: `true` by default.
   * @prop {Array}   options.label.classes - Array of CSS classes for `label`'.
   * @prop {String}  options.label.position - Change `label`'s position: `bottom` or `top` by default.
   * @prop {Object}  options.progressbar - Options for `progressbar`'s behavior.
   * @prop {String}  options.progressbar.context - Change `progress bar`'s context: `success`, `warning`, `danger`, or `info` by default.
   * @prop {Boolean} options.progressbar.striped - Switch on/off `progress bar`'s striped effect: `false` by default.
   * @prop {Boolean} options.progressbar.animated - Switch on/off `progress bar`'s animated effect: `false` by default.
   * @prop {Object}  options.progression - Options for `progression`'s behavior.
   * @prop {Boolean} options.progression.visible - Switch on/off `progression`'s visibility: `true` by default.
   * @prop {String}  options.progression.format - Change `progression`'s format: `{{percent}}%` by default
   */

  function ProgressBarModuleEngineBootstrap(container, options) {
    ProgressBarModuleEngineBootstrap.__super__.constructor.call(this, container, options);
    this._settings = {};
  }


  /**
   * @memberof ProgressBarModuleEngineBootstrap
   * @see ProgressBarModuleEngine#render
   */

  ProgressBarModuleEngineBootstrap.prototype.render = function() {
    this._createElements();
    this._renderElements();
  };


  /**
   * @memberof ProgressBarModuleEngineBootstrap
   * @see ProgressBarModuleEngine#onInit
   */

  ProgressBarModuleEngineBootstrap.prototype.onInit = function(data) {
    var max, min, ref, value;
    ref = [0, 100, 100], min = ref[0], max = ref[1], value = ref[2];
    if (data.indeterminate === false) {
      min = data.min, max = data.max, value = data.value;
    }
    this._config('indeterminate', data.indeterminate);
    this._config('min', min);
    this._config('max', max);
    this._config('value', value);
    this.onUpdate({
      value: value
    });
  };


  /**
   * @memberof ProgressBarModuleEngineBootstrap
   * @see ProgressBarModuleEngine#onUpdate
   */

  ProgressBarModuleEngineBootstrap.prototype.onUpdate = function(data) {
    this._config('value', data.value);
    this._config('progression', ((this._settings.value / this._settings.max) * 100).toFixed());
    this.$progressbar.style.width = this._settings.progression + '%';
    if (data.label !== void 0) {
      this.updateLabel(data.label);
    }
    this.updateProgression(this._settings.progression);
  };


  /**
   * @memberof ProgressBarModuleEngineBootstrap
   * @see ProgressBarModuleEngine#updateLabel
   */

  ProgressBarModuleEngineBootstrap.prototype.updateLabel = function(msg) {
    this.$label.textContent = msg;
  };


  /**
   * @memberof ProgressBarModuleEngineBootstrap
   * @see ProgressBarModuleEngine#updateProgression
   */

  ProgressBarModuleEngineBootstrap.prototype.updateProgression = function(progression) {
    this.$progression.textContent = this.options.progression.format.replace(/\{\{ *percent *\}\}/g, progression);
  };


  /**
   * Create HTML elements.
   * @private
   * @memberof ProgressBarModuleEngineBootstrap
   */

  ProgressBarModuleEngineBootstrap.prototype._createElements = function() {
    var __, i, len, ref, ref1;
    this.$progress = document.createElement('div');
    this.$progress.classList.add('progress');
    this.$progressbar = document.createElement('div');
    this.$progressbar.classList.add('progress-bar');
    this.$progressbar.setAttribute('role', 'progressbar');
    if ((ref = this.options.progressbar.context) === 'info' || ref === 'success' || ref === 'warning' || ref === 'danger') {
      this.$progressbar.classList.add('progress-bar-' + this.options.progressbar.context);
    }
    if (this.options.progressbar.striped === true) {
      this.$progressbar.classList.add('progress-bar-striped');
      if (this.options.progressbar.animated === true) {
        this.$progressbar.classList.add('active');
      }
    }
    this.$progression = document.createElement('span');
    if (this.options.progression.visible === false) {
      this.$progression.classList.add('sr-only');
    }
    this.$label = document.createElement('span');
    ref1 = this.options.label.classes;
    for (i = 0, len = ref1.length; i < len; i++) {
      __ = ref1[i];
      this.$label.classList.add(__);
    }
    if (this.options.label.visible === false) {
      this.$label.style.display = 'none';
    }
  };


  /**
   * Render HTML elements.
   * @private
   * @memberof ProgressBarModuleEngineBootstrap
   */

  ProgressBarModuleEngineBootstrap.prototype._renderElements = function() {
    this.$progressbar.appendChild(this.$progression);
    this.$progress.appendChild(this.$progressbar);
    this.$container.appendChild(this.$progress);
    if (this.options.label.position === 'top') {
      this.$container.insertBefore(this.$label, this.$progress);
    } else {
      this.$container.appendChild(this.$label);
    }
  };


  /**
   * Configure progress bar with key/value combination.
   * @private
   * @memberof ProgressBarModuleEngineBootstrap
   * @param {*} key - Key of reference.
   * @param {*} value - Value to save.
   */

  ProgressBarModuleEngineBootstrap.prototype._config = function(key, value) {
    this._settings[key] = value;
    switch (key) {
      case 'min':
      case 'max':
      case 'value':
        if (key === 'value') {
          key = 'now';
        }
        this.$progressbar.setAttribute('aria-value' + key, value);
        break;
      case 'indeterminate':
        if (value === true) {
          this.$progressbar.classList.add('progress-bar-striped');
          this.$progressbar.classList.add('active');
          this.$progressbar.style.width = '100%';
        }
    }
  };

  return ProgressBarModuleEngineBootstrap;

})(ProgressBarModuleEngine);
