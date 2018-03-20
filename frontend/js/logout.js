var app = angular.module('logout_app',[]);
app.controller('logout_controller', function($scope,$http){

//alert(localStorage.getItem('token'));
  $http({
    method  : 'POST',
    url     : 'http://192.168.43.176:8000/logout',
    data: $.param({'user_token':  localStorage.getItem('token')}),
    headers : {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(function (response) {
    localStorage.removeItem('token');
    localStorage.removeItem('user_name');
    localStorage.removeItem('type');
      window.location.href = "index.html";
  });
});
