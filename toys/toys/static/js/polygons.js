/** @jsx React.DOM */
var RD = React.DOM;

var PolygonStorage = function(state) {
    var storage = BaseStorage( {
        'url':'',
        'listeners': [],
        'id_map': {},
        'number': 1,
        'rows': [],
        'cells': []
    });
    $.extend( storage, state || {});
    $.extend( storage, {
        'set_number': function( number ) {
            storage.number = number;
            storage.update();
        }
    });
    return storage;
};


var POLYGON_NAMES = {
    1: 'point',
    2: 'line',
    3: 'triangle/trigon',
    4: 'square/diamond/tetragon',
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

var PolygonRender = React.createClass( {
    componentWillMount: function() {
        this.props.store.listen( this.setState.bind(this) );
    },
    render: function() {
        var self = this;
        var store = this.props.store;
        var number = store.number;
        var points = [];
        if (number == 1) {
            points = [
                [.01,.01],
                [.01,-.01],
                [-.01,-.01],
                [-.01,.01],
            ];
        } else if (number==2) {
            points = [
                [.01,1],
                [.01,-1],
                [-.01,-1],
                [-.01,1],
            ];
        } else {
            var point;
            var factor = Math.PI * 2;
            for (point=0;point<number;point++) {
                points.push([ 
                    Math.sin( factor * (point/number) + Math.PI),
                    Math.cos( factor * (point/number) + Math.PI)
                ]);
            }
        }
        var point_attr = $.map( points, function(point) {
            return ''+point[0]+','+point[1];
        }).join(' ');
        var label = ''+number;
        if (POLYGON_NAMES[number]) {
            label += ' ('+POLYGON_NAMES[number]+')';
        }
        return RD.div({},
            RD.div({}, label ),
            RD.div({},NumberChoice({
                min:1,
                max:100,
                get_value: function() { return store.number; },
                set_value: store.set_number.bind(store),
                store:this.props.store
            })),
            RD.svg({
                'className':'polygon',
                'viewBox':"-1.05 -1.05 2.1 2.1",
                'preserveAspectRatio':"xMidYMid slice",
                'height': '400px'
            },
                RD.polygon({
                    'fill':'yellow',
                    'stroke':'black',
                    'strokeWidth': '.01',
                    'points': point_attr,
                })
            )
        );
    }
});


$(document).ready( function() {
    var tree_holder = document.getElementById('polygon-holder');
    var counting_store = PolygonStorage();
    var number_display = React.renderComponent( 
        PolygonRender({
            store: counting_store,
        }),
        tree_holder
    );

});
