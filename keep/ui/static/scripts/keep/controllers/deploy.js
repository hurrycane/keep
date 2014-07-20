'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('DeployCtrl', function ($scope, $resource, $interval, $q, Keep) {

    $scope.viewLoading = true
    $scope.hosts = []
    $scope.images = []

    $scope.selectedService;

    var keep = Keep()
    var stop;

    $scope.refreshHosts = function(){
      var deferred = $q.defer();

      keep.getHosts().success(function(data){
        _.each(data.hosts, function(elem){
          // is host present if yes -> update status
          var isHost = _.find($scope.hosts, function(e){ return e.name == elem.name })

          if (!isHost || isHost.length == 0){
            $scope.hosts.push(
              _.extend(elem, {
                selected: false,
                containers: 0,
                instace_numbers: 0,
                port_start: 0,
                port_end: 0
              })
            )
          } else {
            isHost.alive = elem.alive
          }
        })
        deferred.resolve()
      })

      return deferred.promise;
    }

    $scope.refreshHosts().then(function(){

      keep.getAvailableImages().success(function(data){
        $scope.images = data.services
        $scope.viewLoading = false
      })

      stop = $interval(function(){
        $scope.refreshHosts()
      }, 10000)
    })

    $scope.save= function(service){
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
