
app.directive('googleplace', function() {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, model) {
            var options = {
                types: []
            };
            scope.gPlace = new google.maps.places.Autocomplete(element[0], options);

            google.maps.event.addListener(scope.gPlace, 'place_changed', function() {
                scope.$apply(function() {
                    model.$setViewValue(element.val());                
                });
            });
        }
    };
});

app.directive('datePicker', function(){
    return {
        restrict:'EAC',
         link: function($scope, elm, attrs){
            elm.pickadate({
              max: new Date(),
              onSet: function(context) {
                console.log('Just set stuff:', context)
              }
            })
        }
    }
});

app.directive('timePicker', function(){
    return {
        restrict:'EAC',
         link: function($scope, elm, attrs){
            elm.pickatime({
              interval: 60
            })
        }
    }
});