(function() {
  'use strict';

  angular.module('WorkoutLogApp', [])

  // config angular module to use different binding tags from Jinja tags
  .config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }])

  .controller('WorkoutLogController', ['$scope', function($scope, $log) {
    $scope.totalExercises = 1;

    $scope.strExercises = [ {sets: 0, reps: 0, weight: 0, name: ''} ];

    $scope.addExercise = function() {
      $scope.strExercises.push({sets: 0, reps: 0, weight: 0, name: ''});
      $scope.totalExercises ++;
    };


  }])

}());