var numbersApp = angular.module('NumbersApp', []);

numbersApp.controller( 'NumberController', function( $scope ) {
    var rows = [];
    var cells = [];
    var row_obj, cell;
    for (row=0; row < 5; row=row+1) {
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
                'factor': false,
                'points': []
            };
            row_obj.push(cell);
            cells.push(cell);
        }
        rows.push( row_obj );
    }
    $scope.rows = rows;
    $scope.cells = cells;
    $scope.on_number = function( cell ) {
        if ($scope.selected) {
            $scope.selected.selected = false;
        }
        $scope.selected = cell;
        cell.selected = true;
        if (! cell.points.length) {
            if (cell.number > 2) {
                var point;
                var factor = Math.PI * 2;
                for (point=0;point<cell.number;point++) {
                    cell.points.push([ 
                        Math.sin( factor * (point/cell.number) + Math.PI),
                        Math.cos( factor * (point/cell.number) + Math.PI)
                    ]);
                }
            }
        }
        if (cell.points.length) {
            var formatted = cell.points.join( ' ' );
            $('.polygon polygon').attr( 'points', formatted );
        } else if (cell.number == 1) {
            $('.polygon polygon').attr( 'points', '.01,.01 .01,-.01 -.01,-.01 -.01,.01' );
        } else if (cell.number == 2) {
            $('.polygon polygon').attr( 'points', '.01,1 .01,-1 -.01,-1 -.01,1' );
        }
    };
});
