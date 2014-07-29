'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('EditServiceCtrl', function ($scope, $rootScope, $resource, $interval, $q, $routeParams, $location, Keep) {

    $scope.serviceId = $routeParams.serviceId;

    $scope.viewLoading = true
    $scope.hosts = {}
    $scope.hostMetadata = {}

    $scope.images = []

    $scope.selectedService;

    $scope.stages = [
      { name: "Alpha", selected: true},
      { name: "Beta", selected: false },
      { name: "Gamma", selected: false },
      { name: "Prod", selected: false }
    ]

    var keep = Keep()

    $rootScope.refreshHosts().then(function(){
      var availableImages = keep.getAvailableImages()
      var fetchService = keep.Service.get({serviceId: $scope.serviceId})

      $scope.hosts = angular.copy($rootScope.hosts)

      $scope.hostMetadata = _.object(_.map($scope.hosts, function(value, key){
        return [ key, {
          selected: false,
          instace_numbers: 0,
          port_start: 0,
          port_end: 0
        }]
      }))

      $q.all([availableImages, fetchService.$promise]).then(function(images, service){

        availableImages.then(function(images){
          $scope.images = images.data.services
        })
        fetchService.$promise.then(function(data){
          $scope.service = data.service

          console.log($scope.service.stage)
          $scope.selectStage($scope.service.stage)

          _.each($scope.service.hosts, function(elem){
            $scope.hostMetadata[elem.name] = {
              selected: true,
              instace_numbers: elem.container_count,
              port_start: elem.ports.start,
              port_end: elem.ports.end
            }
          })
          $scope.viewLoading = false
        })
      })
    })

    $scope.save = function(service){
      keep.Service.update({serviceId: $scope.serviceId}, {
        name: service.name,
        image: service.image,
        stage: _.first(_.where($scope.stages, { selected: true })).name,
        hosts: _.map($scope.hosts, function(value, hostname){
          var host = $scope.hostMetadata[hostname]

          return {
            name: hostname,
            container_count: host.instace_numbers,
            ports: {
              start: host.port_start,
              end: host.port_end
            }
          }
        }),
        envvars: service.envvars,
        volumes: service.volumes
      })
      //$location.path("/").replace()
    }

    $scope.selectHost = function(host){
      $scope.hostMetadata[host].selected = !$scope.hostMetadata[host].selected
    }

    $scope.selectStage = function(stage){
      $scope.stages = _.map($scope.stages, function(item){
        if(item.name == stage){
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
