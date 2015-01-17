(function() {
  'use strict';

  angular.module('WorkoutLogApp', ['autocomplete'])

  // config angular module to use different binding tags from Jinja tags
  .config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);

  // ------------- Services/Factories ------------- //

  /**
  * Service for getting and creating exercises
  */
  angular.module('WorkoutLogApp')
  .service('ExerciseService', function($http, $q) {

    // get all exercise objects in db
    this.getAllExercises = function() {
      return $http.get('/lookup/exercise?exercise=all')
        .then(function(response) {
          return response.data.results;
        });
    }

    // get a specific exercise by name
    this.getExerciseByName = function(exercise) {
      return $http.get('/lookup/exercise?exercise=' + exercise)
        .then(function(response) {
          return response.data.results;

        }, function(response, status) {
            return $q.reject(response.data);
        });
    }

    // create exercise object in db
    this.createExercise = function(exercise) {
      // TODO: handle missing info/validate input
      return $http.post('/create', exercise)
        .success(function(data) {
          return data;
        })
        .error(function(data, status) {
          return { status: status, msg: data };
        });
    }
  });


  /**
  * Service for managing entries
  *
  * Allows retrieving an entry by date, adding and removing
  * exercises from entry, and saving changes to database.
  */
  angular.module('WorkoutLogApp')
  .service('EntryService', function($http) {

    // empty new entry
    var createEntry = function() {
      return {
        strExercises : [],
        cardioExercises : []
      }
    }

    var entry = createEntry();

    this.getCurrentEntry = function() {
      return entry;
    }

    // TODO: load from json format, how to pass userId safely?
    this.loadEntry = function(userId, date) {
      return $http.get('/lookup/entry?date=' + date)
        .then(function(data) { entry = data; });
    }

    this.addExercise = function(row, type) {
      var exercises = type === 'strength' ? entry.strExercises : entry.cardioExercises;
      exercises.push(row);
    }

    this.removeExercise = function(row, type) {
      var exercises = type === 'strength' ? entry.strExercises : entry.cardioExercises;
      angular.forEach(exercises, function(ex, i) {
        if (ex.name === row.name) { exercises.splice(i), 1 }
      });
    }

    this.saveEntry = function() {
      console.log('entry saved!');
    }

  });


  /**
  * REMOVE LATER: Service for testing things
  */
  angular.module('WorkoutLogApp')
  .service('TestService', function() {
    var testVariable = 1;
    this.testFunc = function() {
      console.log('test service');
    }
  });


  // ------------- Controllers ------------- //

  /**
  * Controller for creating new workout entry
  */
  angular.module('WorkoutLogApp')
  .controller('NewEntryController',
    ['$scope', 'ExerciseService', 'EntryService', 'TestService',
    function($scope, ExerciseService, EntryService, TestService) {

    $scope.allExercises;
    $scope.exerciseNames;
    $scope.entry = EntryService.getCurrentEntry();
    $scope.addExerciseForm = 'strength'; // default template for add exercise form
    $scope.defaultStrExercise = {
      sets: 0,
      reps: 0,
      weight: 0.0,
      exercise: null
    }
    $scope.defaultCardioExercise = {
      time: 0,
      exercise: null
    }
    // track name of current exercise chosen in add exercise form
    // need to store separately because of autocomplete directive
    $scope.exerciseName = '';
    $scope.addExercise; // user input for adding row to entry

    // initialize data for autocomplete and adding row to entry
    ExerciseService.getAllExercises()
      .then(function(data) {
        // save all exercises and create array of names for autocomplete
        $scope.allExercises = data;
        $scope.exerciseNames = (function() {
          var names = [];
          angular.forEach(data, function(ex) { names.push(ex.name); });
          return names;
        })();

        // set new row to default strength exercise
        $scope.addExercise = angular.copy($scope.defaultStrExercise);
      });

    // effects: adds the current addExercise object to the current entry
    $scope.addExerciseToEntry = function() {
      // finds exercise object with user input
      var ex = $scope.findExercise($scope.exerciseName);
      if (!ex) {
        $scope.addExercise.exercise = ex;
        EntryService.addExercise($scope.addExercise, $scope.addExerciseForm);
      } else {
        alert('Could not find exercise!');
      }
    }

    // requires: row object of current entry, type of exercise for row
    // effects: removes the row object from current entry
    $scope.removeExerciseFromEntry = function(row, type) {
      EntryService.removeExercise(row, type);
    }

    // requires: name of exercise
    // returns: exercise object from allExercises array
    $scope.findExercise = function(name) {
      for (var i=0; i<$scope.allExercises.length; i++) {
        if ($scope.allExercises[i].name === name) {
          return $scope.allExercises[i];
        }
      }
    }

  }]);


  // ------------- Directives ------------- //
  angular.module('WorkoutLogApp')
  .directive('templateSwitch', function() {
    return {
      link: function(scope, element, attrs) {
        // watch exerciseName to see what type of form to show
        scope.$watch('exerciseName', function(newVal) {
          // can't set the form until exercises are loaded
          if (scope.allExercises) {
            var ex = scope.findExercise(scope.exerciseName);
            if (ex) { scope.addExerciseForm = ex.exerciseType; }
          }
        });
      }
    }
  });

}());