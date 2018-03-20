  var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};
var t= 0 ;
var dict={};
    $( ".btn-send" ).click(function( event ) {
      // alert("IDhar");
      dict[$("#rank").val()]=$("#form-answer-id").html();
      if($("#rank").val()=="1"){
        $("#1_selection").removeClass("glyphicon-remove");
        $("#1_selection").addClass("glyphicon-ok");
      }else if($("#rank").val()=="2"){
        $("#2_selection").removeClass("glyphicon-remove");
        $("#2_selection").addClass("glyphicon-ok");
      }else if($("#rank").val()=="3"){
        $("#3_selection").removeClass("glyphicon-remove");
        $("#3_selection").addClass("glyphicon-ok");
      }else{
        alert("Invalid Rank");
      }
});

var app=angular.module('viewsubmissionapp',['ngSanitize']);

app.controller('viewsubmissioncontroller',function($scope,$http){
    $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getQuestionDetails',
    crossDomain:true,
    data    :$.param({'question_id':localStorage.getItem('qid')}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
      $scope.quesDetails=response.data.message;
  });

  $scope.callFn = function(){
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getAnswersOfQuestion',
    crossDomain:true,
    data    :$.param({'question_id':localStorage.getItem('qid'),'user_token':localStorage.getItem('token')}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
      $scope.answers=response.data.message["answers"];
      $scope.total=response.data.message["answers"].length;
  });
  };
  $scope.callStarFn = function(){
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getStarredAnswersOfQuestion',
    crossDomain:true,
    data    :$.param({'question_id':getUrlParameter('qid'),'user_token':localStorage.getItem('token')}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
      $scope.answers=response.data.message["answers"];
      // alert(JSON.stringify($scope.answers));
  });
  };
  $scope.declareWinner=function(){
    if(!dict.hasOwnProperty('1') && !dict.hasOwnProperty('2') && !dict.hasOwnProperty('3')){
      alert("Select 3 Winners");
      return;
    }
    $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/setWinner',
    crossDomain:true,
    data    :$.param({'user_token':localStorage.getItem('token'),'question_id':getUrlParameter('qid'),'first_prize':dict['1'],'second_prize':dict['2']
      ,'third_prize':dict['3']}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
      // alert(JSON.stringify(response.data.message));
  });
  };
  $scope.getDownloadClass=function(text){
    if(text.toLowerCase()=="None"){
      return "glyphicon glyphicon-download-alt"
    }else{
      return "glyphicon glyphicon-download-alt"
    }
  }
  $scope.getClass= function(someValue){
     if(someValue=="0")
      return "glyphicon star glyphicon-star-empty"
     else
      return "glyphicon star glyphicon-star"
    };
  $scope.pigClicked = function($event){
    // alert($event.currentTarget.id.split("-")[2]);
    $("#form-answer-id").html($event.currentTarget.id.split("-")[2]);
  };
  $scope.starClicked = function($event) {
       var id=$event.currentTarget.id.split('-')[1];
       if($event.currentTarget.classList.contains("glyphicon-star-empty")){
          $event.currentTarget.classList.remove("glyphicon-star-empty");
          $event.currentTarget.classList.add("glyphicon-star");
          $http({
            method  : 'POST',
            url     : 'http://192.168.43.176:8000/starAnswer',
            crossDomain:true,
            data    :$.param({'answer_id':id,'user_token':localStorage.getItem('token')}) ,
            headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
          }).then(function (response) {
              // alert(JSON.stringify(response.data.message));
          });
       }else{
          $event.currentTarget.classList.remove("glyphicon-star");
          $event.currentTarget.classList.add("glyphicon-star-empty");
          $http({
            method  : 'POST',
            url     : 'http://192.168.43.176:8000/deStarAnswer',
            crossDomain:true,
            data    :$.param({'answer_id':id,'user_token':localStorage.getItem('token')}) ,
            headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
          }).then(function (response) {
              // alert(JSON.stringify(response.data.message));
          });
       }
    };

    $(".nav-tabs").click(function(){
      if($(this).hasClass("active")){
        // alert("Here");
        //Nothing
      }else{
        clickedItem= $(this).children().text();
        activeItem= $(".nav-tabs-active").children().text();
        // alert(clickedItem+'---'+activeItem);
        $(".nav-tabs-active").removeClass("active");
        $(".nav-tabs-active").removeClass("nav-tabs-active");
        if($("#nav-tab-starred").hasClass("hide-nav-tab-div")){
            $scope.callStarFn();
            $("#nav-tab-starred").removeClass("hide-nav-tab-div");
            $("#nav-tab-all").addClass("hide-nav-tab-div");
        }else{
            $scope.callFn();
            $("#nav-tab-all").removeClass("hide-nav-tab-div");
            $("#nav-tab-starred").addClass("hide-nav-tab-div");
        }
        $(this).addClass("active");
        $(this).addClass("nav-tabs-active");
      }
    });
  $scope.callFn();
});
