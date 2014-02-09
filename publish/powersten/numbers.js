$(document).ready( function() {
    var table = $('.number-block' );
    var body = table.find( 'tbody' );
    var footer = table.find( 'tfoot .number-text');
    var number_entry = $('.choose-number' );
    var row_object;
    var cell_object;
    var shown_digits = 6;
    var i,j;
    for ( i=0; i<9; i++){
        row_object = $('<tr class="blocks"></tr>');
        row_object.data( 'number', 9-i );
        for (j=0; j<shown_digits; j++) {
            cell_object = $('<td class="block"></td>' );
            cell_object.data( 'power', shown_digits-j );
            cell_object.data( 'value', 9-i );
            row_object.append( cell_object );
        }
        body.append( row_object );
    }
    for (j=0; j<shown_digits; j++) {
        cell_object = $('<td class="block"></td>' );
        cell_object.data( 'power', shown_digits-j );
        cell_object.text( '' + (shown_digits-j));
        footer.append( cell_object );
    }
    var select_number = function( number ) {
        var representation = '         ' + number;
        representation = representation.slice( -shown_digits );
        
        $('.blocks .block' ).each( function() {
            var cell_object = $(this);
            var digit = cell_object.data( 'value' );
            var power = cell_object.data( 'power' );
            var value_digit = representation[shown_digits-power];
            if (value_digit !== ' ') {
                var value = parseInt( value_digit );
                if (value >= digit) {
                    cell_object.addClass( 'selected' );
                } else {
                    cell_object.removeClass( 'selected' );
                }
            } else {
                cell_object.removeClass( 'selected' );
            }
        });
        footer.find( 'td' ).each( function() {
            var cell_object = $(this);
            var power = cell_object.data( 'power' );
            var value_digit = representation[shown_digits-power];
            cell_object.text( value_digit );
        });
    };
    number_entry.change( function() {
        var value = parseInt( number_entry.prop('value'));
        if (! isNaN( value )) {
            select_number( value );
        }
    });
    select_number( 1 );
});
