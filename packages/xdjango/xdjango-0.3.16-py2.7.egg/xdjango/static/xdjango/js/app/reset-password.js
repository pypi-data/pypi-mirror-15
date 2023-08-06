app.controller('ResetPasswordCtrl', ['$scope', 'xdjangoApi', function ($scope, xdjangoApi)
{
    $scope.password = null;
    $scope.confirmPassword = null;
    

    var sendUpdatePassword = function() {
        var url_path_split = window.location.pathname.split("/");
        var user_id = url_path_split[url_path_split.length-2];
        var token = url_path_split[url_path_split.length-1];
        
        xdjangoApi.updatePassword(user_id, $scope.password, token).then(function(response) {
            $scope.password = null;
            $scope.confirmPassword = null;

        }, function (response) {
            // do nothing
        });
    };
    
    $scope.sendUpdatePassword = function() {
        sendUpdatePassword();
    };

}]);