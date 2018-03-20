var app=angular.module('contestapp',['ngSanitize','ui.bootstrap']);

app.controller('contestcontroller',function($scope,$http){
  //$('#myModal').modal('show');
  $scope.checkIfLoggedIn=function(){
    if (localStorage.getItem("token") === null) {
      return false;
    }
    else{
      return true;
    }
  };
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getAnswerOfUser',
    crossDomain:true,
    data    :$.param({'question_id':localStorage.getItem('question_id'),'user_token':localStorage.getItem('token')}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
    //alert(JSON.stringify(response));
      $scope.submission=response.data.message;
if($scope.submission!='No Answer Exists'){
  $('#abstract').val($scope.submission.abstract);
  $scope.theEditor.setData($scope.submission.solution);

      //alert(JSON.stringify(response.data.message));
    }
  });
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getQuestionDetails',
    crossDomain:true,
    data    :$.param({'question_id':localStorage.getItem('question_id')}) ,
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
  }).then(function (response) {
      $scope.quesdetails=response.data.message;

      //alert(JSON.stringify(response.data.message));
  });
$scope.theEditor;
  ClassicEditor
            .create( document.querySelector( '#editor' ) ).
      then( editor => {
          $scope.theEditor = editor;
          $('.ck-editor__editable').attr('min-height','400px'); // Save for later use.
    } );
$scope.uploadedFile = function(element) {
     $scope.$apply(function($scope) {
       $scope.files = element.files;
     });
}
$scope.getHoursLeft=function(date){
  //alert(date);
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


$scope.submitfinal=function(){
var abstract=$('#abstract').val();
var solution=$scope.theEditor.getData();

if(solution=='<p>&nbsp;</p>' && abstract!=''){
$('#loginerror').show();
}
else{
  var fd = new FormData();
 var url = 'http://192.168.43.176:8000/answerPost';

 angular.forEach($scope.files,function(file){
 fd.append('file',file);
 });

 //sample data
 var data ={
   'question_id':localStorage.getItem('question_id'),
   'user_token':localStorage.getItem("token"),
   'abstract': abstract,
  'solution' : solution
 };

 fd.append("data", JSON.stringify(data));

 $http.post(url, fd, {
  withCredentials : false,
  headers : {
  'Content-Type' : undefined
  },
  transformRequest : angular.identity
 })
 .then(function(response)
 {
   //alert(response.data.message);

  if(response.data.message=='Answer Inserted'){
    $('#loginerror').show();

  $('#loginerrorspan').css('color','#388E3C');
    $('#loginerrorspan').text('Submitted successfully');
    setTimeout(function ()
        {
        window.location.href = "challenges.html"; //will redirect to your blog page (an ex: blog.html)
        }, 2000);
  }
  else{
    $('#loginerror').show();
    $('#loginerrorspan').css('color',' #f44336');
      $('#loginerrorspan').text("There is some error.Please try again later");
  }
  });
  }
};

$scope.submit=function(){
var abstract=$('#abstract').val();
var solution=$scope.theEditor.getData();

if(solution=='<p>&nbsp;</p>' && abstract!=''){
$('#loginerror').show();
}
else{
  var fd = new FormData();
 var url = 'http://192.168.43.176:8000/answerCheck';

 angular.forEach($scope.files,function(file){
 fd.append('file',file);
 });

 //sample data
 var data ={
   'question_id':localStorage.getItem('question_id'),
   'user_token':localStorage.getItem("token"),
   'abstract': abstract,
  'solution' : solution
 };

 fd.append("data", JSON.stringify(data));

 $http.post(url, fd, {
  withCredentials : false,
  headers : {
  'Content-Type' : undefined
  },
  transformRequest : angular.identity
 })
 .then(function(response)
 {
  // alert(response.data.message);

  $scope.msg=response.data.message;
  $('#submit').hide();
$('.similarity').show();
  });
  }
};
$scope.reload=function(){
  window.location.href='contestpage.html';
};

});
