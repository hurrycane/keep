'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('DeployCtrl', function ($scope, $rootScope, $resource, $interval, $q, Keep) {

    $scope.viewLoading = true
    $scope.hosts = []
    $scope.images = []

    $scope.selectedService;

    var keep = Keep()

    $rootScope.refreshHosts().then(function(){
      $scope.hosts = $rootScope.hosts

      keep.getAvailableImages().success(function(data){
        $scope.images = data.services
        $scope.viewLoading = false
      })
    })

    $scope.save = function(service){
      new keep.Service({
        name: service.name,
        image: service.image,
        stage: _.first(_.where($scope.stages, { selected: true })).name,
        hosts: _.map($scope.hosts, function(host){
          return {
            name: host.name,
            containers: host.containers,
            ports: {
              start: host.port_start,
              end: host.port_end
            }
          }
        }),
        envvars: $scope.envvars,
        volumes: $scope.volumes
      }).$save()
    }

    $scope.stages = [
      { name: "Alpha", selected: true},
      { name: "Beta", selected: false },
      { name: "Gamma", selected: false },
      { name: "Prod", selected: false }
    ]

    $scope.envvars = [
      { name: "", value: "" }
    ]

    $scope.volumes = [
      { name: "", value: "" }
    ]

    $scope.selectHost = function(host){
      host.selected = !host.selected
    }

    $scope.selectStage = function(stage){
      $scope.stages = _.map($scope.stages, function(item){
        if(item == stage){
          item.selected = true
        }else{
          item.selected = false
        }
        return item
      })
    }

    $scope.appendCollection = function(collection){
      collection.push({name:"", value:""})
    }

    $scope.$on('$destroy', function() {
      if (angular.isDefined(stop)) {
        $interval.cancel(stop);
        stop = undefined;
      }
    })

  });
