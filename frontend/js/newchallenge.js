var app=angular.module('challengeapp',[]);

app.controller('challengecontroller',function($scope,$http){

$scope.theEditor;
  ClassicEditor
            .create( document.querySelector( '#editor' ) ).
      then( editor => {
          $scope.theEditor = editor;
          $('.ck-editor__editable').attr('min-height','400px'); // Save for later use.
    } );
$scope.uploadedFileImg = function(element) {
     $scope.$apply(function($scope) {
       $scope.filesImg = element.files;
     });
}
$scope.uploadedFileSup = function(element) {
     $scope.$apply(function($scope) {
       $scope.filesSup = element.files;
      });
}


$scope.submit=function(){
var solution=$scope.theEditor.getData();

if(solution=='<p>&nbsp;</p>' && abstract!=''){
$('#loginerror').show();
}
else{
  var fd = new FormData();
  var url = 'http://192.168.43.176:8000/questionPost';
  var data ={
  'title':$('#main_question').val(),
  'description':$('#description').val(),
  'category':'1',
  'deliverables':solution,
  'first_prize':$('#first_prize').val(),
  'second_prize':$('#second_prize').val(),
  'third_prize':$('#third_prize').val(),
  'total_prize':parseInt($('#first_prize').val())+parseInt($('#second_prize').val())+parseInt($('#third_prize').val()),
  "final_date":$("#final_date").val(),
  'user_token':localStorage.getItem('token')
 };
 if($scope.filesSup==undefined){
  data['file']='None';
 }else{
  fd.append('file',$scope.filesSup[0]);
 }
 fd.append('image_file',$scope.filesImg[0]);

 //sample data

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
  if(response.data.message=='Question Inserted'){
    $('#loginerror').show();
  $('#loginerrorspan').css('color','#388E3C');
    $('#loginerrorspan').text('Submitted successfully');
    setTimeout(function ()
        {
        window.location.href = "mychallenge.html"; //will redirect to your blog page (an ex: blog.html)
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
});
