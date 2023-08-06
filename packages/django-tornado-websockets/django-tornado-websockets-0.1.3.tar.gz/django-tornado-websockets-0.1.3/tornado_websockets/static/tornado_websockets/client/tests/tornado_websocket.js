describe('TornadoWebSocket instances shortcuts', function () {

    it('`TornadoWebSocket()` should be an instance of TornadoWebSocket', function () {
        var ws = TornadoWebSocket('/foo');
        expect(ws instanceof TornadoWebSocket).toBeTruthy()
    });

    // In case of :^)
    it('`new TornadoWebSocket()` should be an instance of TornadoWebSocket', function () {
        var ws = new TornadoWebSocket('/foo');
        expect(ws instanceof TornadoWebSocket).toBeTruthy()
    });

});

describe('`TornadoWebSocket::constructor(path, options)', function () {

    it('should raise a ReferenceError exception because there is no "path" parameter', function () {
        expect(function () {
            return new TornadoWebSocket
        }).toThrowError(ReferenceError, "You must pass 'path' parameter during 'TornadoWebSocket' instantiation.")
    });

    it('should be using default options', function () {
        var ws = new TornadoWebSocket('my_app');

        expect(ws.options).toEqual({
            host: 'localhost',
            port: 8000,
            secure: false,
        });
    });

    it('should be merging options', function () {
        var ws = new TornadoWebSocket('my_app', {
            host: 'my.host.fr',
            port: 8080,
            secure: true
        });

        expect(ws.options).toEqual({
            host: 'my.host.fr',
            port: 8080,
            secure: true,
        });
    });


    it('should suffix path by "/"', function () {
        var ws = new TornadoWebSocket('my_app');
        expect(ws.path).toBe('/my_app');
        expect(ws.path).not.toBe('my_app')
    });

    it('should not suffix path by "/"', function () {
        var ws = new TornadoWebSocket('/my_app');
        expect(ws.path).toBe('/my_app');
        expect(ws.path).not.toBe('//my_app')
    });

});

describe('`TornadoWebSocket::buildUrl()`', function () {

    it('using default options', function () {
        var ws = new TornadoWebSocket('my_app');

        expect(ws.buildUrl(), 'ws://localhost:8000/ws/my_app')
    });

    it('using default options with suffixed path', function () {
        var ws = new TornadoWebSocket('/my_app');

        expect(ws.buildUrl(), 'ws://localhost:8000/ws/my_app')
    });

    it('using secure websocket connection', function () {
        var ws = new TornadoWebSocket('/my_app', {
            secure: true
        });

        expect(ws.buildUrl(), 'wss://localhost:8000/ws/my_app')
    });

    it('using custom host and port', function () {
        var ws = new TornadoWebSocket('/my_app', {
            host: 'my_host.fr',
            port: 8080
        });

        expect(ws.buildUrl(), 'ws://my_host.fr:8080/ws/my_app')
    });

});

describe('`TornadoWebSocket::connect()`', function () {

    it('should connect to a websocket server', function (done) {
        var ws = new TornadoWebSocket('/echo', {
            host: 'kocal.fr'
        });

        ws.on('open', function (event) {
            ws.websocket.close();
        });

        ws.on('close', function (event) {
            expect(event).toEqual(jasmine.any(CloseEvent));
            expect(event.type).toBe('close');
            done();
        });
    });

    it('should not connect to a non existing websocket server', function (done) {
        var ws = new TornadoWebSocket('/i/do/not/exist', {host: 'kocal.fr'});

        ws.on('error', function () {
            done();
        })
    });
});

describe('`TornadoWebSocket::on(event, cb)`', function () {

    beforeEach(function () {
        spyOn(console, 'info');
        spyOn(console, 'warn');
        spyOn(console, 'error');
        spyOn(console, 'log');
    });

    it('should use defaults callbacks', function () {
        var ws = new TornadoWebSocket('/my_app');

        expect(ws.websocket.onopen).toEqual(jasmine.any(Function));
        ws.websocket.onopen(new Event('open'));
        expect(console.info).toHaveBeenCalledWith('New connection', jasmine.any(Event));

        expect(ws.websocket.onclose).toEqual(jasmine.any(Function));
        ws.websocket.onclose(new CloseEvent('close'));
        expect(console.info).toHaveBeenCalledWith('Connection closed', jasmine.any(CloseEvent));

        expect(ws.websocket.onerror).toEqual(jasmine.any(Function));
        ws.websocket.onerror(new Event('open'));
        expect(console.info).toHaveBeenCalledWith('Error', jasmine.any(Event));

        expect(ws.websocket.onmessage).toEqual(jasmine.any(Function));
    });

    it('should use overridden callbacks', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.on('open', function (socket, event) {
            console.log('New connection');
        });

        ws.on('close', function (reason, event) {
            console.log('Closed connection')
        });

        ws.on('error', function (event) {
            console.log('Got an error');
        });

    });

    it('should warn about invalid JSON', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.websocket.onmessage(new MessageEvent('message', {data: 'Not JSON.'}));
        expect(console.warn).toHaveBeenCalledWith('Can not parse invalid JSON: ', 'Not JSON.');
    });

    it('should warn about passed event not found', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.websocket.onmessage(new MessageEvent('message', {
            data: JSON.stringify({"key": "data"})
        }));
        expect(console.warn).toHaveBeenCalledWith('Can not get passed event from JSON data.');
    });

    it('should warn about passed data not found', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.websocket.onmessage(new MessageEvent('message', {
            data: JSON.stringify({"event": "my_event"})
        }));
        expect(console.warn).toHaveBeenCalledWith('Can not get passed data from JSON data.');
    });

    it('should warn about passed data that is not an object', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.websocket.onmessage(new MessageEvent('message', {
            data: JSON.stringify({"event": "my_event", "data": "Not an object."})
        }));
        expect(console.warn).toHaveBeenCalledWith('Can not get passed data from JSON data.');
    });

    it('should warn about not binded passed event', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.websocket.onmessage(new MessageEvent('message', {
            data: JSON.stringify({"event": "my_event", "data": {}})
        }));
        expect(console.warn).toHaveBeenCalledWith('Passed event « my_event » is not binded.');
    });

    it('should not warn about binded passed event', function () {
        var ws = new TornadoWebSocket('/my_app');

        ws.on('my_event', function () {
        });

        ws.websocket.onmessage(new MessageEvent('message', {
            data: JSON.stringify({"event": "my_event", "data": {}})
        }));
        expect(console.warn).not.toHaveBeenCalled();
    });

    it('should not throw an exception when callback is a function', function () {
        var ws = TornadoWebSocket('/my_app');

        expect(function () {
            ws.on('open', function () {
            });
        }).not.toThrowError(TypeError, "You must pass a function for 'callback' parameter.");
    });

    it('should throw an exception when callback is not a function', function () {
        var ws = TornadoWebSocket('/my_app');

        expect(function () {
            ws.on('open', 'not a function');
        }).toThrowError(TypeError, "You must pass a function for 'callback' parameter.");
    });

});

describe('`TornadoWebSocket::emit(event, data)`', function () {

    var realWebSocket;
    var spySend;
    var spyWebSocket;
    var spyOnMessageCallback;

    beforeAll(function () {
        // Save real WebSocket class
        realWebSocket = window.WebSocket;

        // Mocking WebSocket.send method
        spySend = spyOn(WebSocket.prototype, 'send').and.callFake(function (data) {
            var data = JSON.parse(data);
            var passed_data = data.data;
            this.onmessage(passed_data);
        });

        // Mocking WebSocket class
        spyWebSocket = spyOn(window, 'WebSocket').and.callFake(function (url, protocols) {
            return new realWebSocket(url, protocols);
        });

        spyOnMessageCallback = jasmine.createSpy('onMessageCallback');
    });

    it('should send data when an object given', function () {
        var ws = new TornadoWebSocket('/my_app');
        ws.websocket.onmessage = spyOnMessageCallback;

        ws.emit('event', {
            key: 'value'
        });

        expect(spyOnMessageCallback).toHaveBeenCalledWith({key: 'value'});
        spyOnMessageCallback.calls.reset();
    });

    it('should send an empty object when no data are given', function () {
        var ws = new TornadoWebSocket('/my_app');
        ws.websocket.onmessage = spyOnMessageCallback;

        ws.emit('event');
        expect(spyOnMessageCallback).toHaveBeenCalledWith({});
        spyOnMessageCallback.calls.reset();
    });

    it('should put data in an object when given data is not an object', function () {
        var ws = new TornadoWebSocket('/my_app');
        ws.websocket.onmessage = spyOnMessageCallback;

        ws.emit('event', 'A string.');
        expect(spyOnMessageCallback).toHaveBeenCalledWith({message: 'A string.'});
        spyOnMessageCallback.calls.reset();

        ws.emit('event', 12000);
        expect(spyOnMessageCallback).toHaveBeenCalledWith({message: 12000});
        spyOnMessageCallback.calls.reset();
    });


    afterEach(function () {
        window.WebSocket = realWebSocket;
    })

});
