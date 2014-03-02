#! /usr/bin/env python
"""Build the web-toys directory from templates"""
import os, sys, shutil, glob, json, subprocess
import jinja2
HERE = os.path.abspath( os.path.dirname( __file__ ) )

TEMPLATES = os.path.join( HERE, 'templates' )

def rebuild_audio():
    subprocess.check_call( [
        os.path.join( HERE,'wordlists','generatesounds.py' ),
        '-w',os.path.join( HERE,'wordlists','wl-0.txt' ),
        '-o',os.path.join( HERE,'build','wordlist','sounds'),
    ])

def wordlist1():
    all = {
        'wordlists': [],
    }
    for wordlist in sorted(glob.glob( os.path.join( HERE,'wordlists','wl-*.txt'))):
        words = [x.strip() for x in open( wordlist ).read().splitlines() if x.strip()]
        name = os.path.basename(wordlist)
        all['wordlists'].append( {
            'words': words,
            'name': os.path.splitext(os.path.basename(name))[0],
        })
    directory = os.path.join( HERE, 'build','wordlist' )
    if not os.path.exists( directory ):
        os.makedirs( directory )
    content = 'WORDLIST = '+json.dumps(all)+';'
    open( os.path.join( directory,'wordlists.json' ), 'w').write( content )

def generate_build( source=os.path.join( HERE, 'publish' ), target=os.path.join( HERE, 'build' ) ):
    wordlist1()
    for directory, subdirectories, files in os.walk( source ):
        print 'directory', directory, files
        relative = os.path.relpath( directory, source )
        target_directory = os.path.join( target, relative )
        if not os.path.exists( target_directory ):
            print 'making directory', target_directory
            os.makedirs( target_directory )
            
        loader = jinja2.FileSystemLoader( [directory,TEMPLATES] )
        environment = jinja2.Environment(
            loader = loader,
        )
        for file in files:
            target_file = os.path.join( target_directory, file )
            if file.endswith( '.html' ):
                template = loader.load( environment, file )
                content = template.render( 
                    root_relative = os.path.relpath( source, directory ),
                )
                open( target_file, 'w').write( content )
            else:
                shutil.copy( os.path.join( directory, file ), target_file )

if __name__ == "__main__":
    generate_build()
    
