
var app = angular.module('topsolvers_app',[]);
app.controller('topsolvers_controller', function($scope,$http){
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
    url     : 'http://192.168.43.176:8000/getTopUser'
  }).then(function (response) {
    //alert(JSON.stringify(response));
    $scope.solvers=response.data.message.users;

  });
  $scope.goToUser=function(user_name){
    localStorage.setItem("user_name", user_name);
    window.location.href = "profile.html";

  };
});
