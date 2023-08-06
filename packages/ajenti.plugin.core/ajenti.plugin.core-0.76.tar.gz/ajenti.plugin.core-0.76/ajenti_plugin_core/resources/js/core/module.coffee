angular.module 'core', [
    'ngAnimate',
    'ngCookies',
    'ngRoute',
    'ngStorage',
    'ngTouch',

    'angular-loading-bar',
    'btford.socket-io',
    'persona',
    'toaster',
    'ui.bootstrap',
    'angular-sortable-view',
    'base64',
    'gettext',
]


angular.module('core').config ($httpProvider, $animateProvider, $compileProvider) ->
    $httpProvider.interceptors.push 'urlPrefixInterceptor'
    $httpProvider.interceptors.push 'unauthenticatedInterceptor'
    $animateProvider.classNameFilter /animate.+/
    $compileProvider.aHrefSanitizationWhitelist /^\s*(https?|ftp|mailto|data|file):/


angular.module('core').run () ->
    FastClick.attach(document.body)


angular.module('core').factory '$exceptionHandler', ($injector, $log, gettext) ->
    return (exception, cause) ->
        if not exception.toString().startsWith('Possibly unhandled rejection')
            $injector.get('notify').warning gettext('Unhanded error occured'), gettext('Please see browser console')

        console.group('Unhandled exception occured')
        console.warn('Consider sending this error to https://github.com/ajenti/ajenti/issues/new')
        $log.error.apply $log, arguments
        console.groupEnd()


Array.prototype.remove = (args...) ->
    output = []
    for arg in args
        index = @indexOf arg
        output.push @splice(index, 1) if index isnt -1
    output = output[0] if args.length is 1
    output


Array.prototype.contains = (v) ->
    return @indexOf(v) > -1


Array.prototype.toggleItem = (v) ->
    if @contains(v)
        @remove(v)
    else
        @push(v)


String.prototype.lpad = (padString, length) ->
    str = this
    while (str.length < length)
        str = padString + str
    return str
