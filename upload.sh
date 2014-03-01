#! /bin/bash

./build.py
rsync -av build/* www.vex.net:~mcfletch/public_html/webtoys/

