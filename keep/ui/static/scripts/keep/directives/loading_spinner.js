app.directive('loadingSpinner', function() {
  return {
    restrict: 'A',
    replace: true,
    transclude: true,
    scope: {
      loading: '=loadingSpinner'
    },
    templateUrl: '/static/views/directives/loading.html',
    link: function(scope, element, attrs) {
      /*var loadingContainer, spinner;
      spinner = new Spinner().spin();
      loadingContainer = element.find('.loading-spinner')[0];
      return loadingContainer.appendChild(spinner.el);*/
    }
  };
});
