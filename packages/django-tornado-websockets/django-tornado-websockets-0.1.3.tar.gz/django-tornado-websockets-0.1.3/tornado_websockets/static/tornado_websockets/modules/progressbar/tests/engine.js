describe("`ProgressBarModuleEngine`", function () {

    it("should be defined", function () {
        expect(ProgressBarModuleEngine).toBeDefined();
    });

    it("should not be instantiated", function () {

    });
});

describe("`ProgressBarModuleEngine::constructor($container, options)`", function () {

    it("should throw a TypeError because there is no `$container`", function () {
        expect(function () {
            new ProgressBarModuleEngine()
        }).toThrow(new TypeError(
            'Parameter `$container` should be an instance of HTMLElement, got undefined instead.'
        ));
    });

    it("should not throw a TypeError because `$container` is an HTMLElement", function () {
        expect(function () {
            var $container = document.createElement('div');
            new ProgressBarModuleEngine($container);
        }).not.toThrow(new TypeError(
            'Parameter `$container` should be an instance of HTMLElement, got undefined instead.'
        ));
    });

    it("should throw a TypeError because `options` is not an Object", function () {
        expect(function () {
            var $container = document.createElement('div');
            new ProgressBarModuleEngine($container, 'not an object');
        }).toThrow(new TypeError('Parameter `options` should be an Object, got string instead.'));
    });

    it("should not throw a TypeError because `options` is an Object", function () {
        expect(function () {
            var $container = document.createElement('div');
            new ProgressBarModuleEngine($container, {'my': 'object'});
        }).not.toThrow(new TypeError('Parameter `options` should be an Object, got string instead.'));
    });

});

describe("`ProgressBarModuleEngine` methods should be overridden.", function () {
    function MyEngine() {
        return MyEngine.__super__.constructor.apply(this, arguments);
    }

    extend(MyEngine, ProgressBarModuleEngine);
    var myEngine = new MyEngine(document.createElement('div'), {my: 'object'});

    it("`ProgressBarModuleEngine::render()` should be overridden.", function () {
        expect(function () {
            myEngine.render();
        }).toThrow(new Error('`render` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::onInit(data)` should be overridden.", function () {
        expect(function () {
            myEngine.onInit();
        }).toThrow(new Error('`onInit` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::onUpdate(data)` should be overridden.", function () {
        expect(function () {
            myEngine.onUpdate();
        }).toThrow(new Error('`onUpdate` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::updateLabel(label)` should be overridden.", function () {
        expect(function () {
            myEngine.updateLabel();
        }).toThrow(new Error('`updateLabel` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::updateProgression(progression)` should be overridden.", function () {
        expect(function () {
            myEngine.updateProgression();
        }).toThrow(new Error('`updateProgression` method should be overridden.'));
    });

});

describe("`ProgressBarModuleEngine` methods should be overridden.", function () {
    function MyEngine() {
        return MyEngine.__super__.constructor.apply(this, arguments);
    }

    extend(MyEngine, ProgressBarModuleEngine);

    MyEngine.prototype.render = function () {
    };
    MyEngine.prototype.onInit = function () {
    };
    MyEngine.prototype.onUpdate = function () {
    };
    MyEngine.prototype.updateLabel = function () {
    };
    MyEngine.prototype.updateProgression = function () {
    };

    var myEngine = new MyEngine(document.createElement('div'), {my: 'object'});

    it("`ProgressBarModuleEngine::render()` should be overridden.", function () {
        expect(function () {
            myEngine.render();
        }).not.toThrow(new Error('`render` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::onInit(data)` should be overridden.", function () {
        expect(function () {
            myEngine.onInit();
        }).not.toThrow(new Error('`onInit` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::onUpdate(data)` should be overridden.", function () {
        expect(function () {
            myEngine.onUpdate();
        }).not.toThrow(new Error('`onUpdate` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::updateLabel(label)` should be overridden.", function () {
        expect(function () {
            myEngine.updateLabel();
        }).not.toThrow(new Error('`updateLabel` method should be overridden.'));
    });


    it("`ProgressBarModuleEngine::updateProgression(progression)` should be overridden.", function () {
        expect(function () {
            myEngine.updateProgression();
        }).not.toThrow(new Error('`updateProgression` method should be overridden.'));
    });

});
