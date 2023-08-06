angular.module('core').service 'config', ($http, $q, initialConfigContent) ->
    @load = () =>
        q = $q.defer()
        $http.get("/api/core/config").success (data) =>
            @data = data
            q.resolve()
        .error (err) ->
            q.reject(err)
        return q.promise

    @save = () =>
        q = $q.defer()
        $http.post("/api/core/config", @data).success () ->
            q.resolve()
        .error (err) ->
            q.reject(err)
        return q.promise

    @getUserConfig = () ->
        q = $q.defer()
        $http.get("/api/core/user-config").success (data) ->
            q.resolve(data)
        .error (err) ->
            q.reject(err)
        return q.promise

    @setUserConfig = (config) ->
        q = $q.defer()
        $http.post("/api/core/user-config", config).success (data) ->
            q.resolve(data)
        .error (err) ->
            q.reject(err)
        return q.promise

    @getAuthenticationProviders = (config) ->
        q = $q.defer()
        $http.post("/api/core/authentication-providers", config).success (data) ->
            q.resolve(data)
        .error (err) ->
            q.reject(err)
        return q.promise

    @getPermissions = (config) ->
        q = $q.defer()
        $http.post("/api/core/permissions", config).success (data) ->
            q.resolve(data)
        .error (err) ->
            q.reject(err)
        return q.promise

    @data = initialConfigContent
    q = $q.defer()
    q.resolve(@data)
    @promise = q.promise

    return this
