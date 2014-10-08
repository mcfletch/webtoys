from django.utils.translation import ugettext_lazy as _
import logging
from django import forms
from django.forms import widgets
from django.core import validators
from django.conf import settings

log = logging.getLogger( __name__ )

class GenerateText(forms.Form):
    words = forms.CharField(
        required = True, 
        validators = [
        ], 
    )
    format = forms.ChoiceField(
        choices = [
            ('mp3', 'MP3'), 
            ('ogg', 'OGG Vorbis'), 
        ], 
        widget = widgets.HiddenInput(), 
    )
