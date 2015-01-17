  // DEPRECATED FOR NOW: service for getting/creating equipment
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

    // get a specific equipment
    this.getEquipment = function(equipment) {
      return $http.get('/lookup/equipment?equipment=' + equipment)
        .then(function(response) {
          return response.data.results;

        }, function(response) {
            return $q.reject(response.data);
        });
    }
  });

    // DEPRECATED FOR NOW
    $scope.initializeCreateExercise = function() {
      if (typeof($scope.allEquipment) === 'undefined') {
        // get all equipment for select options
        EquipmentService.getAllEquipment()
          .then(function(data) {
            $scope.allEquipment = data;

            // set default values for form
            $scope.defaultExercise = {
              name: '',
              exType: 1,
              equipment: $scope.allEquipment[0] // default to 'none'
            }
            $scope.newExercise = angular.copy($scope.defaultExercise);
          })
      }
    }

    // DEPRECATED FOR NOW
    $scope.createExercise = function() {
      // create request object
      var request = {
        name: $scope.newExercise.name,
        exType: $scope.newExercise.exType == 1 ? true : false,
        equipmentId: $scope.newExercise.equipment.id
      }

      // check if exercise already in database
      ExerciseService.getExerciseByName(request.name)
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