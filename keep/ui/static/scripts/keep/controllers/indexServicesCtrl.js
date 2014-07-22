'use strict';

angular.module('keepUiApp')
  .controller('IndexServiceCtrl', function ($scope, $rootScope, Keep) {

    $scope.services = []
    $scope.selectedService;

    $scope.viewLoading = true

    var keep = Keep()

    keep.Service.index().$promise.then(function(data){
      $scope.services = data.services

      $rootScope.refreshHosts().then(function(){
        $scope.viewLoading = false
      })
    })

    $scope.show = function(service){
      $scope.selectedService = service
    }
  });
