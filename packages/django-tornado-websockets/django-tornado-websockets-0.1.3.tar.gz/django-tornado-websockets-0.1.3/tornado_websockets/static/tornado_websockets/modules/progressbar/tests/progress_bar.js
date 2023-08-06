/**
 * Created by kocal on 26/05/16.
 */

describe('`TornadoWebSocket`', function () {
    it('should be defined', function () {
        expect(TornadoWebSocket).toBeDefined();
    });
});

describe('`TornadoWebSocketModule`', function () {
    it('should be defined', function () {
        expect(TornadoWebSocketModule).toBeDefined();
    });
});

describe('`ProgressBarModule`', function () {
    it('should be defined', function () {
        expect(ProgressBarModule).toBeDefined();
    });
});

describe('`ProgressBarModuleEngineBootstrap`', function () {
    it('should be defined', function () {
        expect(ProgressBarModuleEngineBootstrap).toBeDefined();
    });
});

describe('`ProgressBarModuleEngineHtml5`', function () {
    it('should be defined', function () {
        expect(ProgressBarModuleEngineHtml5).toBeDefined();
    });
});

describe('`ProgressBarModule` instances', function () {

    it('should be a `ProgressBarModule` instance', function () {
        var ws = new TornadoWebSocket('foo');
        var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
        var progress = new ProgressBarModule(ws, engine);

        expect(progress instanceof ProgressBarModule).toBeTruthy()
    });

    it('should force a `ProgressBarModule` instance', function () {
        var ws = new TornadoWebSocket('foo');
        var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
        var progress = ProgressBarModule(ws, engine);

        expect(progress instanceof ProgressBarModule).toBeTruthy()
    });

});

describe('`ProgressBarModule::constructor(websocket, engine)`', function () {

    it('should throw an Error when there is no websocket parameter', function () {
        expect(function () {
            return new ProgressBarModule("foo");
        }).toThrow(new TypeError(
            'Parameter `websocket` should be an instance of TornadoWebSocket, got string instead.'
        ));
    });

    it('should throw an Error when there is no container', function () {
        expect(function () {
            return new ProgressBarModule(new TornadoWebSocket('foo'), 'foo');
        }).toThrow(new TypeError(
            'Parameter `engine` should be an instance of ProgressBarModuleEngine, got string instead.'
        ));
    });

    it('should not throw any Error', function () {
        expect(function () {
            var ws = new TornadoWebSocket('foo');
            var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
            return ProgressBarModule(ws, engine);
        }).not.toThrowError();
    });

});

describe('`ProgressBarModule::on(event, callback)`', function () {

    var spyOnOn, spyConsoleLog;

    beforeEach(function () {
        // kek
        spyOnOn = spyOn(TornadoWebSocket.prototype, 'on').and.callThrough();
        spyConsoleLog = spyOn(console, 'log').and.callThrough();
    });

    it("should be using `TornadoWebSocket::on(event, callback)` shortcut", function () {
        var ws = new TornadoWebSocket('foo');
        var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
        var progress = ProgressBarModule(ws, engine);

        progress.on('first_event', function (data) {
            console.log('Got `first_event`.');
        });

        progress.websocket.on('second_event', function (data) {
            console.log('Got `second_event`.');
        });

        expect(spyOnOn).toHaveBeenCalledWith('module_progressbar_first_event', jasmine.any(Function));
        expect(progress.websocket.events['module_progressbar_first_event']).toEqual(jasmine.any(Function));
        progress.websocket.events['module_progressbar_first_event']({});
        expect(spyConsoleLog).toHaveBeenCalledWith('Got `first_event`.');

        expect(spyOnOn).toHaveBeenCalledWith('second_event', jasmine.any(Function));
        expect(progress.websocket.events['second_event']).toEqual(jasmine.any(Function));
        progress.websocket.events['second_event']({});
        expect(spyConsoleLog).toHaveBeenCalledWith('Got `second_event`.');

    });

    it("`init` event should be binded for `ProgressBarModuleEngineBootstrap`.", function () {
        var spyOnInit = spyOn(ProgressBarModuleEngineBootstrap.prototype, 'onInit');

        var ws = new TornadoWebSocket('foo');
        var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
        var progress = ProgressBarModule(ws, engine);

        expect(progress.websocket.events['module_progressbar_init']).toEqual(jasmine.any(Function));
        progress.websocket.events['module_progressbar_init']({});
        expect(spyOnInit).toHaveBeenCalledWith({});
    });

    it("`update` event should be binded for `ProgressBarModuleEngineBootstrap`.", function () {
        var spyOnUpdate = spyOn(ProgressBarModuleEngineBootstrap.prototype, 'onUpdate');

        var ws = new TornadoWebSocket('foo');
        var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
        var progress = ProgressBarModule(ws, engine);

        expect(progress.websocket.events['module_progressbar_update']).toEqual(jasmine.any(Function));
        progress.websocket.events['module_progressbar_update']({});
        expect(spyOnUpdate).toHaveBeenCalledWith({});
    });

});

describe('`ProgressBarModule::emit(event, data)`', function () {

    it("should be using `TornadoWebSocket::emit(event, callback)` shortcut", function () {

        var spyOnEmit = spyOn(TornadoWebSocket.prototype, 'emit');
        var ws = new TornadoWebSocket('foo');
        var engine = new ProgressBarModuleEngineBootstrap(document.createElement('div'), {});
        var progress = ProgressBarModule(ws, engine);

        spyOnEmit.calls.reset();
        progress.websocket.emit('first_event', {});
        expect(spyOnEmit).toHaveBeenCalledWith('first_event', {});

        spyOnEmit.calls.reset();
        progress.websocket.emit('second_event', {'key': 'value'});
        expect(spyOnEmit).toHaveBeenCalledWith('second_event', {'key': 'value'});

        spyOnEmit.calls.reset();
        progress.emit('third_event', {});
        expect(spyOnEmit).toHaveBeenCalledWith('module_progressbar_third_event', {});

        spyOnEmit.calls.reset();
        progress.emit('fourth_event', {'key': 'value'});
        expect(spyOnEmit).toHaveBeenCalledWith('module_progressbar_fourth_event', {'key': 'value'});

    });

});
