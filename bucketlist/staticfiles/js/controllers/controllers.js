'use strict';
angular.module('bucketlist.controllers', ['ngMaterial'])
.controller('AuthController', ['$rootScope', '$scope', '$state', '$localStorage', 'Toast', 'BucketListService',
    function AuthController($rootScope, $scope, $state, $localStorage, Toast, BucketListService) {
        $scope.user = {};
        $scope.user.signup = true;

        $scope.navLogin = function () {
            $scope.user.login = true;
            $scope.user.signup = false;
        }
        $scope.navSignup = function () {
            $scope.user.login = false;
            $scope.user.signup = true;
        }

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
    $scope.editbucket = {};

    $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
    $scope.$on('updateBucketList', function() {
        $scope.bucketlists = BucketListService.Bucketlists.getAllBuckets();
    });

    $scope.selectBucketlist = function (bucketlist) {
        $scope.selectedBucket = bucketlist
        $scope.editbucket.enabled = false;
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
                console.log(JSON.stringify(response));
                Toast.show('Yeiy! Bucketlist created successfully!')
                // nullify the new bucketlist object
                $scope.newbucket.name = null;
            }, function() {
                Toast.show('Oops! There is a bucket with the same name.')
            })
        }

    $scope.toggleUpdate = function () {
        if (!$scope.editbucket.enabled) {
            $scope.editbucket.enabled = true;
        }
        else{
            $scope.editbucket.enabled = undefined;
        }
    }

    $scope.cancelEdit = function () {
        $scope.editbucket.enabled = false;
    }
    $scope.updateBucket = function (bucketlist) {
        var data = { name: $scope.editbucket.name, id: bucketlist.id}
        BucketListService.Bucketlists.updateBucket(data).$promise
        .then(function (response) {
            Toast.show("Your bucketlist has been updated");
            $scope.$emit('updateBucketList');
            $scope.editbucket.enabled = false;
            delete $scope.selectedBucket;
            $scope.selectBucketlist(bucketlist);
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
        $scope.$on('updateBucketlistItems', function () {
            console.log("HERE IS THE STATE PARAM " + $stateParams.id);
            $scope.bucket = BucketListService.Bucketlists.getOneBucket({
                id: $stateParams.id
            });
        });

        $scope.bucket = BucketListService.Bucketlists.getOneBucket({
            id: $stateParams.id
        });
        console.log(JSON.stringify($scope.bucket));

        $scope.createBucketItem = function (params) {
            var data = angular.extend({}, params);
            data.name = $scope.newitem.name;
            BucketListService.BucketlistItems.createBucketItem(data)
            .$promise.then(function(response) {
                    console.log(JSON.stringify(response));
                    $scope.newitem.name = null
                    $scope.$emit('updateBucketlistItems');
                    Toast.show('Item created successfully');
                }, function(error) {
                    //creating an item failed
                    console.log(JSON.stringify(error));
                    if (error.status == 400) {
                        Toast.show('An item with the same name already exists');
                    }
                    else if (error.status == -1) {
                        Toast.show('You are disconnected from the server. Please ensure you have an internet connection.')
                    }
                    else {
                        Toast.show('Unable to create item. Please try again')
                    }
                })
        };

        $scope.toggleDone = function (item, itemId, bucketlistId) {
            var data = {
                done: item.done, name: item.name,
                id: itemId, bucketlist: bucketlistId, bid: bucketlistId
            };
            BucketListService.BucketlistItems.updateBucketItem(data)
            .$promise.then(function(response) {
                Toast.show("Your item has been updated.");
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
                    $scope.$emit('updateBucketlistItems');
                    Toast.show('Bucketlist Item Deleted successfully.');
                }, function (response_error) {
                    // Failed to delete item
                    console.log(JSON.stringify(response_error));
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
