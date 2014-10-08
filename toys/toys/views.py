import logging,  tempfile,  os,  subprocess, shutil, hashlib
from annoying.decorators import render_to
from functools import wraps
from django.core import cache as _cache
from django.http import HttpResponse
from toys import forms
log = logging.getLogger( __name__ )

AUDIO_CACHE = _cache.get_cache('utterances')

def with_title( title ):
    def wrapper(function):
        @wraps(function)
        def with_title_injected(*args, **named):
            result = function(*args, **named)
            try:
                if 'title' not in result:
                    result['title'] = title 
            except Exception:
                pass 
            return result 
        return with_title_injected 
    return wrapper

@render_to( 'toys/frontpage.html' )
def frontpage( request ):
    return {
    }
@render_to( 'toys/countingby.html' )
@with_title('Counting By')
def countingby( request, per_row=None ):
    result = {
        'per_row':per_row, 
    }
    if per_row:
        result['title'] = 'Multiple Factors'
    return result 
@render_to( 'toys/powersten.html' )
@with_title('Powers of Ten')
def powersten( request ):
    return {
    }
@render_to( 'toys/polygons.html' )
@with_title('Polygons')
def polygons( request ):
    return {
    }

@render_to('toys/wordlist.html')
@with_title('Sight Word List')
def wordlist(request):
    from . import sightwords
    return {
        'wordlists':sightwords.WORD_LISTS, 
    }
@render_to('toys/clickfast.html')
@with_title('Click Fast')
def clickfast(request):
    from . import sightwords
    return {
        'wordlists':sightwords.WORD_LISTS, 
    }
@render_to('toys/subwords.html')
@with_title('Sub Words')
def subwords(request):
    return {}


@render_to( 'toys/saywhat.html' )
@with_title('Say What?')
def saywhat( request ):
    if request.GET or request.POST:
        form = forms.GenerateText(request.GET or request.POST)
        if form.is_valid():
            extension = form.cleaned_data.get('format')
            words = form.cleaned_data.get('words')
            words = words[:120]
            key = '%s_%s'%(extension, hashlib.md5(words).hexdigest())
            content = AUDIO_CACHE.get( key )
            if not content:
                temp_dir = tempfile.mkdtemp(prefix='utterance')
                try:
                    temp = os.path.join( temp_dir, 'utterance.wav' )
                    final = os.path.join( temp_dir,  'utterance.%s'%(extension))
                    command = [
                        'espeak',
                            '-a200',
                            '-w', temp,  
                            '-ven-us',
                            '-k5','-s150', '-z', 
                            words, 
                    ]
                    subprocess.check_call(command)
                    if extension == 'mp3':
                        extra_args = []
                    else:
                        extra_args = ['-acodec','libvorbis']
                    if os.path.exists( final ):
                        os.remove( final )
                    subprocess.check_call( [
                        'avconv', '-i', temp] + extra_args + [final],
                    )
                    content = open(final, 'rb').read()
                    AUDIO_CACHE.set( key,  content )
                finally:
                    shutil.rmtree(temp_dir)
            if extension == 'ogg':
                mime_type = 'audio/ogg'
            else:
                mime_type = 'audio/mpeg'
            return HttpResponse(content, content_type=mime_type)
    return {
    }
