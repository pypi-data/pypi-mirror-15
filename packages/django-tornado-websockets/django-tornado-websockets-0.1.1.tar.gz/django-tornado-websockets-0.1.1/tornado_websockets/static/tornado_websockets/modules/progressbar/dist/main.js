(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(factory);
  } else if (typeof exports === 'object') {
    module.exports = factory();
  } else {
    root.deepmerge = factory();
  }
}(this, function() {

  return function deepmerge(target, src) {
    var array = Array.isArray(src);
    var dst = array && [] || {};

    if (array) {
      target = target || [];
      dst = dst.concat(target);
      src.forEach(function(e, i) {
        if (typeof dst[i] === 'undefined') {
          dst[i] = e;
        } else if (typeof e === 'object') {
          dst[i] = deepmerge(target[i], e);
        } else {
          if (target.indexOf(e) === -1) {
            dst.push(e);
          }
        }
      });
    } else {
      if (target && typeof target === 'object') {
        Object.keys(target).forEach(function(key) {
          dst[key] = target[key];
        })
      }
      Object.keys(src).forEach(function(key) {
        if (typeof src[key] !== 'object' || !src[key]) {
          dst[key] = src[key];
        } else {
          if (!target[key]) {
            dst[key] = src[key];
          } else {
            dst[key] = deepmerge(target[key], src[key]);
          }
        }
      });
    }

    return dst;
  }

}));

var ProgressBarModuleEngine;

ProgressBarModuleEngine = (function() {

  /**
   * Interface for classes that represent a {@link ProgressBarModule#engine}.
   * @interface
   * @constructs
   * @param {HTMLElement} $container - HTML container for the progress bar.
   * @param {Object} options - Options from ProgressBarModule.
   */
  function ProgressBarModuleEngine($container, options) {
    if ($container === void 0 || !($container instanceof HTMLElement)) {
      throw new TypeError("You must pass an HTML element as container during `ProgressBarModuleEngine` instantiation.");
    }
    if (!(options instanceof Object)) {
      throw new TypeError("You must pass an Object as options during `ProgressBarModuleEngine` instantiation.");
    }
    this.$container = $container;
    this.options = options;
  }


  /**
   * Make and display an HTML render to the user.
   * @memberof ProgressBarModuleEngine
   */

  ProgressBarModuleEngine.prototype.render = function() {
    throw new Error('`render` method should be overridden.');
  };


  /**
   * Called when receive `init` progress bar's websocket event.
   * @memberof ProgressBarModuleEngine
   * @param {Object} data - Data sent by the server.
   */

  ProgressBarModuleEngine.prototype.onInit = function(data) {
    throw new Error('`onInit` method should be overridden.');
  };


  /**
   * Called when receive `update` progress bar's websocket event.
   * @memberof ProgressBarModuleEngine
   * @param {Object} data - Data sent by the server.
   */

  ProgressBarModuleEngine.prototype.onUpdate = function(data) {
    throw new Error('`onUpdate` method should be overridden.');
  };


  /**
   * Update label.
   * @memberof ProgressBarModuleEngine
   * @param {String} label - Label to display.
   */

  ProgressBarModuleEngine.prototype.updateLabel = function(label) {
    throw new Error('`updateLabel` method should be overridden.');
  };


  /**
   * Update progression.
   * @memberof ProgressBarModuleEngine
   * @param {Number} progression - Progression to display.
   */

  ProgressBarModuleEngine.prototype.updateProgression = function(progression) {
    throw new Error('`updateProgression` method should be overridden.');
  };

  return ProgressBarModuleEngine;

})();

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


  /**
   * Bootstrap engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
   * @constructs
   * @extends ProgressBarModuleEngine
   * @see ProgressBarModuleEngine
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


  /**
   * HTML5 engine for {@link ProgressBarModule} that implements {@link ProgressBarModuleEngine}.
   * @constructs
   * @extends ProgressBarModuleEngine
   * @see ProgressBarModuleEngine
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

var ProgressBarModule;

ProgressBarModule = (function() {

  /**
   * Initialize a new ProgressBarModule object with given parameters.
   *
   * @constructs
   * @param {String} path - Path of a progress bar module application
   * @param {HTMLElement} container - HTML container for progress bar HTML element
   * @param {Object}  options - Object options
   * @example
   * var $container = document.querySelector('#container');
   * var progress = new ProgressBarModule('/my_progressbar', $container, {
   *     websocket: {
   *         host: 'my_host.com'
   *     },
   *     bootstrap: {
   *         progressbar: {
   *             animated: false,
   *         },
   *         progression: {
   *             format: 'Progression: {percent}%'
   *         }
   *     }
   * });
   *
   * progress.on('open', function() {
   *
   *     progress.emit('an_event ...');
   *
   *     progress.on('before_init', function() {
   *         // Is called before progress bar initialization
   *     });
   *
   *     progress.on('after_init', function() {
   *         // Is called after progress bar initialization
   *     });
   *
   *     progress.on('before_update', function() {
   *         // Is called before progress bar updating
   *     });
   *
   *     progress.on('after_update', function() {
   *         // Is called after progress bar updating
   *     });
   *
   *     progress.on('done', function() {
   *         // Is called when progression is done
   *     });
   * });
   *
   */
  function ProgressBarModule(path, container, options) {
    if (options == null) {
      options = {};
    }
    if (!(this instanceof ProgressBarModule)) {
      return new ProgressBarModule(path, container, options);
    }
    if (path === void 0 || typeof path !== 'string') {
      throw new TypeError("You must pass 'path' parameter during 'ProgressBarModule' instantiation.");
    }
    if (container === void 0 || !(container instanceof HTMLElement)) {
      throw new TypeError("You must pass an HTML element as container during `ProgressBarModule` instantiation.");
    }
    if (!(options instanceof Object)) {
      throw new TypeError("You must pass an Object as options during `ProgressBarModuleEngine` instantiation.");
    }

    /**
     * @prop {String} path - Path of a progress bar module application.
     * @private
     */
    this.path = path.trim();
    this.path = this.path[0] === '/' ? this.path : '/' + this.path;

    /**
     * @prop {HTMLElement} container - HTML container for progress bar HTML element
     * @private
     */
    this.container = container;

    /**
     * @prop {Object}  options - Default options which can be overridden during {@link ProgressBarModule} instantiation.
     * @prop {Object}  options.websocket - Same options than `TornadoWebSocket` constructor.
     * @prop {String}  options.type - Type of the progress bar, `html5` or `bootstrap` by default.
     *
     * @prop {Object}  options.bootstrap - Options to use when `type` is `bootstrap`.
     * @prop {Object}  options.bootstrap.label - Options for `label`'s behavior.
     * @prop {Boolean} options.bootstrap.label.visible - Switch on/off `label`'s visibility: `true` by default.
     * @prop {Array}   options.bootstrap.label.classes - Array of CSS classes for `label`'.
     * @prop {String}  options.bootstrap.label.position - Change `label`'s position: `bottom` or `top` by default.
     * @prop {Object}  options.bootstrap.progressbar - Options for `progressbar`'s behavior.
     * @prop {String}  options.bootstrap.progressbar.context - Change `progress bar`'s context: `success`, `warning`, `danger`, or `info` by default.
     * @prop {Boolean} options.bootstrap.progressbar.striped - Switch on/off `progress bar`'s striped effect: `false` by default.
     * @prop {Boolean} options.bootstrap.progressbar.animated - Switch on/off `progress bar`'s animated effect: `false` by default.
     * @prop {Object}  options.bootstrap.progression - Options for `progression`'s behavior.
     * @prop {Boolean} options.bootstrap.progression.visible - Switch on/off `progression`'s visibility: `true` by default.
     * @prop {String}  options.bootstrap.progression.format - Change `progression`'s format: `{{percent}}%` by default
     *
     * @prop {Object}  options.html5 - Options to use when `type` is `html5`.
     * @prop {Object}  options.html5.label - Options for `label`'s behavior.
     * @prop {Boolean} options.html5.label.visible - Switch on/off `label`'s visibility: `true` by default.
     * @prop {Array}   options.html5.label.classes - Array of CSS classes for `label`'.
     * @prop {String}  options.html5.label.position - Change `label`'s position: `bottom` or `top` by default.
     * @prop {Object}  options.html5.progression - Options for `progression`'s behavior.
     * @prop {Boolean} options.html5.progression.visible - Switch on/off `progression`'s visibility: `true` by default.
     * @prop {String}  options.html5.progression.format - Change `progression`'s format: `{{percent}}%` by default
     * @prop {String}  options.html5.progression.position - Change `progression`'s position: `left` or `right` by default.
    
     * @private
     */
    this.options = {
      websocket: {},
      type: 'bootstrap',
      bootstrap: {
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
      },
      html5: {
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
      }
    };
    this.options = deepmerge(this.options, options);

    /**
     * @prop {ProgressBarModuleEngine} engine - Progress bar engine.
     * @public
     */
    this.engine = null;
    switch (this.options.type) {
      case 'bootstrap':
        this.engine = new ProgressBarModuleEngineBootstrap(this.container, this.options.bootstrap);
        break;
      case 'html5':
        this.engine = new ProgressBarModuleEngineHtml5(this.container, this.options.html5);
        break;
      default:
        throw new Error('Given `type` should be equal to ``bootstrap`` or ``html5``.');
    }

    /**
     * @prop {TornadoWebSocket} websocket - Instance of TornadoWebSocket.
     * @public
     */
    this.websocket = new TornadoWebSocket('/module/progress_bar' + this.path, this.options.websocket);
    this.init();
  }


  /**
   * Is automatically called at the end of the instantiation. Binds `init` and `update` events and render the
   * progress bar from defined engine.
   *
   * @memberof ProgressBarModule
   */

  ProgressBarModule.prototype.init = function() {
    this.on('init', (function(_this) {
      return function(data) {
        return _this.engine.onInit.apply(_this.engine, [data]);
      };
    })(this));
    this.on('update', (function(_this) {
      return function(data) {
        return _this.engine.onUpdate.apply(_this.engine, [data]);
      };
    })(this));
    this.engine.render();
  };


  /**
   * Shortcut off `TornadoWebSocket.on` method.
   *
   * @param {String} event - Event name.
   * @param {Function} callback - Function to execute when event `event` is received.
   * @memberof ProgressBarModule
   * @see http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#TornadoWebSocket.on
   */

  ProgressBarModule.prototype.on = function(event, callback) {
    return this.websocket.on(event, callback);
  };


  /**
   * Shortcut off `TornadoWebSocket.emit` method.
   *
   * @param {String} event - Event name.
   * @param {Object|*} data - Data to send.
   * @memberof ProgressBarModule
   * @see http://django-tornado-websockets.readthedocs.io/en/latest/usage.html#TornadoWebSocket.emit
   */

  ProgressBarModule.prototype.emit = function(event, data) {
    if (data == null) {
      data = {};
    }
    return this.websocket.emit(event, data);
  };

  return ProgressBarModule;

})();
