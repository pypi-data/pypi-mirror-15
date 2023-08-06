var app = angular.module('xdjango', ['ngCookies']);

app.run(function($rootScope, $location) {
    $rootScope.location = $location;
});

app.service('xdjangoApi', ['$http', '$cookies', function($http, $cookies) {

    var USERS_PATH = "/users/";
    var ONE_TIME_TOKEN_PATH = "/one-time-tokens/";

    var X_CSRF_TOKEN_HEADER_NAME = "X-CSRFToken";
    var COOKIE_HEADER_NAME = "Cookie";

    var config = {
        headers:  {
            'Content-Type': 'application/json'
        }
    };

    var urlEncode = function(obj) {
        var str = [];
        for(var p in obj)
            if (obj.hasOwnProperty(p)) {
              str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            }
        return str.join("&");
    };

    var defaultHeaders = function() {
        var csrftoken = $cookies.get("csrftoken") || "";

        var xHeaders = config.headers;
        xHeaders[X_CSRF_TOKEN_HEADER_NAME] = csrftoken;
        return xHeaders;
    };

    var _http = function(method, url, query_params, data, headers, transformRequest) {
        query_params = query_params || null;
        data = data || null;
        headers = headers || defaultHeaders();
        transformRequest = transformRequest || null;

        if (transformRequest != null)
            var req = {
                method: method,
                url: url,
                headers: headers,
                params: query_params,
                data: data,
                transformRequest: transformRequest
            };
        else
            var req = {
                method: method,
                url: url,
                headers: headers,
                params: query_params,
                data: data,
            };

        return $http(req);
    };

    this.getUsers = function() {
        return _http("GET", USERS_PATH);
    };


    this.getSession = function() {
        return _http("GET", SESSION_PATH);
    };

    this.authenticate = function(username, password) {
        var form_params = {
            'email_or_phone_number': username,
            'password': password
        };
        return _http("POST", SESSION_PATH, null, form_params);
    };

    this.updatePassword = function(user_id, password, token) {
        var password = password || null;
        var token = token || null;

        var form_params = {
            'password': password,
            'oneTimeToken': token
        };
        return _http("PATCH", USERS_PATH + user_id + "/", null, form_params);
    };
    
    this.createUser = function(email) {
        var email = email || null;
        var send_email = true;
        
        var query_params = {"send_email": send_email}

        var form_params = {
            'email': email,
            'is_staff': true,
            'is_active': true
        };
        return _http("POST", USERS_PATH, query_params, form_params);
    };

    this.createOneTimeToken = function(email) {
        email = email || null;

        var form_params = {
            'email': email
        };
        return _http("POST", ONE_TIME_TOKEN_PATH, null, form_params);
    };

}]);

