var numbersApp = angular.module('NumbersApp', []);

numbersApp.controller( 'NumberController', function( $scope ) {
    var rows = [];
    var cells = [];
    var row_obj, cell;
    var is_integer = function( number ) {
        if (Math.round( number) == number) {
            return true;
        } else {
            return false;
        }
    };
    for (row=0; row < 10; row=row+1) {
        row_obj = [];
        for (col=0;col < 10;col++) {
            var cell = {
                'number': 1 + col + (10*row),
                'row': row,
                'col': col,
                'equation': ' ',
                'square': false,
                'multiple': false,
                'selected': false,
                'factor': false
            };
            row_obj.push(cell);
            cells.push(cell);
        }
        rows.push( row_obj );
    }
    $scope.base = 10;
    $scope.rows = rows;
    $scope.cells = cells;
    var clear_equations = function() {
        $.map( cells, function( cell ) { 
            cell.equation = ' '; 
            cell.selected = false;
            cell.multiple = false;
        } );
    };
    var restructure = function() {
        var row,col,cell;
        $scope.rows = [];
        $.map( cells, function( cell, index ) {
            if (index % $scope.base == 0) {
                $scope.rows.push( [] );
            }
            $scope.rows[$scope.rows.length-1].push( cell );
        });
    };
    $scope.on_number = function( cell ) {
        $scope.base = cell.number;
        clear_equations();
        restructure();
        $.map( cells, function( test_cell ) {
            var test_number = test_cell.number;
            var number = cell.number;
            var other;
            if (test_number == number) {
                test_cell.selected = true;
            } else if (test_number % number == 0) {
                test_cell.multiple = true;
            }
        });
    };
});
