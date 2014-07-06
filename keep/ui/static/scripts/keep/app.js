'use strict';

/**
 * @ngdoc overview
 * @name keepUiApp
 * @description
 * # keepUiApp
 *
 * Main module of the application.
 */
angular
  .module('keepUiApp', [
    'ngRoute',
    'ngResource',
    'ngSanitize'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'static/views/index.html',
        controller: 'ServiceCtrl'
      })
      .when('/hosts', {
        templateUrl: 'static/views/hosts.html',
        controller: 'HostsCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });

console.log("!")
