'use strict';

app.factory('BucketlistService', ['$resource', function($resource) {
    return {
        auth: $resource('/api/auth/', {}, {
            login: {
                method: 'POST'
            }
        }, { stripTrailingSlashes: false }),

        users: $resource('api/signup/', {}, {
            create: {
                method: 'POST'
            }
        }, { stripTrailingSlashes: false }),

        Bucketlists: $resource('/api/bucketlists/:id/', {id: "@id"},
        {
            createBucket: { method: 'POST'},
            getAllBuckets: { method: 'GET', isArray: true},
            getOneBucket: { method: 'GET', isArray: false},
            updateBucket: { method: 'PUT'},
            deleteBucket: { method: 'DELETE'}
        },
        { stripTrailingSlashes: false }),

        BucketlistItems: $resource('api/bucketlists/:bid/items/:id/', {bid:"@bid", id: "@id"},
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
}])

.factory('httpRequestInterceptor', function($localStorage) {
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
