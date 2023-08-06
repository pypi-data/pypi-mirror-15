var ProgressBarModule,
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

ProgressBarModule = (function(superClass) {
  extend(ProgressBarModule, superClass);


  /**
   * Initialize a new ProgressBarModule object with given parameters.
   *
   * @constructs
   * @param {TornadoWebSocket} websocket - A TornadoWebSocket instance.
   * @param {ProgressBarModuleEngine} engine - An instance that implement ProgressBarModuleEngineInterface.
   * @param {string} prefix - String that will prefix events name for TornadoWebSocket's on/emit methods.
   * @example
   * var websocket = new TornadoWebSocket('/my_progressbar');
   * var $container = document.querySelector('#container');
   * var engine = new ProgressBarModuleEngineBootstrap($container, {
   *     progressbar: {
   *         animated: true,
   *         striped: true,
   *     }
   * });
   *
   * var progress = new ProgressBarModule(websocket, engine, 'my_prefix');
   *
   * websocket.on('open', function() {
   *
   *     // emit 'event'
   *     websocket.emit('event ...');
   *
   *     // emit 'my_prefix_event'
   *     progress.emit('event ...');
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

  function ProgressBarModule(websocket, engine, prefix) {
    if (prefix == null) {
      prefix = 'module_progressbar_';
    }
    if (!(this instanceof ProgressBarModule)) {
      return new ProgressBarModule(websocket, engine);
    }
    if (!(websocket instanceof TornadoWebSocket)) {
      throw new TypeError("Parameter `websocket` should be an instance of TornadoWebSocket, got " + (typeof websocket) + " instead.");
    }
    if (!(engine instanceof ProgressBarModuleEngine)) {
      throw new TypeError("Parameter `engine` should be an instance of ProgressBarModuleEngine, got " + (typeof engine) + " instead.");
    }
    ProgressBarModule.__super__.constructor.call(this, websocket, prefix);

    /**
     * @prop {ProgressBarModuleEngine} engine - Progress bar engine implementing this interface.
     * @public
     */
    this.engine = engine;
    this.init();
    return;
  }


  /**
   * Is automatically called at the end of the current object instantiation. Binds `init` and `update` events and
   * render the progress bar from defined engine.
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

  return ProgressBarModule;

})(TornadoWebSocketModule);
