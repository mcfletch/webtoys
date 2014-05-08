var RD = React.DOM;
var NumberDisplay = React.createClass({
    getInitialState: function() {
        return {
            number:0,
        };
    },
    render: function() {
        var number = this.state.number;
        var number_nodes = [1,2,3,4,5,6,7,8,9,10].map( function(i) {
            var extra = '';
            if (i <= number){
                extra += ' enabled';
            }
            return (
                RD.div( { className: "number number-"+i+extra} )
            );
        });
        return (
            RD.div({className:"number-display",children:number_nodes})
        );
    }
});
$(document).ready( function() {
    var number_display = React.renderComponent( NumberDisplay({
    }), document.getElementById('number-display-holder'));
    var choice = $('.choose-number');
    choice.change( function() {
        var value = parseInt( choice.val());
        number_display.setState({number: value});
        return false;
    });
});
