'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('HostsCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
