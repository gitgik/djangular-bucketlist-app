'use strict';
angular.module('bucketlist.controllers', ['ngMaterial'])
.controller('AuthController', ['$rootScope', '$scope', '$state', '$localStorage', 'Toast', 'BucketListService',
    function AuthController($rootScope, $scope, $state, $localStorage, Toast, BucketListService) {

        $scope.login = function () {
            var data = {username: $scope.user.username, password: $scope.user.password};
            BucketListService.auth.login(data).$promise.then(function(response){
                $localStorage.token = response.token;
                $localStorage.authenticated = true;
                $localStorage.currentUser = $scope.user.username;
                $localStorage.currentUserid = response.id;

                $state.go('dashboard');
                Toast.show('Welcome ' + $scope.user.username);
            })
            .catch(function(responseError){
                Toast.show('Incorrect credentials! Please try again.')
            });

        };

        $scope.register = function () {
            var data = {username: $scope.user.username, password: $scope.user.password};
            BucketListService.users.create(data).$promise.then($scope.login)
            .catch(function(responseError){
                Toast.show('Oops! User can\'t be registered')
            });
        };
    }])

.controller('BucketListController', ['$rootScope', '$scope', '$state', '$localStorage', '$stateParams', 'Toast', '$mdSidenav', '$timeout', 'BucketListService', '$mdDialog', 'Menu',
    function BucketListController($rootScope, $scope, $state, $localStorage, $stateParams, Toast, $mdSidenav, $timeout, BucketListService, $mdDialog, Menu) {

    $scope.selectedBucket = {};
    $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
    $scope.$on('updateBucketList', function() {
        $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
    });

    $scope.selectBucketlist = function (bucketlist) {
        $scope.selectedBucket = bucketlist
    };

    $scope.toggleLeft = Menu.toggle('left');
    $scope.close = function () {
        $mdSidenav('left').close()
            .then(function () {});
    }
    // create a bucketlist using the provided name
    $scope.createBucketlist = function () {
        var data = { name: $scope.newbucket.name };
        BucketListService.Bucketlists.createBucket(data).$promise.then(
            function(response) {
                // emit the trigger to a fresh UI update
                $scope.$emit('updateBucketList');
                Toast.show('Yeiy! Bucketlist created successfully!')
                // nullify the new bucketlist object
                $scope.newbucket.name = null;
            }, function() {
                Toast.show('Oops! There is a bucket with the same name.')
            })
    }

    $scope.updateBucket = function () {
        var data = { name: $scope.editbucket.name, id: _id}
        BucketListService.Bucketlists.updateBucket(data).$promise
        .then(function (response) {

        })
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
                Toast.show('Bucketlist deleted successfully')
            });
        }, function() {});
    };
}])

.controller('BucketListViewController', ['$rootScope', '$scope', '$state', '$localStorage', '$stateParams', 'Toast', 'Menu', 'BucketListService', '$mdSidenav', '$mdDialog',
    function BucketListViewController ($rootScope, $scope, $state, $localStorage, $stateParams, Toast, Menu, BucketListService, $mdSidenav, $mdDialog) {

        $scope.selectedBucket = {};
        $scope.newitem = {};
        $scope.selectBucketlist = function (bucketlist) {
            $state.go('viewBucket', {id: bucketlist.id});
        };

        $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
        $scope.$on('updateBucketlistItem', function () {
            $scope.bucketlist= BucketListService.Bucketlists.getOneBucket({
                id: $stateParams.id
            });
        });

        $scope.username = $localStorage.currentUser;
        $scope.bucketlist = BucketListService.Bucketlists.getOneBucket({
            id: $stateParams.id
        });

        $scope.createBucketItem = function (params) {
            var data = angular.extend({}, params);
            data.name = $scope.newitem.name;
            BucketListService.BucketlistItems.createBucketItem(data)
            .$promise.then(
                function(response) {
                    $scope.newitem.name = null
                    $scope.$emit('updateBucketlistItem');
                    Toast.show('Item created successfully');
                }, function(error) {
                    //creating an item failed
                    Toast.show('Unable to create item. Please try again')
                })
        };

        $scope.deleteBucketItem = function(ev, bucketlist) {
            // Appending dialog to document.body to cover sidenav in docs app
            var confirm = $mdDialog.confirm()
                  .title('DELETE BUCKETLIST')
                  .textContent('Are you sure you want to delete this bucketlist item? This cannot be undone.')
                  .ariaLabel('Lucky day')
                  .targetEvent(ev)
                  .ok('YES, DELETE ITEM')
                  .cancel('CANCEL');
            $mdDialog.show(confirm).then(function() {
                BucketListService.BucketlistItems.deleteBucketItem(bucketlist)
                .$promise.then(function (response) {
                    $scope.emit('updateBucketList');
                    Toast.show('Bucketlist Item Deleted successfully.');
                }, function () {
                    // Failed to delete
                    Toast.show('Could not delete item. Please try again.');
                });
            }, function() {});
        };

        $scope.toggleLeft = Menu.toggle('left');
        $scope.close = function () {
        $mdSidenav('left').close()
            .then(function () {});
    }
    }])


