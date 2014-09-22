try:
    from django.contrib import admin
except ImportError, err:
    admin = None 
else:
    from toys import models 

#    class toysAdmin( admin.ModelAdmin ):
#        """Admin class"""
#    admin.site.register( models.toys, toysAdmin )
