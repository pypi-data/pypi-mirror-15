var ProgressBarModuleEngine;

ProgressBarModuleEngine = (function() {

  /**
   * Defaults options for an engine.
   * @memberof ProgressBarModuleEngine
   * @param {Object} - Defaults options.
   */
  ProgressBarModuleEngine.prototype.defaults = {};


  /**
   * Interface for classes that represent a {@link ProgressBarModule#engine}.
   * @interface
   * @constructs
   * @param {HTMLElement} $container - HTML container for the progress bar.
   * @param {Object} options - Options from ProgressBarModule.
   */

  function ProgressBarModuleEngine($container, options) {
    if ($container === void 0 || !($container instanceof HTMLElement)) {
      throw new TypeError("Parameter `$container` should be an instance of HTMLElement, got " + (typeof $container) + " instead.");
    }
    if (!(options instanceof Object)) {
      throw new TypeError("Parameter `options` should be an Object, got " + (typeof options) + " instead.");
    }
    this.$container = $container;
    this.options = deepmerge(this.defaults, options);
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
