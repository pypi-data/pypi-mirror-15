Modules
=======

Progress bar
------------

Provide an interface to easily handle a progress bar on both server and client sides.

.. automodule:: tornado_websockets.modules.progress_bar

    Example
    ^^^^^^^

    Server-side
    '''''''''''

    .. code-block:: python

        import time
        import threading
        from tornado_websockets.modules.progress_bar import ProgressBar

        ws = WebSocket('my_app')
        progressbar = ProgressBar(ws, min=0, max=100)

        # Client emitted `my_event` event
        @ws.on
        def my_event(socket, data): pass

        # Client emitted ``module_progressbar_start_progression`` event
        @progressbar.on
        def start_progression(socket, data):

            def my_func():
                for value in range(progressbar.min, progressbar.max):
                    time.sleep(.1)  # Emulate a slow task :^)
                    progressbar.tick(label="[%d/%d] Task #%d is done" % (progressbar.value, progressbar.max, value))

            threading.Thread(None, my_func, None).start()

    Client-side
    '''''''''''

    Read client-side documentation on `<https://docs.kocal.fr/dtws-client-module-progressbar>`_.

    Usage
    ^^^^^

    Construction
    '''''''''''''
    .. autoclass:: ProgressBar

    Methods
    '''''''

    .. automethod:: ProgressBar.reset
    .. automethod:: ProgressBar.tick
    .. automethod:: ProgressBar.is_done

    Events
    ''''''

    .. automethod:: ProgressBar.on
    .. automethod:: ProgressBar.emit_init
    .. automethod:: ProgressBar.emit_update
    .. automethod:: ProgressBar.emit_done
