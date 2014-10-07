;
$.play_word = function(word) {
    var use_ogg = ((new Audio()).canPlayType("audio/ogg; codecs=vorbis") === 'probably');
    /* play the word, relying on pre-built sound-files in the local directory */
    var suffix,source;
    if (use_ogg) {
        suffix = '.ogg';
    } else {
        suffix = '.mp3';
    }
    source = 'sounds/'+word+suffix;
    if (false) {
        var audio = $('<audio buffer="auto"></audio>');
        audio.attr( 'src',source); 
        $('body').append( audio );
    } else {
        var node = new Audio( source );
        node.play();
    }
};
