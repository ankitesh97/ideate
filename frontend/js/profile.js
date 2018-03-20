
var app = angular.module('profile_app',[]);
app.controller('profile_controller', function($scope,$http){
  $scope.checkIfLoggedIn=function(){
    if (localStorage.getItem("token") === null) {
      return false;
    }
    else{
      return true;
    }
  };
  $scope.div = "profile";
  //localStorage.setItem("token","86f006db7deed78ebadff273ea271f8c");
  // get user profile details
  if (localStorage.getItem("user_name")){
    $http({
    method:'POST',
    url :'http://192.168.43.176:8000/getUserPublicProfile',
    data:$.param({"user_name":localStorage.getItem("user_name")}),
    headers:{'Content-Type':'application/x-www-form-urlencoded'}
    }).then(function (response){
    localStorage.removeItem('user_name');
    //alert(JSON.stringify(response));
    $scope.user_data = response.data.message;
    $scope.user_answers = $scope.user_data.questions;
    $scope.show=false;

  });
  }
  else{
    $http({
    method:'POST',
    url :'http://192.168.43.176:8000/getUserPrivateProfile',
    data:$.param({"user_token":localStorage.getItem("token")}),
    headers:{'Content-Type':'application/x-www-form-urlencoded'}
    }).then(function (response){
    //alert(JSON.stringify(response));
    $scope.user_data = response.data.message;
    $scope.user_answers = $scope.user_data.questions;
    $scope.show=true;
  });
  }



  $scope.onQuestionClick = function(question_id){
    //alert(question_id);

    localStorage.setItem("question_id",question_id);
    window.location.href='contestpage.html';
  };

  $scope.submitBankDetails = function(){
    bank_name = $("#bank_name").val();
    bank_account_no = $("#acc_no").val();
    bank_ifsc_code = $("#ifsc").val();
    aadhar_no = $("#aad").val();
    pancard_no = $("#pan").val();
    $http({
    method:'POST',
    url :'http://192.168.43.176:8000/setUserBankDetails',
    data:$.param({"user_token":localStorage.getItem("token"),"bank_name":bank_name,"bank_account_no":bank_account_no,"bank_ifsc_code":bank_ifsc_code,"aadhar_no":aadhar_no,"pancard_no":pancard_no}),
    headers:{'Content-Type':'application/x-www-form-urlencoded'}
    }).then(function (response){
      //alert("Bank details set");

      location.reload();
  });
  };

  $scope.flipCard = function(click){
    bank_name = $("#bank_name");
    bank_account_no = $("#acc_no");
    bank_ifsc_code = $("#ifsc");
    aadhar_no = $("#aad");
    pancard_no = $("#pan");
    bank_name.val("");
    bank_account_no.val("");
    bank_ifsc_code.val("");
    aadhar_no.val("");
    pancard_no.val("");
    if($scope.div == "profile" && click==1){
      $("#profile").hide();
      $http({
      method:'POST',
      url :'http://192.168.43.176:8000/getUserBankDetails',
      data:$.param({"user_token":localStorage.getItem("token")}),
      headers:{'Content-Type':'application/x-www-form-urlencoded'}
      }).then(function (response){
      bankdet = response.data.message;
      if(bankdet != "Details doesnt exist"){
        bank_name.val(bankdet.bank_name);
        bank_account_no.val(bankdet.bank_account_no);
        bank_ifsc_code.val(bankdet.bank_ifsc_code);
        aadhar_no.val(bankdet.aadhar_no);
        pancard_no.val(bankdet.pancard_no);
      }
  });
      $("#bank").show();
      $scope.div = "bank";
    }
    else if($scope.div == "bank" && click==0){

      $("#bank").hide();
      $("#profile").show();
      $scope.div = "profile";
    }
  }

});
