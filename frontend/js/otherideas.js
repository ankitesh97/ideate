var app=angular.module('otherideasapp',[]);

app.controller('otherideascontroller',function($scope,$http){
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getDepartments'
  }).then(function (response) {
    //alert(JSON.stringify(response));
    $scope.departments = response.data.message.departments;
    //$scope.challenges_copy = response.data.message.questions;
    //alert(JSON.stringify($scope.challenges));
});
  $scope.theEditor;
    ClassicEditor
              .create( document.querySelector( '#editor' ) ).
        then( editor => {
            $scope.theEditor = editor;
            $('.ck-editor__editable').attr('min-height','400px'); // Save for later use.
      } );
      $scope.checkIfLoggedIn=function(){
        if (localStorage.getItem("token") === null) {
          return false;
        }
        else{
          return true;
        }
      };
      $scope.uploadedFile = function(element) {
           $scope.$apply(function($scope) {
             $scope.files = element.files;
           });
      };
      $scope.submit=function(){
      var abstract=$('#abstract').val();
      var solution=$scope.theEditor.getData();
      var department=$('#department').val();
    //  alert(department);
      if(solution=='<p>&nbsp;</p>' && abstract!=''){
      $('#loginerror').show();
      }
      else{
        $http({
          method  : 'POST',
          url     : 'http://192.168.43.176:8000/addUniqueSolution',
          data    :$.param({'user_token':localStorage.getItem('token'),'solution_abstract':abstract,'solution_solution':solution,'solution_department':department}) ,
          headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object

        }).then(function(response)
       {
         //alert(response.data.message);
        if(response.data.message=='Solution Inserted'){
          $('#loginerror').show();

        $('#loginerrorspan').css('color','#388E3C');
          $('#loginerrorspan').text('Submitted successfully');
          setTimeout(function ()
              {
              window.location.href = "index.html"; //will redirect to your blog page (an ex: blog.html)
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
