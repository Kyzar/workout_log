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

    // get a specific equipment, or all equipment with equipment=all
    this.getEquipment = function(equipment) {
      var result;

      return $http.get('/lookup/equipment?equipment=' + equipment)
        .then(function(response) {
          if (equipment == 'all') {
            result = [];
            angular.forEach(response.data.results, function(obj, i) {
              result.push(obj.name);
            })
          } else {
            result = response.data.results.name;
          }
          return result;

        }, function(response) {
            return $q.reject(response.data);
        });
    }
  });

  // service for getting/creating exercises
  angular.module('WorkoutLogApp')
  .service('ExerciseService', function($http, $q, EquipmentService) {

    // get a specific exercise, or all exercises with exercise=all
    this.getExercise = function(exercise) {
      return $http.get('/lookup/exercise?exercise=' + exercise)
        .then(function(response) {
          return response.data.results;

        }, function(response) {
            return $q.reject(response.data);
        });
    }

    this.createExercise = function(exercise) {
      // TODO: handle missing info

      // check if exercise already in database
      var promise = this.getExercise(exercise.exName);

      promise.then(
        function(data) {
          console.log('exercise already exists!');
        },
        function(error) {
          // TODO: validate input
          $http.post('/create', exercise)
            .success(function(data) {
              return data;
            })
            .error(function(data, status) {
              console.log('failed to create');
              return {
                status: status,
                msg: data
              };
            })
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


  // ------------- Directives ------------- //

  angular.module('WorkoutLogApp')


  // ------------- Controllers ------------- //

  // controller for new entry view
  angular.module('WorkoutLogApp')
  .controller('WorkoutLogController',
    function($scope, EquipmentService, ExerciseService, EntryService) {

    // initialization
    EquipmentService.getEquipment('all')
      .then(function(data) {
        $scope.allEquipment = data;
      });

    $scope.newExercise = {
      exName: '',
      exType: 1,
      equipment: 'none' // default for new exercises
    }

    $scope.createExercise = function() {
      // configure the exercise type
      $scope.newExercise.exType = $scope.newExercise.exType == 1 ? true : false;
      ExerciseService.createExercise($scope.newExercise);
      // reset the modal form
      $scope.newExercise = {
        exName: '',
        exType: 1,
        equipment: 'none'
      }
    }

    $scope.removeExercise = function(exercise) {
      EntryService.removeExercise(exercise);
    }

  });

}());