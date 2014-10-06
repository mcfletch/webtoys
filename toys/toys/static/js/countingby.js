/** @jsx React.DOM */
var RD = React.DOM;

var CountingByStorage = function(state) {
    var storage = BaseStorage( {
        'url':'',
        'listeners': [],
        'id_map': {},
        'number': 10,
        'total': 100,
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

var CountingBy = React.createClass( {
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
        var i,cell_classes;
        var overall = [];
        var current = [];
        var number = store.number;
        for (i=1;i<store.total+1;i++) {
            if ((i % number == 1)) {
                overall.push( RD.tr({'className':'number-row','children':current,'align':'top'}) );
                current = [];
            }
            cell_classes = 'cell number ';
            equation = "";
            if (number == i) {
                cell_classes += 'selected ';
            } else if (i%number == 0) {
                cell_classes += 'multiple ';
                equation += ''+number+'\u2715'+(i/number);
            } else if (number%i == 0) {
                cell_classes += 'factor ';
                equation += ''+i+'\u2715'+(number/i);
            } else {
                if (i-number > 0) {
                    equation += ''+(i-number)+' \u2795 '+number;
                }
            }
            current.push( RD.td({
                'className': cell_classes,
                'style': {
                    'width':Math.floor((1/number)*100)+'%'
                },
                onClick: self.setter(i).bind(self)
            }, 
                RD.div({className:"num"},""+i),
                RD.div({className:"equation"},equation)
            ));
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
    var counting_store = CountingByStorage();
    var number_display = React.renderComponent( 
        CountingBy({
            store: counting_store
        }),
        tree_holder
    );

});
