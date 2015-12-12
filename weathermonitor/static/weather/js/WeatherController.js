app.controller("WeatherCtrl",function($scope, $state, 
    $timeout, APIService, $log) {

    $scope.observations = []
    function fetchData(stationId,params){
        var end_point = "/api/stations/"+stationId+"/plot/graph"

        APIService.getRequest(end_point, params, null)
        .success(function(data) {
            $log.log(data)
            buid_graph(data.hours, data.values, data.weather_parameter)
        }).error(function(data){
            alert(JSON.stringify(data))
            $log.error(data)
        });
    }

    $scope.plot_graph = function(){
        var stationId = $scope.payload.station.id
        var params = {}
        params.start_hour = $scope.payload.start_hour
        params.end_hour = $scope.payload.end_hour
        params.weather_parameter = $scope.payload.parameter.name
        params.date = get_formatted_date()

        fetchData(stationId,params)
    }

    function  get_formatted_date(){
        var dateobj = new Date($scope.payload.date);
        var dd = dateobj.getDate();
        var mm = dateobj.getMonth()+1; //January is 0!
        var yyyy = dateobj.getFullYear();
        if(dd<10) {
            dd='0'+dd
        } 

        if(mm<10) {
            mm='0'+mm
        } 
        formatted_date = yyyy+''+mm+''+dd
        return formatted_date
    }

    $scope.stations = []
    $scope.payload = {}    

    $scope.setup = function(){
        var end_point = "/api/stations"
        APIService.getRequest(end_point, null, null)
        .success(function(data) {
            for (var i = 0; i < data.stations.length; i++) {
              $scope.stations.push(data.stations[i])
            };
            $scope.payload.station = $scope.stations[0]
            $scope.weather_parameters = data.weather_parameters
            $scope.payload.parameter = $scope.weather_parameters[0]
        }).error(function(data){
            alert(JSON.stringify(data))
        });
    }

    function buid_graph(labels, data, weather_parameter){
        $scope.labels = labels
        $scope.data = [
            data
        ]
        if ( weather_parameter === "temperature"){
            $scope.series = ['Temperature in Celsius, Time in 24 hours format'];
        }
        else if ( weather_parameter === "humidity"){
            $scope.series = ['Humidity in cubic meter volume, Time in 24 hours format'];
        }
        else if ( weather_parameter === "pressure"){
            $scope.series = ['Pressure in Newton, Time in 24 hours format '];
        }
        
    }
    
    $scope.gPlace;
    $scope.place = {}
    $scope.AddNewStation = function(){
        var el = document.getElementById("addStation");
        console.log($scope.place)
        var end_point = "/api/stations/"
        var payload = { place:$scope.place.name}
        APIService.postRequest(end_point, payload, null)
        .success(function(data) {
            $scope.stations.push(data.station)
            // dont mix jquery in controller
            $('#addStation').modal('hide')
            $timeout(function(){
                alert("new station added")
            },100)
        }).error(function(data){
            alert(JSON.stringify(data))
            $log.error(data)
        });
    }

});