var app=angular.module('signupapp',[]);

app.controller('signupcontroller',function($scope){
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
          var fname=$('#fname').val();
          var lname=$('#lname').val();
          var pnumber=$('#pnumber').val();
          var emailid=$('#emailid').val();
          var password=$('#password').val();
          //var password = CryptoJS.SHA256(password);
        $.post('http://192.168.43.176:8000/register',{first_name:fname,last_name:lname,contact:pnumber,user_name:emailid,password:password},function (data)
  			{

              var response=JSON.parse(data);


  			  if(response.message=='User Inserted')
  				{
  					$('#loginerror').show();
  					          $('#loginerrorspan').css('color','#388E3C');

            $('#loginerrorspan').text('Successfully created an account');

  			setTimeout(function ()
            {
            window.location.href = "index.html"; //will redirect to your blog page (an ex: blog.html)
            }, 2000);

  				}
          else
          {
            $('#loginerror').show();
          $('#loginerrorspan').css('color',' #f44336');

            $('#loginerrorspan').text("Username already exists");
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
