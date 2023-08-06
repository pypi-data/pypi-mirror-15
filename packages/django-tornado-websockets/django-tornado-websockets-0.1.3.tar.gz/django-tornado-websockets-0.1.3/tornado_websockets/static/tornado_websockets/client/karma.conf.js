// Karma configuration
// Generated on Mon May 16 2016 20:25:41 GMT+0200 (CEST)

module.exports = function (config) {
    var configuration = {

        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: '',


        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine'],


        // list of files / patterns to load in the browser
        files: [
            'dist/polyfills.js',
            'dist/tornado_websocket.js',
            'dist/tornado_websocket_module.js',
            'tests/*.js'
        ],


        // list of files to exclude
        exclude: [],


        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            'dist/tornado_websocket.js': ['coverage'],
            'dist/tornado_websocket_module.js': ['coverage']
        },


        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['mocha', 'coverage'],


        // web server port
        port: 9876,


        // enable / disable colors in the output (reporters and logs)
        colors: true,


        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,


        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: false,


        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: [],

        customLaunchers: {
            Chrome_travis_ci: {
                base: 'Chrome',
                flags: ['--no-sandbox']
            }
        },


        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: true,

        // Concurrency level
        // how many browser should be started simultaneous
        concurrency: Infinity
    };

    // Browser
    if (process.env.TRAVIS) {
        var browser = process.env.BROWSER;

        if (browser == 'Chrome') {
            browser = 'Chrome_travis_ci';
        }

        configuration.browsers.push(browser);
    } else {
        configuration.browsers.push('Chrome', 'Firefox', 'Opera')
    }

    // Coveralls
    if (process.env.TRAVIS) {
        console.log('On Travis sending coveralls');
        configuration.reporters.push('coveralls');
        configuration.coverageReporter = {
            type: 'lcov',
            dir: 'coverage'
        };
    } else {
        console.log('Not on Travis so not sending coveralls');
        configuration.coverageReporter = {
            type: 'html',
            dir: 'coverage'
        }
    }

    config.set(configuration)
};
