from django.utils.translation import ugettext_lazy as _
import logging
from annoying.decorators import render_to
from functools import wraps
log = logging.getLogger( __name__ )

def with_title( title ):
    def wrapper(function):
        @wraps(function)
        def with_title_injected(*args, **named):
            result = function(*args, **named)
            try:
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
def countingby( request ):
    return {
    }
@render_to( 'toys/powersten.html' )
@with_title('Powers of Ten')
def powersten( request ):
    return {
    }

from django.utils.translation import ugettext as _
