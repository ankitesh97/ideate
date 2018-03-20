var app=angular.module('viewideasapp',['ngMaterial','ngSanitize']);

app.controller('viewideascontroller',function($scope,$http, $mdDialog){
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/getUniqueSolutions'
  }).then(function (response) {
    //alert(JSON.stringify(response));
      $scope.solutions=response.data.message.solutions;

  });
      $scope.checkIfLoggedIn=function(){
        if (localStorage.getItem("token") === null) {
          return false;
        }
        else{
          return true;
        }
      };
      $scope.upvotes=function(solution_id){
        $http({
          method  : 'POST',
          url     : 'http://192.168.43.176:8000/upvoteSolution',
          crossDomain:true,
          data    :$.param({'solution_id':solution_id}) ,
          headers : {'Content-Type': 'application/x-www-form-urlencoded'}//forms user object
        }).then(function (response) {
          //alert(JSON.stringify(response));
            $scope.submission=response.data.message;
      if($scope.submission=='Upvoted Successfully'){
        var p='#'+solution_id;
        $(p).show();
        var b='#button'+solution_id;
        $(b).hide();
        window.location.href='viewideas.html';
        //$('#abstract').val($scope.submission.abstract);
        //$scope.theEditor.setData($scope.submission.solution);
            //alert(JSON.stringify(response.data.message));
          }
        });

      };
      $scope.showModal = function(ev,user_image,user_name,solution_abstract,solution_solution,solution_upvotes,solution_id) {
        //alert(user_image);
        $scope.image=user_image;
        $scope.name=user_name;
        $scope.abstract=solution_abstract;
        $scope.solution=solution_solution;
        $scope.noofupvotes=solution_upvotes;

        $scope.id=solution_id;
      //  $scope.heard='hiihihih';
          $mdDialog.show({

            contentElement: '#myDialog',
        parent: angular.element(document.body),
        targetEvent: ev,
        clickOutsideToClose: true// Only for -xs, -sm breakpoints.
          });
        };
        function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };

    $scope.cancel = function() {
      $mdDialog.cancel();
    };

    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };

  }
});
