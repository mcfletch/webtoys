#! /usr/bin/env python
"""Script to generate a bad-word-filtered word-list in json format

Uses the intersection of the system dictionary, a list of 10,000 common 
English words and the exclusion of a collection of "bad" words to produce 
a (hopefully) reasonable word-list.

Meh, the result isn't very clean, maybe should use nltk word-lists?
"""
import requests, os, json, glob, gzip
HERE = os.path.dirname( __file__ )
TARGET = os.path.join( HERE, '..', 'publish', 'wordlist','words.js' )

def get_badwords():
    if not os.path.exists( 'badwords.txt' ):
        response = requests.get('https://github.com/shutterstock/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/raw/master/en')
        if response.status_code == 200:
            open('badwords.txt','w').write( response.content )
            content = response.content 
        else:
            raise RuntimeError( 'Unable to download naughty-words list for filtering' )
    else:
        content = open('badwords.txt').read()
    return set([x.strip() for x in content.splitlines() if x.strip()])
def get_commonwords():
    if not os.path.exists( 'dictionary.txt' ):
        response = requests.get('https://github.com/first20hours/google-10000-english/raw/master/google-10000-english.txt')
        if response.status_code == 200:
            open('dictionary.txt','w').write( response.content )
            content = response.content 
        else:
            raise RuntimeError( 'Unable to download common-words list' )
    else:
        content = open( 'dictionary.txt').read()
    return [x.strip() for x in content.splitlines() if x.strip()]
def get_dictionary_words():
    return set([x.strip() for x in open('/usr/share/dict/words').read().splitlines() if x.strip()])

def filtered_dictionary():
    bad = get_badwords()
    dictionary = get_dictionary_words()
    words = set()
    for source in (get_commonwords(), dictionary ):
        for word in source:
            if (
                not word in bad and 
                not word[0].isupper() and 
                not word.endswith( "'s")
            ):
                if not (source is dictionary or word in dictionary):
                    print 'non-dictionary', word 
                else:
                    words.add( word )
            else:
                print 'filtered out %s'%(word,)
    # now explicitly make sure that we have our word-lists in there...
    for filename in glob.glob( os.path.join( HERE, 'wl-*.txt')):
        for word in open(filename).read().splitlines():
            words.add( word )
    words = sorted(words, key=lambda x: x.lower())
    with open( TARGET, 'w') as fh:
        fh.write( 'dictionary=' )
        print '%s words after filtering'%(len(words))
        fh.write( json.dumps( words ))

if __name__ == "__main__":
    filtered_dictionary()
    
