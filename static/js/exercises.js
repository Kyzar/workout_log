(function() {
  'use strict';

  angular.module('WorkoutLogApp', [])

  // config angular module to use different binding tags from Jinja tags
  .config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
  }]);

  // ------------- Services/Factories ------------- //

  // service for getting/creating equipment
  angular.module('WorkoutLogApp')
  .service('EquipmentService', function($http, $q) {

    // array of all equipment in db, with none as first
    this.getAllEquipment = function() {
      var allEquipment;
      return $http.get('/lookup/equipment?equipment=all')
        .then(function(response) {
          allEquipment = response.data.results;
          // re-order equipment so it is alphabetical but 'none' is first
          var idOfNone = (function() {
            for (var i=0; i<allEquipment.length; i++) {
              if (allEquipment[i].name === 'none') { return i; }
            }
            throw 'Could not find none option';
          })();
          var none = allEquipment.splice(idOfNone, 1)[0];
          allEquipment.unshift(none);
          return allEquipment;
        });
    }

    // get a specific equipment, or all equipment with equipment=all
    this.getEquipment = function(equipment) {
      return $http.get('/lookup/equipment?equipment=' + equipment)
        .then(function(response) {
          return response.data.results;

        }, function(response) {
            return $q.reject(response.data);
        });
    }
  });

  // service for getting/creating exercises
  angular.module('WorkoutLogApp')
  .service('ExerciseService', function($http, $q, EquipmentService) {
    this.getAllExercises = function() {
      return $http.get('/lookup/exercise?exercise=all')
        .then(function(response) {
          return response.data.results;
        });
    }

    // get a specific exercise, or all exercises with exercise=all
    this.getExercise = function(exercise) {
      return $http.get('/lookup/exercise?exercise=' + exercise)
        .then(function(response) {
          return response.data.results;

        }, function(response, status) {
            return $q.reject(response.data);
        });
    }

    this.createExercise = function(exercise) {
      // TODO: handle missing info/validate input
      return $http.post('/create', exercise)
        .success(function(data) {
          return data;
        })
        .error(function(data, status) {
          console.log('failed to create');
          return {
            status: status,
            msg: data
          };
        });
    }
  });

  // service for managing an entry
  angular.module('WorkoutLogApp')
  .service('EntryService', function($http) {
    // List of strength exercises in current entry
    var exercises = [];

    // TODO: load from json format
    this.loadEntry = function(userId, date) {
      $http.get('entry')
        .success(function(data) {
          exercises = data;
        })
        .error(function(data) {
          alert('No entry for that date');
        });
    }

    this.removeExercise = function(exercise) {
     exercises.splice(exercises.indexOf(exercise), 1);
    }

  });


  // ------------- Controllers ------------- //

  // controller for new entry view
  angular.module('WorkoutLogApp')
  .controller('WorkoutLogController',
    function($scope, EquipmentService, ExerciseService, EntryService) {

    $scope.initializeAddExercise = function() {
      // get all exercises for autocomplete search
      ExerciseService.getAllExercises()
        .then(function(data) {
          $scope.allExercises = data;
          $scope.defaultAddExercise = {
            sets: 0,
            reps: 0,
            weight: 0.0,
            exercise: $scope.allExercises[0]
          }
          $scope.addExercise = angular.copy($scope.defaultAddExercise);
        })
    }

    $scope.initializeCreateExercise = function() {
      if (typeof($scope.allEquipment) === 'undefined') {
        // get all equipment for select options
        EquipmentService.getAllEquipment()
          .then(function(data) {
            $scope.allEquipment = data;

            // set default values for form
            $scope.defaultExercise = {
              exName: '',
              exType: 1,
              equipment: $scope.allEquipment[0] // default to 'none'
            }
            $scope.newExercise = angular.copy($scope.defaultExercise);
          })
      }
    }

    $scope.createExercise = function() {
      // create request object
      var request = {
        exName: $scope.newExercise.exName,
        exType: $scope.newExercise.exType == 1 ? true : false,
        equipmentId: $scope.newExercise.equipment.id
      }

      // check if exercise already in database
      ExerciseService.getExercise(request.exName)
        .then(function(data) {
          alert('exercise already exists!');

        }, function(error) {
          // if not found, proceed to create exercise
          ExerciseService.createExercise(request)
            .then(function(data) {
              $scope.newExercise = angular.copy($scope.defaultExercise);

            }, function(error) {
              alert('exercise failed to be created');
            });
        });
    }

    $scope.removeExercise = function(exercise) {
      EntryService.removeExercise(exercise);
    }

  });

}());