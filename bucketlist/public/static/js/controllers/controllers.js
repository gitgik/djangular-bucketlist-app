'use strict';
angular.module('bucketlist.controllers', ['ngMaterial'])
.controller('AuthController', ['$rootScope', '$scope', '$state', '$localStorage', '$mdToast', 'BucketListService',
    function AuthController($rootScope, $scope, $state, $localStorage, $mdToast, BucketListService) {

        var showToast = function (message) {
            $mdToast.show(
                $mdToast.simple()
                    .textContent(message)
                    .position($scope.getToastPosition())
                    .hideDelay(2000)
                );
        }
        $scope.login = function () {
            var data = {username: $scope.user.username, password: $scope.user.password};
            BucketListService.auth.login(data).$promise.then(function(response){
                $localStorage.token = response.token;
                $localStorage.authenticated = true;
                $localStorage.currentUser = $scope.user.username;
                $localStorage.currentUserid = response.id;

                $state.go('dashboard');
                showToast('Welcome ' + $scope.user.username);
            })
            .catch(function(responseError){
                showToast('Incorrect credentials! Please try again.')
            });

        };

        $scope.register = function () {
            var data = {username: $scope.user.username, password: $scope.user.password};
            BucketListService.users.create(data).$promise.then($scope.login)
            .catch(function(responseError){
                $mdToast.show(
                    $mdToast.simple()
                        .textContent('Yikes! Could not register user.')
                        .position($scope.getToastPosition())
                        .hideDelay(2000)
                );
            });
        };
        var last = {
            bottom: false, top: true,
            left: false, right: true
        };
        var sanitizePosition = function () {
            var current = $scope.toastPosition;
            if ( current.bottom && last.top ) current.top = false;
            if ( current.top && last.bottom ) current.bottom = false;
            if ( current.right && last.left ) current.left = false;
            if ( current.left && last.right ) current.right = false;
            last = angular.extend({},current);
        }
        $scope.toastPosition = angular.extend({},last);
        $scope.getToastPosition = function() {
            sanitizePosition();
            return Object.keys($scope.toastPosition)
              .filter(function(pos) { return $scope.toastPosition[pos]; })
              .join(' ');
        };
    }])

.controller('BucketListController', ['$rootScope', '$scope', '$state', '$localStorage', '$stateParams', '$mdToast', '$mdSidenav', '$timeout', 'BucketListService', '$mdDialog',
    function BucketListController($rootScope, $scope, $state, $localStorage, $stateParams, $mdToast, $mdSidenav, $timeout, BucketListService, $mdDialog) {

    $scope.selectedBucket = {};
    $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
    $scope.$on('updateBucketList', function() {
        $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
    });

    $scope.selectBucketlist = function (bucketlist) {
        $scope.selectedBucket = bucketlist
    };

    // create a bucketlist using the provided name
    $scope.createBucketlist = function () {
        var data = { name: $scope.newbucket.name };
        BucketListService.Bucketlists.createBucket(data).$promise.then(
            function(response) {
                // emit the trigger to a fresh UI update
                $scope.$emit('updateBucketList');
                showToast('Yeiy! Bucketlist created successfully!')
                // nullify the new bucketlist object
                $scope.newbucket.name = null;
            }, function() {
                showToast('Oops! There is a bucket with the same name.')
            })
    }

    $scope.updateBucket = function () {
        var data = { name: $scope.editbucket.name, id: _id}
        BucketListService.Bucketlists.updateBucket(data).$promise
        .then(function (response) {

        })
    };

    // helper functions for toast.
    $scope.toggleLeft = buildDelayedToggler('left');
    $scope.close = function () {
      $mdSidenav('left').close()
        .then(function () {});
    };
    /**
     * Supplies a function that will continue to operate until the
     * time is up.
     */
    function debounce(func, wait, context) {
      var timer;
      return function debounced() {
        var context = $scope,
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

    var showToast = function (message) {
        $mdToast.show(
            $mdToast.simple()
                .textContent(message)
                .position($scope.getToastPosition())
                .hideDelay(2000)
            );
    };

    $scope.showConfirm = function(ev, bucketlist) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
              .title('DELETE BUCKETLIST')
              .textContent('Are you sure you want to delete this bucketlist? This cannot be undone.')
              .ariaLabel('Lucky day')
              .targetEvent(ev)
              .ok('YES, DELETE IT')
              .cancel('CANCEL');
        $mdDialog.show(confirm).then(function() {
            bucketlist.$deleteBucket().then(function() {
                delete $scope.selectedBucket;
                $scope.$emit('updateBucketList');
                showToast('Bucketlist deleted successfully')
            });
        }, function() {});
    };

    var last = {
        bottom: false, top: true,
        left: false, right: true
    };
    var sanitizePosition = function () {
        var current = $scope.toastPosition;
        if ( current.bottom && last.top ) current.top = false;
        if ( current.top && last.bottom ) current.bottom = false;
        if ( current.right && last.left ) current.left = false;
        if ( current.left && last.right ) current.right = false;
        last = angular.extend({},current);
    }
    $scope.toastPosition = angular.extend({},last);
    $scope.getToastPosition = function () {
        sanitizePosition();
        return Object.keys($scope.toastPosition)
          .filter(function(pos) { return $scope.toastPosition[pos]; })
          .join(' ');
    };
}])

.controller('BucketListViewController', ['$rootScope', '$scope', '$state', '$localStorage', '$stateParams', '$mdToast', '$mdSidenav', '$timeout', 'BucketListService', '$mdDialog',
    function BucketListViewController ($rootScope, $scope, $state, $localStorage, $stateParams, $mdToast, $mdSidenav, $timeout, BucketListService, $mdDialog) {

        $scope.$on('updateBucketlist', function () {
            $scope.bucketlist= BucketListService.Bucketlists.getOneBucket({
                id: $stateParams.id
            });
        });

        $scope.username = $localStorage.currentUser;
        $scope.bucketlist = BucketListService.Bucketlists.getOneBucket({
            id: $stateParams.id
        });

    }])


