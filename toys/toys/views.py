from django.utils.translation import ugettext_lazy as _
import logging
from annoying.decorators import render_to
log = logging.getLogger( __name__ )

@render_to( 'toys/frontpage.html' )
def frontpage( request ):
    return {
    }
@render_to( 'toys/countingby.html' )
def countingby( request ):
    return {
    }

from django.utils.translation import ugettext as _
