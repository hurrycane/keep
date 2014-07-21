'use strict';

angular.module('keepUiApp')
  .controller('ModalDeployCtrl', function ($scope, Keep) {

  });

angular.module('keepUiApp')
  .controller('SelectedServiceCtrl', function ($scope, $modal, ModalDeployCtrl, Keep) {

    var keep = Keep()

    $scope.destroyService = function(service){
      new keep.Service().$delete({id: service.id})
    }

    $scope.deploy = function(service){
      var modalInstance = $modal.open({
        templateUrl: '/static/views/modal.deploy.html',
        controller: ModalDeployCtrl,
        resolve: {
        }
      })
    }
  });
