'use strict';

/**
 * @ngdoc overview
 * @name keepUiApp
 * @description
 * # keepUiApp
 *
 * Main module of the application.
 */
var app = angular.module('keepUiApp', [
  'ngRoute',
  'ngResource',
  'ngSanitize'
])

app.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/views/index.html',
      controller: 'ServiceCtrl'
    })
    .when('/hosts', {
      templateUrl: 'static/views/hosts.html',
      controller: 'HostsCtrl'
    })
    .when('/deploy', {
      templateUrl: 'static/views/deploy.html',
      controller: 'DeployCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
});
