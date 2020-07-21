#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse

# https://github.com/soulxhacker/Google-Python-LogPuzzle/blob/master/logpuzzle.py


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open(filename) as open_file:
        file_list = open_file.readlines()  # save whats in the file to a list.
        urls = []  # a list that will soon contain all of the urls we need!

        # iterate over each file in our filelist
        for string in file_list:
            current_string = string  # saving the iterator string to a var
            # a regex pattern used to find the images
            file_pattern = r'/edu.*.jpg'
            # searching for a match
            file_match = re.search(file_pattern, current_string)
            if file_match:
                # if we find a match...
                if "http://code.google.com"+file_match.group() not in urls:
                    # add the complete url obtained
                    #  the string to the url list
                    urls.append("http://code.google.com"+file_match.group())
            else:
                # we do nothing
                pass
            sorted_urls = sorted(urls, key=last_word)
        for url in sorted_urls:
            print(url + '\n')
        return sorted_urls  # so we can pass into next function


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    file_count = 0
    if os.path.exists(dest_dir):
        for img in img_urls:
            print('Retrieving {} image(s)...'.format(file_count + 1))
            file_img_path = os.path.join(dest_dir, 'img{}'.format(file_count))
            file_count += 1
            urllib.request.urlretrieve(img, file_img_path)
    else:
        image_dir = os.mkdir(dest_dir)
        for img in img_urls:
            print('Retrieving {} images...'.format(file_count + 1))
            file_img_path = os.path.join(image_dir, 'img{}'.format(file_count))
            file_count += 1
            urllib.request.urlretrieve(img, file_img_path)

    with open(dest_dir+'/index.html', 'w') as filename:

        html_boiler = """<html>
        <head></head>
        <body>
        """
        html_closer = "</body></html>"
        filename.write(html_boiler)
        for img in img_urls:
            img_string = '<img src={}></img>'.format(img)
            filename.write(img_string)
        filename.write(html_closer)

    return  # returns the list of filenames


def last_word(url):
    """Use a regex pattern to capture the last 
    word of the file to sort alphabetically."""
    return re.findall(r"-(....).jpg", url)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
