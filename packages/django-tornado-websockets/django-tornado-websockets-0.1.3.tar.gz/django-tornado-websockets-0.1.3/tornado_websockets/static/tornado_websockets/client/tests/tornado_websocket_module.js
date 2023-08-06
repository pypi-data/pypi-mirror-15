describe('`TornadoWebSocketModule`', function () {
    it('should be defined', function () {
        expect(TornadoWebSocketModule).toBeDefined();
    });
});

describe('`TornadoWebSocketModule::constructor(websocket, prefix)`', function () {
    it('should raise a TypeError because `websocket` is not a `TornadoWebSocket` instance', function () {
        expect(function () {
            new TornadoWebSocketModule("blabla");
        }).toThrow(
            new TypeError("Parameter `websocket` should be an instance of TornadoWebSocket, got string instead.")
        )
    });

    it('should cast `prefix` to string', function () {
        var ws = new TornadoWebSocket('foo');
        var twsm = new TornadoWebSocketModule(ws, 123);

        expect(twsm.prefix).toEqual("123");
    });
});

describe('`TornadoWebSocketModule::on(event, callback)`', function () {
    beforeAll(function () {
        spyOn(TornadoWebSocket.prototype, 'on');
    });

    it('should call `TornadoWebSocket.on(event, callback)', function () {
        var ws = new TornadoWebSocket('foo');
        var twsm = new TornadoWebSocketModule(ws);

        twsm.on('event', function () {

        });

        expect(TornadoWebSocket.prototype.on).toHaveBeenCalledWith('event', jasmine.any(Function));
    });

    it('should call `TornadoWebSocket.on(event, callback) with prefix', function () {
        var ws = new TornadoWebSocket('foo');
        var twsm = new TornadoWebSocketModule(ws, 'a_prefix_');

        twsm.on('event', function () {

        });

        expect(TornadoWebSocket.prototype.on).toHaveBeenCalledWith('a_prefix_event', jasmine.any(Function));
    });
});


describe('`TornadoWebSocketModule::emit(event, data)`', function () {
    beforeAll(function () {
        spyOn(TornadoWebSocket.prototype, 'emit');
    });

    it('should call `TornadoWebSocket.emit(event, data)', function () {
        var ws = new TornadoWebSocket('foo');
        var twsm = new TornadoWebSocketModule(ws);

        twsm.emit('event', {'key': 'value'});

        expect(TornadoWebSocket.prototype.emit).toHaveBeenCalledWith('event', {'key': 'value'});
    });

    it('should call `TornadoWebSocket.emit(event, data) with prefix', function () {
        var ws = new TornadoWebSocket('foo');
        var twsm = new TornadoWebSocketModule(ws, 'a_prefix_');

        twsm.emit('event');

        expect(TornadoWebSocket.prototype.emit).toHaveBeenCalledWith('a_prefix_event', {});
    });
});
