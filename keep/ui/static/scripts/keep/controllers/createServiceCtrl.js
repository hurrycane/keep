'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('NewServiceCtrl', function ($scope, $rootScope, $resource, $interval, $q, Keep) {

    $scope.viewLoading = true
    $scope.hosts = {}
    $scope.hostMetadata = {}

    $scope.images = []

    $scope.selectedService;

    var keep = Keep()

    $rootScope.refreshHosts().then(function(){
      $scope.hosts = angular.copy($rootScope.hosts)
      $scope.hostMetadata = _.object(_.map($scope.hosts, function(value, key){
        return [ key, {
          selected: false,
          instace_numbers: 0,
          port_start: 0,
          port_end: 0
        }]
      }))

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
        hosts: _.map($scope.hosts, function(value, hostname){
          var host = $scope.hostMetadata[hostname]

          return {
            name: hostname,
            container_count: host.instace_numbers,
            containers: _.map(_.range(host.instace_numbers), function(element){
              return {
                id: null,
                status: "not deployed",
                image_name: service.image,
                image_version: null,
                uptime: 0,
                ports: {},
                volumes: {},
                command: null
              }
            }),
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
      $scope.hostMetadata[host].selected = !$scope.hostMetadata[host].selected
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

  });
