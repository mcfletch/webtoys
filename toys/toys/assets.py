from django_assets import Bundle, register

css = Bundle(
    'css/site.css',
    filters='yui_css',
    output='css/webtoys-%(version)s.css',
)
register('css_all', css)


