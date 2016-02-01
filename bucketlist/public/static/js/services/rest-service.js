'use strict';

app.factory('BucketListService', ['$resource', function($resource) {
    return {
        auth: $resource('/auth/', {}, {
            login: {
                method: 'POST'
            }
        }, { stripTrailingSlashes: false }),

        users: $resource('/signup/', {}, {
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
            createBucketItem: {
                method: 'POST'
            },
            getOneBucketItem: {
                method: 'GET',
                isArray: false
            },
            updateBucketItem: {
                method: 'PUT'
            },
            deleteBucketItem: {
                method: 'DELETE'
            }
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
