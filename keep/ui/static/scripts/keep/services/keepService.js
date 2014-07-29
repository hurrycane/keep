app.service('Keep', function($resource, $http) {

  return function(){
    return {
      'getHosts': function(){
        return $http({
          method: 'GET',
          url: "/1.0/hosts"
        });
      },
      'getAvailableImages': function(){
        return $http({
          method: 'GET',
          url: "/1.0/available-images"
        });
      },
      'getImageVersions': function(serviceName){
        return $http({
          method: 'GET',
          url: "/1.0/service-versions?service=" + serviceName
        });
      },
      'deployService': function(service, version){
        return $http({
          method: 'POST',
          url: "/1.0/deploy/" + service.id + "?version=" + version
        });
      },
      Service: $resource("/1.0/services/:serviceId", {}, {
        index: {
          method: 'GET',
          params: {},
          headers: {
            'Content-Type': 'application/json'
          }
        },
        update: { method: 'PUT' }
      })
    }
  }

});
