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
