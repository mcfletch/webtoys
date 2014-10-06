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

from django.utils.translation import ugettext as _
