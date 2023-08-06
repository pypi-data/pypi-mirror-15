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
