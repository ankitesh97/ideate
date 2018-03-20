var app=angular.module('loginapp',['ngCookies']);

app.controller('logincontroller',function($scope, $window, $cookieStore){
  $scope.checkIfLoggedIn=function(){
    if (localStorage.getItem("token") === null) {
      return false;
    }
    else{
      return true;
    }
  };
(function ($) {
    "use strict";


    /*==================================================================
    [ Validate ]*/
    var input = $('.validate-input .input100');

    $('.validate-form').on('submit',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if(validate(input[i]) == false){
                showValidate(input[i]);
                check=false;
            }
        }
        if (check==true)
        {
          var emailid=$('#emailid').val();
          var password=$('#password').val();
          //var password = CryptoJS.SHA256(password);

        $.post('http://192.168.43.176:8000/login',{user_name:emailid,password:password},function (data)
  			{

              var response=JSON.parse(data);
              //alert(data);
  	      		if(response.message=='Username / Password seems to be incorrect')
  	      {
  	      			$('#loginerror').show();
  	     			$('#loginerrorspan').css('color',' #f44336');

  	      			$('#loginerrorspan').text("Username/password incorrect");
  				}
  				else if(response.message=='Successfully Logged in')
  				{

            localStorage.setItem("token", response.token);
            localStorage.setItem("type",response.type);
            //alert(response.type);
  					$('#loginerror').show();
  					$('#loginerrorspan').css('color','#388E3C');
            $('#loginerrorspan').text('Successfully logged in');

          //  localStorage.setItem("sessId", response.sessId);
            if(response.type== 'b2b57bd11b4438cb060753bd6acd06a5'){
        			setTimeout(function ()
                  {
                  window.location.href = "challenges.html"; //will redirect to your blog page (an ex: blog.html)
                  }, 2000);
            }
            else if(response.type=='8f564c11846a64f94a2d4931d372cc8b'){
              setTimeout(function ()
                  {
                  window.location.href = "mychallenge.html"; //will redirect to your blog page (an ex: blog.html)
                  }, 2000);
            }
  				}
  			});
      }
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
        });
    });

    function validate (input) {
        if($(input).attr('type') == 'email' || $(input).attr('name') == 'email') {
            if($(input).val().trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/) == null) {
                return false;
            }
        }
        else {
            if($(input).val().trim() == ''){
                return false;
            }
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }



})(jQuery);
});
