var app=angular.module('mychallengeapp',[]);

app.controller('mychallengecontroller',function($scope,$http){
	$http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getQuestionsTitles',
    crossDomain:true,
    data    :$.param({'user_token':localStorage.getItem('token')}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
      // alert(JSON.stringify(response.data.message["questions_title"]));
  	   $scope.questitles=response.data.message["questions_title"];
      // =response.data.message;
  });
	$scope.goToQuestion=function(qid){
		localStorage.setItem('qid',qid);
		window.location.href='admin-viewsubmission.html';
	};
});
