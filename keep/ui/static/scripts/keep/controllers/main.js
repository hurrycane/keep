'use strict';

/**
 * @ngdoc function
 * @name keepUiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the keepUiApp
 */
angular.module('keepUiApp')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
