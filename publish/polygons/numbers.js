var numbersApp = angular.module('NumbersApp', []);

numbersApp.controller( 'NumberController', function( $scope ) {
    var rows = [];
    var cells = [];
    var names = {
        1: 'point',
        2: 'line',
        3: 'triangle/trigon',
        4: 'diamond/tetragon',
        5: 'pentagon',
        6: 'hexagon',
        7: 'septagon/heptagon',
        8: 'octagon',
        9: 'nonagon/enneagon',
        10: 'decagon',
        11: 'undecagon/hendecagon',
        12: 'dodecagon',
        13: 'tridecagon',
        14: 'tetradecagon',
        15: 'pendedecagon',
        16: 'hexdecagon',
        17: 'heptdecagon',
        18: 'octdecagon',
        19: 'enneadecagon',
        20: 'icosagon'
    };
    var row_obj, cell;
    for (row=0; row < 2; row=row+1) {
        row_obj = [];
        for (col=0;col < 10;col++) {
            var number = 1 + col + (10*row)
            var cell = {
                'number': number,
                'row': row,
                'col': col,
                'equation': ' ',
                'square': false,
                'multiple': false,
                'selected': false,
                'factor': false,
                'name': names[number],
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
    $scope.on_number( cells[0] );
});
