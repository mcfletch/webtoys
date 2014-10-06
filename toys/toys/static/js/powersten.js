/** @jsx React.DOM */
var RD = React.DOM;

var PowerStorage = function(state) {
    var storage = BaseStorage( {
        'url':'',
        'listeners': [],
        'id_map': {},
        'number': 1,
        'power': 10,
        'min_levels': 3,
        'min':1,
        'max':999999999,
        'rows': [],
        'cells': []
    });
    $.extend( storage, state || {});
    $.extend( storage, {
        'set_number': function( number ) {
            storage.number = number;
            storage.update();
        },
        'set_power': function(number) {
            storage.power = number;
            storage.update();
        },
        'baseLog': function( number, base ) {
            return Math.log(number)/Math.log(base);
        },
        'levels': function( number ) {
            number = number || storage.number;
            var required_levels = Math.max(
                storage.min_levels-1,
                Math.floor(storage.baseLog( number || storage.number, storage.power ))
            );
            var i,levels;
            levels = [];
            for (i=required_levels;i>-1;i--) {
                levels.push( Math.pow(storage.power, i) );
            }
            return levels;
        }
    });
    return storage;
};

var NumberChoice = React.createClass( {
    componentWillMount: function() {
        this.props.store.listen( this.setState.bind(this) );
    },
    handleChange: function(event) {
        if (!event) {
            return true;
        }
        if (!event.target) {
            return true;
        }
        if (!event.target.value) {
            return true;
        }
        var updated = event.target.value;
        updated = parseInt(updated);
        if ((! updated) || (! isNaN(updated))) {
            updated = Math.min(updated,this.props.max);
            updated = Math.max(updated,this.props.min);
            this.props.set_value( updated );
        }
        return true;
    },
    render: function() {
        return RD.input({
            'type':'number',
            'value': this.props.get_value(),
            'max': this.props.max,
            'min': this.props.min,
            'onChange': this.handleChange
        });
    }
});

var PowerDisplay = React.createClass( {
    componentWillMount: function() {
        this.props.store.listen( this.setState.bind(this) );
    },
    setter: function(i) {
        /* create a function to set a specific value */
        var operator = function() { this.props.store.set_number(i);};
        return operator;
    },
    rows: function() {
        var self = this;
        var store = this.props.store;
        var number = store.number;
        
        /* we have power-1 rows, cell is "on" if (value / column) > row */
        var row,power;
        var overall = [];
        var levels = store.levels();
        for (row=(store.power-1);row > -1;row--) {
            if (row > 0) {
                overall.push(
                    RD.tr({'children': $.map( levels, function(level,index) {
                        var remainder = number % (level*store.power);
                        var multiple = remainder / level;
                        var class_name = 'power power-'+(levels.length-index);
                        if (multiple >= row) {
                            class_name += ' selected';
                        }
                        return RD.td({'className':class_name} );
                    })})
                );
            } else {
                overall.push(
                    RD.tr({'children': $.map( levels, function(level,index) {
                        var remainder = number % (level*store.power);
                        var multiple = Math.floor(remainder / level);
                        if (level>number) {
                            multiple = ''
                        }
                        return RD.td({},''+(multiple) );
                    })})
                );
            }
        }
        return overall;
    },
    render: function() {
        var storage = this.props.store;
        var input = NumberChoice({ 
            get_value: function() {return storage.number}, 
            set_value:storage.set_number.bind(storage),
            store: storage,
            min: storage.min,
            max: storage.max
        });
        var power = NumberChoice({
            get_value: function() {return storage.power}, 
            set_value:storage.set_power.bind(storage),
            store: storage,
            min: 2,
            max: 24
        });
            
        
        return RD.div({
            'className': 'powers-view',
        },
            RD.div({"className":'number-form'},
                input,
                " in base ",
                power
            ),
            
            RD.table({ 
                'className': 'group-view number-block', 
            },
                RD.thead({},
                    RD.tr({
                        children: $.map(storage.levels(),function(level) {
                            return RD.th({},''+level)
                        })
                    })
                ),
                RD.tbody({ children: this.rows()})
            )
        );
    }
});

$(document).ready( function() {
    var tree_holder = document.getElementById('powers-ten-holder');
    var power_store = PowerStorage();
    var number_display = React.renderComponent( 
        PowerDisplay({
            store: power_store
        }),
        tree_holder
    );

});
