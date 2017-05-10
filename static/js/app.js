angular.module('myApp', ['ngAnimate'])
	.controller('HomeCtrl', function ($scope, $http, $log) {

		$scope.info = "Hello World";

		$scope.showAdd = true;

		$scope.documents = []
		$scope.summarization = null;

		$http.get('/documents').then(function successCallback(response) {
				$scope.documents = [];
				docs =  response.data.result;
				$log.info("Documents loaded ", docs);
				docs.forEach(function(element) {
					var textDocument = new TextDocument(element.name,element.text);
					$scope.documents.push(textDocument);
				}, this);
  			}, function errorCallback(response) {
    			$log.error("Could not load documents ", response);
 		 });

		 $scope.loadSummarizations = function(){
			$http.get('/summarize').then(function successCallback(response) {
				$scope.summarization = response.data;
				$log.info("Summarization loaded ", response.data);
			}, function errorCallback(response){
				    $scope.summarization = null;
					$log.error("Could not load summarization")
				}
			)

		};

		 $scope.deleteDocument = function (name) {
			 $http.delete('/documents/' + name).then(function successCallback(response) {
			 }, function errorCallback(response) {
				 $scope.summarization = null;
				 $log.error("Could not delete document")
			 });
		 }

	})