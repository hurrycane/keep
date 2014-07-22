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
  'ngSanitize',
  'ui.bootstrap'
])

app.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/views/services/index.html',
      controller: 'IndexServiceCtrl'
    })
    .when('/hosts', {
      templateUrl: 'static/views/hosts.html',
      controller: 'HostsCtrl'
    })
    .when('/services/new', {
      templateUrl: 'static/views/services/new.html',
      controller: 'NewServiceCtrl'
    })
    .otherwise({
      redirectTo: '/'
    });
});

app.run(function($rootScope, $interval, $q, Keep){
  var keep = Keep()

  $rootScope.hosts = {}

  /* Added a new host
   * Removed a host
   * Make a dead host alive
   * Make an alive host dead
   */

  $rootScope.refreshHosts = function(){
    var deferred = $q.defer()

    keep.getHosts().success(function(data){
      // detect changes
      _.each(data.hosts, function(value){
        var hostname = value.name

        if(_.has($rootScope.hosts, hostname)){
          if(value.alive != $rootScope.hosts[hostname]){
            var oldState = $rootScope.hosts[hostname]
            $rootScope.hosts[hostname] = value.alive

            $rootScope.$broadcast('hostStateChanged', hostname, oldState, value.alive)
          }
        } else {
          $rootScope.hosts[hostname] = value.alive
          $rootScope.$broadcast('hostAdded', hostname)
        }
      })

      var toDelete = _.difference(
        _.keys($rootScope.hosts),
        _.map(data.hosts, function(e){ return e.name })
      )

      _.each(toDelete, function(hostname){
        delete $rootScope.hosts[hostname]
        $rootScope.$broadcast('hostRemoved', hostname)
      })

      deferred.resolve()
    })

    return deferred.promise;
  }

  $interval(function(){
    $rootScope.refreshHosts()
  }, 5000)

})
