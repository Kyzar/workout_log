(function() {
  'use strict';

  angular.module('WorkoutLogApp', [])

  // config angular module to use different binding tags from Jinja tags
  .config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }])

  .controller('WorkoutLogController', ['$scope', function($scope, $log) {

    $scope.strExercises = [];

    $scope.addExercise = function() {
      $scope.strExercises.push({
        sets: $scope.newExerciseSets,
        reps: $scope.newExerciseReps,
        weight: $scope.newExerciseWeight,
        name: $scope.newExerciseName
      });
    };

    $scope.removeExercise = function(exercise) {
      $scope.strExercises.splice($scope.strExercises.indexOf(exercise),1);
    };

  }])

}());