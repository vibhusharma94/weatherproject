
var app = angular.module('app', ['ui.router','chart.js']);

app.config(function($stateProvider, $urlRouterProvider, ChartJsProvider) {
    
    $urlRouterProvider.otherwise('/home');
    
    $stateProvider
        
        .state('home', {
            url: '/home',
            templateUrl: '/static/weather/partial/weather.html',
            controller: 'WeatherCtrl'
        })

    ChartJsProvider.setOptions({
      colours: ['#FF5252', '#FF8A80'],
      responsive: true
    });
    // Configure all line charts
    ChartJsProvider.setOptions('Line', {
      datasetFill: false
    });
        
});

app.constant('API_HOST', 'http://127.0.0.1:8000')

