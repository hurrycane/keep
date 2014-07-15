'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('DeployCtrl', function ($scope, $resource) {

    $scope.stages = [
      { name: "Alpha", selected: true},
      { name: "Beta", selected: false },
      { name: "Gamma", selected: false },
      { name: "Prod", selected: false }
    ]

    $scope.hosts = [
      {
        name: "gs4-us-east-1-aws.2o.com",
        selected: false,
        containers: 7,
        instace_numbers: 0,
        port_start: 0,
        port_end: 0
      },
      {
        name: "gs3-us-east-1-aws.2o.com",
        selected: false,
        containers: 8,
        instace_numbers: 0,
        port_start: 0,
        port_end: 0
      }
    ];

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

  });
