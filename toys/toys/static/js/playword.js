;
$.play_word = function(value,base_url) {
    var use_ogg = ((new Audio()).canPlayType("audio/ogg; codecs=vorbis") === 'probably');
    /* play the word, relying on pre-built sound-files in the local directory */
    var suffix,source;
    if (use_ogg) {
        format = 'ogg';
    } else {
        suffix = 'mp3';
    }
    var final_url = base_url+'?words='+encodeURIComponent(value)+'&format='+format;
    var node = new Audio( final_url );
    node.play();
};
