app.controller('RequestResetPasswordCtrl', ['$scope', 'xdjangoApi', function ($scope, xdjangoApi)
{
    $scope.email = null;
    

    var sendResetPasswordRequest = function() {

        xdjangoApi.createOneTimeToken($scope.email).then(function(response) {
            $scope.email = null;

        }, function (response) {
            // do nothing
        });
    };
    
    $scope.sendResetPasswordRequest = function() {
        sendResetPasswordRequest();
    };

}]);