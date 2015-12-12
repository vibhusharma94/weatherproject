app.service('APIService', ['$http', 'API_HOST', function($http, API_HOST) {

        var _postRequest = function(endPoint, data, headers) {
            
            //var url = API_HOST + endPoint;
            var url = endPoint
            var config = {headers:  headers};
            return $http.post(url, data, config)
        };

        var _getRequest = function(endPoint, params, headers) {
            //var url = API_HOST + endPoint;
            var url = endPoint
            if (params && Object.keys(params).length > 0) {
                url = url + '?';
                for (var key in params) {
                  if (params.hasOwnProperty(key)) {
                    url = url + key + '=' + params[key] + '&';   
                  }
                }
            };

            var config = {headers:  headers
            };
            return $http.get(url,config)
        }

        return {
            getRequest: _getRequest,
            postRequest: _postRequest
        };
}]);