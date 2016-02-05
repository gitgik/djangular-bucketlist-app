'use strict';

var app = angular.module('bucketlist',
    [
        'ui.router',
        'ngMaterial',
        'angularMoment',
        'ngResource',
        'ngStorage',
        'bucketlist.controllers',
    ]);

app.config(['$stateProvider', '$urlRouterProvider', '$locationProvider', '$httpProvider',
    function($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {

    $stateProvider
        .state('signup', {
            url: '/signup',
            controller: 'AuthController',
            templateUrl: '/static/views/signup.html',
            module: 'public'
        })

        .state('logout', {
            url: '/logout',
            controller: function($rootScope, $state, $localStorage) {
                $localStorage.$reset();
                $state.go('signup', {}, {
                    reload: true
                });
            },
            module: 'private'
        })

        //States for bucketlist
        .state('viewBucket', {
            url: '/bucketlists/:id/items',
            controller: 'BucketListViewController',
            templateUrl: '/static/views/bucketlist-view.html',
            module: 'private'
        })


        .state('dashboard', {
            url: '/bucketlists',
            controller: 'BucketListController',
            templateUrl: '/static/views/dashboard.html',
            module: 'private'
        });


    $urlRouterProvider.otherwise('/signup');

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.interceptors.push('httpRequestInterceptor');

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
}]);

app.run(function($rootScope, $state, $localStorage, BucketListService) {
    $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams) {
        if (toState.module === 'private' && !$localStorage.authenticated) {
            // If logged out and transitioning to a logged in page:
            event.preventDefault();
            $state.go('login', {}, {
                reload: true
            });
        }
        if (toState.module === 'public' && $localStorage.authenticated) {
            event.preventDefault();
            $state.go('dashboard', {}, {
                reload: true
            });
        }

    });
});
