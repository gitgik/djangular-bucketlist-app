'use strict';

app.factory('BucketListService', ['$resource', function($resource) {
    return {
        auth: $resource('/auth/', {}, {
            login: {
                method: 'POST'
            }
        }, { stripTrailingSlashes: false }),

        verify: $resource('/auth_verify/', {}, {
            token: {
                method: 'POST'
            }
        }, {
            stripTrailingSlashes: false
        }),

        users: $resource('/auth/signup/', {}, {
            create: {
                method: 'POST'
            }
        }, { stripTrailingSlashes: false }),

        Bucketlists: $resource('/bucketlists/:id/', {id: "@id"},
        {
            createBucket: { method: 'POST'},
            getAllBuckets: { method: 'GET', isArray: true},
            getOneBucket: { method: 'GET', isArray: false},
            updateBucket: { method: 'PUT'},
            deleteBucket: { method: 'DELETE'}
        },
        { stripTrailingSlashes: false }),

        BucketlistItems: $resource('/bucketlists/:bid/items/:id/', {bid:"@bid", id: "@id"},
        {
            createBucketItem: { method: 'POST'},
            getOneBucketItem: { method: 'GET', isArray: false },
            updateBucketItem: { method: 'PUT' },
            deleteBucketItem: { method: 'DELETE'}
        },
        { stripTrailingSlashes: false })
    };
}]);

app.factory('httpRequestInterceptor', function($localStorage) {
    return {
        request: function(config) {
            var token = $localStorage.token;
            config.headers = config.headers || {};
            if (token) {
                config.headers['Authorization'] = 'JWT '+ token;
            }
            return config;
        }
    };
});

app.factory('Toast', function($mdToast) {
    var last = {
        bottom: false, top: true,
        left: false, right: true
    };
    var toastPosition = angular.extend({},last);
    var sanitizePosition = function () {
        var current = toastPosition;
        if ( current.bottom && last.top ) current.top = false;
        if ( current.top && last.bottom ) current.bottom = false;
        if ( current.right && last.left ) current.left = false;
        if ( current.left && last.right ) current.right = false;
        last = angular.extend({},current);
    }
    var getToastPosition = function () {
        sanitizePosition();
        return Object.keys(toastPosition)
          .filter(function(pos) { return toastPosition[pos]; })
          .join(' ');
    };

    return {
        show: function(message) {
            $mdToast.show(
            $mdToast.simple()
                .textContent(message)
                .position(getToastPosition())
                .hideDelay(2000)
            );
        }
    }
});

app.factory('Menu', function($mdSidenav, $timeout, Toast) {
    return {
        toggle: function(side) {
            return buildDelayedToggler(side);
        }
    }
    /**
     * Supplies a function that will continue to operate until the
     * time is up.
     */
    function debounce(func, wait, context) {
      var timer;
      return function debounced() {
        var context,
            args = Array.prototype.slice.call(arguments);
        $timeout.cancel(timer);
        timer = $timeout(function() {
          timer = undefined;
          func.apply(context, args);
        }, wait || 10);
      };
    }
    /**
     * Build handler to open/close a SideNav; when animation finishes
     * report completion in console
     */
    function buildDelayedToggler(navID) {
      return debounce(function() {
        $mdSidenav(navID)
          .toggle()
          .then(function () {});
      }, 200);
    }
});

