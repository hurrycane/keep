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
      Service: $resource("/1.0/services", {}, {
        index: {
          method: 'GET',
          params: {},
          headers: {
            'Content-Type': 'application/json'
          }
        }
      })
    }
  }

});
