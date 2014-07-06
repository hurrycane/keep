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
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
