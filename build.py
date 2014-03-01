#! /usr/bin/env python
"""Build the web-toys directory from templates"""
import os, sys, shutil
import jinja2
HERE = os.path.abspath( os.path.dirname( __file__ ) )

TEMPLATES = os.path.join( HERE, 'templates' )

def generate_build( source=os.path.join( HERE, 'publish' ), target=os.path.join( HERE, 'build' ) ):
    for directory, subdirectories, files in os.walk( source ):
        print 'directory', directory, files
        relative = os.path.relpath( directory, source )
        target_directory = os.path.join( target, relative )
        if not os.path.exists( target_directory ):
            print 'making directory', target_directory
            os.makedirs( target_directory )
            
        loader = jinja2.FileSystemLoader( [directory,TEMPLATES] )
        environment = jinja2.Environment(
            loader = loader
        )
        for file in files:
            target_file = os.path.join( target_directory, file )
            if file.endswith( '.html' ):
                template = loader.load( environment, file )
                content = template.render( )
                open( target_file, 'w').write( content )
            else:
                shutil.copy( os.path.join( directory, file ), target_file )

if __name__ == "__main__":
    generate_build()
    
