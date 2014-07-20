'use strict';

angular.module('keepUiApp')
  .controller('ServiceCtrl', function ($scope, Keep) {

    $scope.services = []
    $scope.selectedService;

    var keep = Keep()

    keep.Service.index().$promise.then(function(data){
      $scope.services = data.services
    })

    $scope.show = function(service){
      $scope.selectedService = service
    }
  });
