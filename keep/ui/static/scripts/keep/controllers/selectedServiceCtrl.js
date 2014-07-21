'use strict';

angular.module('keepUiApp')
  .controller('SelectedServiceCtrl', function ($scope, $modal, Keep) {

    var keep = Keep()

    $scope.destroyService = function(service){
      new keep.Service().$delete({id: service.id})
    }
  });
