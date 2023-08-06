var ProgressBarModuleEngineHtml5,
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

ProgressBarModuleEngineHtml5 = (function(superClass) {
  extend(ProgressBarModuleEngineHtml5, superClass);

  ProgressBarModuleEngineHtml5.prototype.defaults = {
    label: {
      visible: true,
      classes: ['progressbar-label'],
      position: 'top'
    },
    progression: {
      visible: true,
      format: '{{percent}}%',
      position: 'right'
    }
  };


  /**
   * HTML5 engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
   * @constructs
   * @extends ProgressBarModuleEngine
   * @see ProgressBarModuleEngine
   *
   * @prop {Object}  options - Options to use when `type` is `html5`.
   * @prop {Object}  options.label - Options for `label`'s behavior.
   * @prop {Boolean} options.label.visible - Switch on/off `label`'s visibility: `true` by default.
   * @prop {Array}   options.label.classes - Array of CSS classes for `label`'.
   * @prop {String}  options.label.position - Change `label`'s position: `bottom` or `top` by default.
   * @prop {Object}  options.progression - Options for `progression`'s behavior.
   * @prop {Boolean} options.progression.visible - Switch on/off `progression`'s visibility: `true` by default.
   * @prop {String}  options.progression.format - Change `progression`'s format: `{{percent}}%` by default
   * @prop {String}  options.progression.position - Change `progression`'s position: `left` or `right` by default.
   */

  function ProgressBarModuleEngineHtml5(container, options) {
    ProgressBarModuleEngineHtml5.__super__.constructor.call(this, container, options);
    this._settings = {};
  }


  /**
   * @memberof ProgressBarModuleEngineHtml5
   * @see ProgressBarModuleEngine#render
   */

  ProgressBarModuleEngineHtml5.prototype.render = function() {
    this._createElements();
    this._renderElements();
  };


  /**
   * @memberof ProgressBarModuleEngineHtml5
   * @see ProgressBarModuleEngine#onInit
   */

  ProgressBarModuleEngineHtml5.prototype.onInit = function(data) {
    var max, min, value;
    if (data.indeterminate) {
      return this._config('indeterminate', true);
    } else {
      min = data.min, max = data.max, value = data.value;
      this._config('min', min);
      this._config('max', max);
      this._config('value', value);
      return this.onUpdate({
        value: value
      });
    }
  };


  /**
   * @memberof ProgressBarModuleEngineHtml5
   * @see ProgressBarModuleEngine#onUpdate
   */

  ProgressBarModuleEngineHtml5.prototype.onUpdate = function(data) {
    this._config('value', data.value);
    this._config('progression', ((this._settings.value / this._settings.max) * 100).toFixed());
    if (data.label !== void 0) {
      this.updateLabel(data.label);
    }
    this.updateProgression(this._settings.progression);
  };


  /**
   * @memberof ProgressBarModuleEngineHtml5
   * @see ProgressBarModuleEngine#updateLabel
   */

  ProgressBarModuleEngineHtml5.prototype.updateLabel = function(msg) {
    this.$label.textContent = msg;
  };


  /**
   * @memberof ProgressBarModuleEngineHtml5
   * @see ProgressBarModuleEngine#updateProgression
   */

  ProgressBarModuleEngineHtml5.prototype.updateProgression = function(progression) {
    this.$progression.textContent = this.options.progression.format.replace(/\{\{ *percent *\}\}/g, progression);
  };


  /**
   * Create HTML elements.
   * @private
   * @memberof ProgressBarModuleEngineHtml5
   */

  ProgressBarModuleEngineHtml5.prototype._createElements = function() {
    var __, i, len, ref;
    this.$progress = document.createElement('div');
    this.$progress.classList.add('progress');
    this.$progressbar = document.createElement('progress');
    this.$progressbar.classList.add('progress-bar');
    this.$progression = document.createElement('span');
    if (this.options.progression.visible === false) {
      this.$progression.style.display = 'none';
    }
    this.$label = document.createElement('span');
    ref = this.options.label.classes;
    for (i = 0, len = ref.length; i < len; i++) {
      __ = ref[i];
      this.$label.classList.add(__);
    }
    if (this.options.label.visible === false) {
      this.$label.style.display = 'none';
    }
  };


  /**
   * Render HTML elements.
   * @private
   * @memberof ProgressBarModuleEngineHtml5
   */

  ProgressBarModuleEngineHtml5.prototype._renderElements = function() {
    this.$progress.appendChild(this.$progressbar);
    this.$container.appendChild(this.$progress);
    if (this.options.label.position === 'top') {
      this.$container.insertBefore(this.$label, this.$progress);
    } else {
      this.$container.appendChild(this.$label);
    }
    if (this.options.progression.position === 'left') {
      this.$progressbar.parentNode.insertBefore(this.$progression, this.$progressbar);
    } else {
      this.$progressbar.parentNode.insertBefore(this.$progression, this.$progressbar.nextSibling);
    }
  };


  /**
   * Configure progress bar with key/value combination.
   * @private
   * @memberof ProgressBarModuleEngineHtml5
   * @param {*} key - Key of reference.
   * @param {*} value - Value to save.
   */

  ProgressBarModuleEngineHtml5.prototype._config = function(key, value) {
    this._settings[key] = value;
    switch (key) {
      case 'min':
      case 'max':
      case 'value':
        this.$progressbar.setAttribute(key, value);
        break;
      case 'indeterminate':
        if (value === true) {
          this.$progressbar.removeAttribute('min');
          this.$progressbar.removeAttribute('max');
          this.$progressbar.removeAttribute('value');
        }
    }
  };

  return ProgressBarModuleEngineHtml5;

})(ProgressBarModuleEngine);
