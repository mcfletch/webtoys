#! /bin/bash

./build.py
rsync -av build/* blog.vrplumber.com:/var/webtoys/www/

