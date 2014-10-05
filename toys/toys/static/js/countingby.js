/** @jsx React.DOM */
var RD = React.DOM;

var cell = function(i) {
    return {
        number: i,
        equation: '',
        square: false,
        multiple: false,
        selected: false,
        factor: false
    }
};

var CountingStore = function() {
    var self = {
        number: 10,
        rows: [],
        cells: []
    };
    for (var i=0;i<self.total;i++) {
        self.cells.push( cell(i));
    }
    
    this.number = 10;
    this.total = 100;
    this.cells = [];
    this.rows = [];
    this.set_number = function( number ) {
        this.number = number;
    };
    this.set_number( 10 );
    return this;
};

var CountingBy = React.createClass( {
    rows: function() {
        var self = this;
        var i,cell_classes;
        var overall = [];
        var current = [];
        var number = this.props.store.number;
        for (i=1;i<this.props.store.total+1;i++) {
            if ((i % number == 1)) {
                overall.push( RD.tr({'className':'number-row','children':current}) );
                current = [];
            }
            cell_classes = 'cell ';
            if (number == i) {
                cell_classes += 'selected ';
            } else if (number % i == 0) {
                cell_classes += 'multiple ';
            } else if (i % number == 0) {
                cell_classes += 'factor ';
            }
            current.push( RD.td({
                'className': cell_classes,
                'onClick': function() {
                    self.props.store.number = i;
                }
            }, ""+i));
        }
        if (current.length) {
            overall.push( RD.tr({
                'className':'number-row',
                'children':current
            }) );
        }
        return overall;
    },
    render: function() {
        return RD.table({ 
            'className': 'group-view', 
            children: [RD.tbody({ children: this.rows()})]
        });
        
    }
});

$(document).ready( function() {
    var tree_holder = document.getElementById('counting-by-holder');
    var counting_store = CountingStore();
    var number_display = React.renderComponent( 
        CountingBy({
            store: counting_store
        }),
        tree_holder
    );

});
