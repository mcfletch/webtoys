#! /usr/bin/env python
"""Script to generate .mp3 and .ogg files for a given word-list"""
import os,sys,optparse,tempfile,subprocess

def get_options():
    parser = optparse.OptionParser()
    parser.add_option( 
        '-w','--wordlist', 
        dest='wordlist', 
        default=None, 
        metavar="FILE",
        help="Input word-list file (one word per line)",
    )
    parser.add_option( 
        '-o','--output', 
        dest='output', 
        default=None, 
        metavar="DIRECTORY",
        help="Directory into which to write the .mp3 and .ogg files (default './sounds')",
    )
    return parser 

def main(args=None):
    parser = get_options()
    options,args = parser.parse_args( args )
    if args and not options.wordlist:
        options.wordlist = args[0]
        args = args[1:]
    if args and not options.output:
        options.output = args[0]
        args = args[1:]
    if args:
        return parser.error('Unexpected arguments received: %s'%(args,))
    if not options.wordlist:
        return parser.error('Need an input word-list')
    if not options.output:
        options.output = './sounds'
    words = [
        word for word in [
            x.strip() 
            for x in open( options.wordlist ).read().splitlines()
        ] 
        if word
    ]
    if not os.path.exists( options.output ):
        os.makedirs( options.output )
    for word in words:
        # TODO: validate the filename first...
        base_name = os.path.join(options.output,word )
        target_file = base_name + '.wav'
        command = ['text2wave', '-o', target_file]
        pipe = subprocess.Popen( command, stdin=subprocess.PIPE )
        pipe.communicate( word )
        subprocess.check_call( [
            'avconv', '-i', target_file, base_name+'.mp3'
        ])
        subprocess.check_call( [
            'avconv', '-i', target_file, base_name+'.ogg'
        ])

if __name__ == "__main__":
    main()
