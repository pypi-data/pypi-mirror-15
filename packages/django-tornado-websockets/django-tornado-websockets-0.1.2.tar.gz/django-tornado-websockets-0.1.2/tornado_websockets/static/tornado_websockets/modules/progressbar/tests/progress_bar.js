/**
 * Created by kocal on 26/05/16.
 */

describe('`TornadoWebSocket`', function () {
    it('should be defined', function () {
        expect(TornadoWebSocket).toBeDefined();
    });
});

describe('`ProgressBarModule`', function () {
    it('should be defined', function () {
        expect(ProgressBarModule).toBeDefined();
    });
});

describe('`ProgressBarModule` instances', function () {

    it('should be a `ProgressBarModule` instance', function () {
        var progress = new ProgressBarModule('foo', document.createElement('div'));

        expect(progress instanceof ProgressBarModule).toBeTruthy()
    });

    it('should force a `ProgressBarModule` instance', function () {
        var progress = ProgressBarModule('foo', document.createElement('div'));

        expect(progress instanceof ProgressBarModule).toBeTruthy()
    });

});

describe('`ProgressBarModule(path, container, options)`', function () {

    it('should throw an Error when there is no path', function () {
        expect(function () {
            return new ProgressBarModule();
        }).toThrow(new TypeError("You must pass 'path' parameter during 'ProgressBarModule' instantiation."));
    });

    it('should throw an Error when there is no container', function () {
        expect(function () {
            return new ProgressBarModule('foo');
        }).toThrow(new TypeError('You must pass an HTML element as container during `ProgressBarModule`'
                                 + ' instantiation.'));
    });

    it('should throw an Error when there is a container but not a valid HTMLElement.', function () {
        expect(function () {
            return new ProgressBarModule('foo', 'not an HTMLElement');
        }).toThrow(new TypeError('You must pass an HTML element as container during `ProgressBarModule`'
                                 + ' instantiation.'));
    });

    it('should throw an Error when passed `options` are not an Object instance.', function () {
        expect(function () {
            return new ProgressBarModule('foo', document.createElement('div'), 'not an object');
        }).toThrow(new TypeError('You must pass an Object as options during `ProgressBarModuleEngine`'
                                 + ' instantiation.'));
    });

    it('should not throw any Error', function () {
        expect(function () {
            return new ProgressBarModule('foo', document.createElement('div'))
        }).not.toThrowError();
    });

    it('should prefix `path` by a `/`', function () {
        var progress = new ProgressBarModule('foo', document.createElement('div'));

        expect(progress.path).toEqual('/foo');
        expect(progress.websocket.path, '/module/progress_bar/foo')
    });

    it('should not prefix `path` by a `/`', function () {
        var progress = new ProgressBarModule('/foo', document.createElement('div'));

        expect(progress.path).toEqual('/foo');
        expect(progress.websocket.path, '/module/progress_bar/foo')
    });

    it('should use `ProgressBarModuleEngineBootstrap` as rendering engine', function () {
        var progress = new ProgressBarModule('foo', document.createElement('div'), { type: 'bootstrap' });

        expect(progress.engine).toEqual(jasmine.any(ProgressBarModuleEngineBootstrap));
    });

    xit('should use `ProgressBarModuleEngineHtml5` as rendering engine', function () {
        var progress = new ProgressBarModule('foo', document.createElement('div'), { type: 'html5' });

        expect(progress.engine).toEqual(jasmine.any(ProgressBarModuleEngineHtml5));
    });

    it('should throw an Error for specifying an unknown type', function () {
        expect(function () {
            return new ProgressBarModule('foo', document.createElement('div'), { type: 'QQQQQQQQQQQQQQQQQQQ' });
        }).toThrow(new Error('Given `type` should be equal to ``bootstrap`` or ``html5``.'));
    });

});

describe('`ProgressBarModule::on(event, callback)`', function () {

    it("should be using `TornadoWebSocket::on(event, callback)` shortcut", function () {

        // kek
        var spyOnOn = spyOn(TornadoWebSocket.prototype, 'on').and.callThrough();
        var spyConsoleLog = spyOn(console, 'log').and.callThrough();
        var progress = new ProgressBarModule('foo', document.createElement('div'), { type: 'bootstrap' });

        TornadoWebSocket.prototype.on.calls.reset();

        progress.on('my_event', function () {
            console.log('Got `my_event`.');
        });

        expect(spyOnOn).toHaveBeenCalledWith('my_event', jasmine.any(Function));
        expect(progress.websocket.events.my_event).toBeDefined();
        expect(progress.websocket.events.my_event).toEqual(jasmine.any(Function));
        progress.websocket.events.my_event({}); // force call
        expect(spyConsoleLog).toHaveBeenCalledWith('Got `my_event`.');
    });

    it("`init` event should be binded for `ProgressBarModuleEngineBootstrap`.", function () {
        var spyOnInit = spyOn(ProgressBarModuleEngineBootstrap.prototype, 'onInit');
        var progress = new ProgressBarModule('foo', document.createElement('div'), { type: 'bootstrap' });

        expect(progress.websocket.events.init).toBeDefined();
        expect(progress.websocket.events.init).toEqual(jasmine.any(Function));
        progress.websocket.events.init({}); // force call
        expect(spyOnInit).toHaveBeenCalledWith({});
    });


    it("`update` event should be binded for `ProgressBarModuleEngineBootstrap`.", function () {
        var spyOnInit = spyOn(ProgressBarModuleEngineBootstrap.prototype, 'onUpdate');
        var progress = new ProgressBarModule('foo', document.createElement('div'), { type: 'bootstrap' });

        expect(progress.websocket.events.update).toBeDefined();
        expect(progress.websocket.events.update).toEqual(jasmine.any(Function));
        progress.websocket.events.update({}); // force call
        expect(spyOnInit).toHaveBeenCalledWith({});
    });

});

describe('`ProgressBarModule::emit(event, data)`', function () {

    it("should be using `TornadoWebSocket::emit(event, callback)` shortcut", function () {

        var spyOnEmit = spyOn(TornadoWebSocket.prototype, 'emit');
        var progress = new ProgressBarModule('my_progress_bar', document.createElement('div'), {
            type: 'bootstrap',
            websocket: {
                host: 'kocal.fr'
            }
        });

        progress.emit('my_event', { my: 'data' });
        expect(spyOnEmit).toHaveBeenCalledWith('my_event', { my: 'data' });

        progress.emit('my_event');
        expect(spyOnEmit).toHaveBeenCalledWith('my_event', {});
    });

});
