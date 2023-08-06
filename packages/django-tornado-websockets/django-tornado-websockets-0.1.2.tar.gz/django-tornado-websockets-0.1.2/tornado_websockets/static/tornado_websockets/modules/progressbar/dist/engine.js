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
