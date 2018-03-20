

var app = angular.module('challenge_app',[]);
app.controller('challenge_controller', function($scope,$http){
  $scope.checkIfLoggedIn=function(){
    if (localStorage.getItem("token") === null) {
      return false;
    }
    else{
      return true;
    }
  };
  // data = [{"title":"cool man","question_id":"sup", "time":"2018-03-15 22:50:38.206053", "award":10000},{"title":"cool man","question_id":"sup", "time":"2018-03-15 12:50:38.206053", "award":10000},{"title":"cool man","question_id":"sup", "time":"2018-03-15 12:50:38.206053", "award":10000},{"title":"cool man","question_id":"sup", "time":"2018-03-15 12:50:38.206053", "award":10000},{"title":"cool man","question_id":"sup", "time":"2018-03-15 12:50:38.206053", "award":10000}]
  // $scope.challenges = data
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getQuestions'
  }).then(function (response) {
    response_display = JSON.stringify(response);
    //alert(JSON.stringify(response));
    $scope.challenges = response.data.message.questions;
    $scope.challenges_copy = response.data.message.questions;
    //alert(JSON.stringify($scope.challenges));
});

  $scope.goToChallenge=function(questionid){
    localStorage.setItem("question_id", questionid);
    window.location.href = "contestpage.html";

  };
  $scope.getHoursLeft=function(date){
    parts = date.split(/[- :]/);
    endDate =  new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5]);
    currDate = new Date();
    $scope.hours = parseInt((endDate - currDate) / 36e5);
    if($scope.hours<0){
      return "DONE";
    }
    else if($scope.hours==0){
      return "FEW";
    }
    else{
      return $scope.hours;
    }
  };


  $scope.currentState=function(){
    // if($scope)
    if($scope.hours<0){
      return Math.abs($scope.hours)+" hours ago";
    }
    else if($scope.hours==0){
      return "minutes left";
    }
    else{
      return "hours left";
    }
  };

  $scope.getByTheme=function(clicked){
    if(clicked=="All")
      $scope.challenges = $scope.challenges_copy
    else{
      temp = [];
      for(i=0; i<$scope.challenges_copy.length; i++){
        if($scope.challenges_copy[i].category == clicked)
          temp.push($scope.challenges_copy[i])
      }
      $scope.challenges = temp;
    }
    // alert(JSON.stringify($scope.challenges));
    $scope.$apply();
  };

});
