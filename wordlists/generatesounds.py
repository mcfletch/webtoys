#! /usr/bin/env python
"""Script to generate .mp3 and .ogg files for a given word-list

sudo aptitude install festival festvox-us1 festvox-us2 festvox-us3
sudo aptitude install espeak
sudo aptitude install libav-tools

espeak -ven+f4 -k5 -s150 "Click on the word 'a'"
"""
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
    parser.add_option( 
        '-v','--voice', 
        dest='voice', 
        default='en-us', 
        metavar="VOICE",
        help="ESpeak voice to use for the generation (use espeak --voices to see list)",
    )
    parser.add_option(
        '-a', '--audition',
        dest = 'audition',
        action = 'store_true',
        help="Play the playlist through the speaker instead of generating sound files",
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
        if not options.audition:
            target_file = base_name + '.wav'
            if os.path.exists( target_file ):
                os.remove( target_file )
            command = ['espeak','-a200','-w', target_file, '-v%s'%(options.voice,), '-k5','-s150', '-z', repr(word)]
            subprocess.check_call( command )
            for to_generate in [base_name+'.mp3',base_name+'.ogg']:
                if os.path.exists( to_generate ):
                    os.remove( to_generate )
                if to_generate.endswith( '.ogg' ):
                    extra_args = ['-acodec','libvorbis']
                else:
                    extra_args = []
                subprocess.check_call( [
                    'avconv', '-i', target_file] + extra_args + [to_generate,
                ])
        else:
            command = ['espeak','-v%s'%(options.voice,), '-k5','-s150', '-z', repr(word)]
            subprocess.check_call( command )

if __name__ == "__main__":
    main()
