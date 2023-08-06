function initProgressHtml5($container, options) {
    var websocket = new TornadoWebSocket('/', {
        'host': 'kocal.fr'
    });
    var engine = new ProgressBarModuleEngineHtml5($container, options);
    return new ProgressBarModule(websocket, engine);
}

describe('`ProgressBarModule::engine`', function () {
    it('should be instance of `ProgressBarModuleEngineHtml5`', function () {
        var progress = initProgressHtml5(document.createElement('div'), {});

        expect(progress.engine).toEqual(jasmine.any(ProgressBarModuleEngineHtml5));
    });
});

describe('`ProgressBarModuleEngineHtml5::_createElements()`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('by using default options.', function () {
        var progress = initProgressHtml5($container, {});
        var $progress = progress.engine.$progress;
        var $progressbar = progress.engine.$progressbar;
        var $progression = progress.engine.$progression;
        var $label = progress.engine.$label;

        // tests for $progress
        expect($progress).toEqual(jasmine.any(HTMLDivElement));
        expect($progress.classList).toContain('progress');

        // tests for $progressbar
        expect($progressbar).toEqual(jasmine.any(HTMLProgressElement));
        expect($progressbar.classList).toContain('progress-bar');

        // tests for $progression
        expect($progression).toEqual(jasmine.any(HTMLSpanElement));
        expect($progression.style.display).toEqual('');

        // tests for $label
        expect($label).toEqual(jasmine.any(HTMLSpanElement));
        expect($label.classList).toContain('progressbar-label');
    });

    it('$label should be visible', function () {
        var progress = initProgressHtml5($container, {});
        var $label = progress.engine.$label;

        expect($label.style.display).not.toEqual('none');
    });

    it('$label should not be visible', function () {
        var progress = initProgressHtml5($container, {label: {visible: false}});
        var $label = progress.engine.$label;

        expect($label.style.display).toEqual('none');
    });

    it('$progression should be visible', function () {
        var progress = initProgressHtml5($container, {});
        var $progression = progress.engine.$progression;

        expect($progression.style.display).toEqual('');
    });

    it('$progression should not be visible', function () {
        var progress = initProgressHtml5($container, {progression: {visible: false}});
        var $progression = progress.engine.$progression;

        expect($progression.style.display).toEqual('none');
    });

});

describe('`ProgressBarModuleEngineHtml5::_renderElements()`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('$label should be above to $progressbar', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;
        var $label = progress.engine.$label;

        $label.textContent = 'Foo';
        expect($label.offsetTop).toBeLessThan($progressbar.offsetTop);
    });

    it('$label should be below to $progressbar', function () {
        var progress = initProgressHtml5($container, {label: {position: 'bottom'}});
        var $progressbar = progress.engine.$progressbar;
        var $label = progress.engine.$label;

        $label.textContent = 'Bar';
        expect($label.offsetTop).toBeGreaterThan($progressbar.offsetTop);
    });

    xit('$progression should be to the left of $progressbar', function () {
        var progress = initProgressHtml5($container, {progression: {position: 'left'}});
        var $progressbar = progress.engine.$progressbar;
        var $progression = progress.engine.$progression;

        progress.engine.onInit({indeterminate: false, min: 0, value: 50, max: 100});
        progress.engine.updateProgression('Hop');
        expect($progression.offsetLeft).toBeLessThan($progressbar.offsetLeft);
    });

    xit('$progression should to the right of $progressbar', function () {
        var progress = initProgressHtml5($container, {progression: {position: 'right'}});
        var $progressbar = progress.engine.$progressbar;
        var $progression = progress.engine.$progression;

        progress.engine.onInit({indeterminate: false, min: 0, value: 50, max: 100});
        progress.engine.updateProgression('Hop');
        expect($progression.offsetLeft).toBeGreaterThan($progressbar.offsetLeft);
    });

});

describe('`ProgressBarModuleEngineHtml5::_config(key, value)`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('should set `min` value to $progressbar', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;

        expect($progressbar.getAttribute('min')).toBeNull();

        progress.engine._config('min', 25);
        expect(parseInt($progressbar.getAttribute('min'), 10)).toEqual(25);
    });

    it('should set `max` value to $progressbar', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;

        expect($progressbar.getAttribute('max')).toBeNull();

        progress.engine._config('max', 2000);
        expect(parseInt($progressbar.getAttribute('max'), 10)).toEqual(2000);
    });

    it('should set `value` value to $progressbar', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;

        expect($progressbar.getAttribute('value')).toBeNull();

        progress.engine._config('value', 500);
        expect(parseInt($progressbar.getAttribute('value'), 10)).toEqual(500);
    });

    it('should set $progressbar in `indeterminate` state', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;

        progress.engine._config('min', 0);
        progress.engine._config('value', 50);
        progress.engine._config('max', 100);

        expect(parseInt($progressbar.getAttribute('min'), 10)).toEqual(0);
        expect(parseInt($progressbar.getAttribute('value'), 10)).toEqual(50);
        expect(parseInt($progressbar.getAttribute('max'), 10)).toEqual(100);

        progress.engine._config('indeterminate', true);
        expect($progressbar.getAttribute('min')).toBeNull();
        expect($progressbar.getAttribute('value')).toBeNull();
        expect($progressbar.getAttribute('max')).toBeNull();
    });

});

describe('`ProgressBarModuleEngineHtml5::updateLabel(msg)`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('should update label...', function () {
        var progress = initProgressHtml5($container, {});
        var $label = progress.engine.$label;

        expect($label.textContent).toEqual('');
        progress.engine.updateLabel('Message');
        expect($label.textContent).toEqual('Message');
    });
});

describe('`ProgressBarModuleEngineHtml5::updateLable(msg)`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('should update progression', function () {
        var progress = initProgressHtml5($container, {});
        var $progression = progress.engine.$progression;

        progress.engine.updateProgression(50);
        expect($progression.textContent).toEqual('50%');
    });

    it('should update progression with custom format', function () {
        var progress = initProgressHtml5($container, {progression: {format: 'Progression: {{percent}}%'}});
        var $progression = progress.engine.$progression;

        progress.engine.updateProgression(50);
        expect($progression.textContent).toEqual('Progression: 50%');
    });

});

describe('`ProgressBarModuleEngineHtml5::onInit(data)`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('should not be indeterminate', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;

        progress.engine.onInit({indeterminate: false, min: 50, value: 100, max: 200});
        expect(parseInt($progressbar.getAttribute('min'), 10)).toEqual(50);
        expect(parseInt($progressbar.getAttribute('value'), 10)).toEqual(100);
        expect(parseInt($progressbar.getAttribute('max'), 10)).toEqual(200);
    });

    it('should be indeterminate', function () {
        var progress = initProgressHtml5($container, {});
        var $progressbar = progress.engine.$progressbar;

        progress.engine.onInit({indeterminate: true, min: 500, value: 1000, max: 2000});
        expect($progressbar.getAttribute('min'), 10).toBeNull(); // 0 is default value when indeterminate
        expect($progressbar.getAttribute('value'), 10).toBeNull(); // 100 is ...
        expect($progressbar.getAttribute('max'), 10).toBeNull(); //  100 is ...
    });

});


describe('`ProgressBarModuleEngineHtml5::onUpdate(data)`', function () {

    var $container;

    beforeEach(function () {
        $container = document.createElement('div');
        $container.setAttribute('id', 'html5-container');
        document.body.appendChild($container);
    });

    afterEach(function () {
        document.body.removeChild($container);
    });

    it('should be updated', function () {
        var progress = initProgressHtml5($container, {progression: {format: 'Progression: {{percent}}%'}});
        var $progressbar = progress.engine.$progressbar;
        var $progression = progress.engine.$progression;
        var $label = progress.engine.$label;

        progress.engine.onInit({indeterminate: false, min: 0, value: 0, max: 100});
        expect(parseInt($progressbar.getAttribute('min'), 10)).toEqual(0);
        expect(parseInt($progressbar.getAttribute('value'), 10)).toEqual(0);
        expect(parseInt($progressbar.getAttribute('max'), 10)).toEqual(100);

        progress.engine.onUpdate({value: 50});
        expect(parseInt($progressbar.getAttribute('value'), 10)).toEqual(50);
        expect($progression.textContent).toEqual('Progression: 50%');
        expect($label.textContent).toEqual('');

        progress.engine.onUpdate({value: 70, label: 'A label...'});
        expect(parseInt($progressbar.getAttribute('value'), 10)).toEqual(70);
        expect($progression.textContent).toEqual('Progression: 70%');
        expect($label.textContent).toEqual('A label...');
    });

});
