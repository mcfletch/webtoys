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
    $scope.rows = rows;
    $scope.cells = cells;
    var clear_equations = function() {
        $.map( cells, function( cell ) { 
            cell.equation = ' '; 
            cell.square = false;
            cell.selected = false;
            cell.factor = false;
            cell.multiple = false;
        } );
    };
    $scope.on_number = function( cell ) {
        clear_equations();
        $.map( cells, function( test_cell ) {
            var test_number = test_cell.number;
            var number = cell.number;
            var other;
            if (test_number == number) {
                test_cell.selected = true;
            } else if (test_number % number == 0) {
                test_cell.multiple = true;
                other = test_number/number;
                if (other == number) {
                    test_cell.square = true;
                }
                test_cell.equation = ''+number+' x '+other+' = '+test_number;
            } else if (is_integer( number / test_number)) {
                test_cell.factor = true;
                other = number/test_number;
                if (other == test_number) {
                    test_cell.square = true;
                }
                test_cell.equation= ''+test_number+' x '+other+' = '+number;
            }
        });
    };
});
