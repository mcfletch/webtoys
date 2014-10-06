var BaseStorage = function( state ) {
    var storage = $.extend( {
        'url':'',
        'getting': false,
        'listeners': []
    }, state || {} );
    $.extend( storage, {
        get: function() {
            if (!storage.url) {
                /*console.log( 'Warning: no url specified' );*/
                return;
            }
            if (!storage.getting) {
                console.info( 'Getting: '+ storage.url );
                storage.getting = true;
                return $.ajax( {
                    url: storage.url,
                    dataType: 'json',
                    success: function( data ) {
                        storage.getting = false;
                        if (data.success) {
                            storage.set(data);
                        } else {
                            console.log( 'Error loading data '+data.error );
                        }
                    },
                    error: function( xhr, status, err ) {
                        console.error( "Unable to load data: "+err );
                        storage.getting = false;
                    }
                });
            }
        },
        update: function() {
            var to_remove = [];
            $.map( storage.listeners, function(listener) {
                try {
                    listener( storage );
                } catch( e ) {
                    /* console.log( 'Listener is gone ', e ); */
                    to_remove.push( listener );
                }
            });
            if (to_remove.length) {
                storage.listeners = $.grep(storage.listeners,function(l) {
                    return to_remove.indexOf( l ) == -1;
                });
            }
        },
        listen: function( listener ) {
            storage.listeners.push( listener );
        },
        set: function(state) {
            $.extend( storage, state );
            storage.ensure_keys();
            storage.update();
        }
    });
    return storage;
};
