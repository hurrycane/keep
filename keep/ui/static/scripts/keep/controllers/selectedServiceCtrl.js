'use strict';

var ModalDeployCtrl = function($scope, $modalInstance, serviceName, serviceVersions) {

  $scope.serviceVersions = serviceVersions
  $scope.serviceName = serviceName

  $scope.close = function(){
    $modalInstance.dismiss('cancel')
  }
}

angular.module('keepUiApp')
  .controller('SelectedServiceCtrl', function ($scope, $modal, Keep) {

    var keep = Keep()

    $scope.destroyService = function(service){
      new keep.Service().$delete({id: service.id})
    }

    $scope.deploy = function(service){
      var image_name = service.image.split("/")[1]

      keep.getImageVersions(image_name).success(function(data){

        var modalInstance = $modal.open({
          templateUrl: '/static/views/services/modal.deploy.html',
          controller: ModalDeployCtrl,
          resolve: {
            serviceName: function(){
              return service.name
            },
            serviceVersions: function(){
              return data.versions
            }
          }
        })

      })
    }
  });
