#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse
import codecs
import os
import pkg_resources
import re
import subprocess
import sys
try:
    from urlparse import urlparse
    from urlparse import parse_qs
except ImportError:
    from urllib.parse import urlparse
    from urllib.parse import parse_qs


__author__ = 'Kentaro Wada <www.kentaro.wada@gmail.com>'
__version__ = pkg_resources.get_distribution('gdown').version


def wget_download(url, filename, be_quiet):
    cmd = 'wget --load-cookie /tmp/cookie.txt'
    if be_quiet:
        cmd += ' --quiet'
    cmd += ' --save-cookie /tmp/cookie.txt "{0}"'
    cmd = cmd.format(url)
    if filename:
        cmd += ' -O {}'.format(filename)
    subprocess.call(cmd, shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-O', '--output', default=None)
    parser.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()
    url = args.url
    filename = args.output
    be_quiet = args.quiet
    if filename is None:
        query = urlparse(url).query
        filename = parse_qs(query)['id'][0]

    wget_download(url, filename, be_quiet)

    while os.stat(filename).st_size < 100000:
        with codecs.open(filename, 'r', encoding='latin-1') as f:
            for line in f.readlines():
                m = re.search('href="(\/uc\?export=download[^"]+)', line)
                if m:
                    url = 'https://docs.google.com' + m.groups()[0]
                    url = url.replace('&amp;', '&')
                    confirm = ''
                    break
                m = re.search('confirm=([^;&]+)', line)
                if m:
                    confirm = m.groups()[0]
                    break
                m = re.search('"downloadUrl":"([^"]+)', line)
                if m:
                    url = m.groups()[0]
                    url = url.replace('\\u003d', '=')
                    url = url.replace('\\u0026', '&')
                    confirm = ''
                    break
            else:
                print('Small size file or invalid url.')
                quit()

        if confirm:
            url = re.sub(r'confirm=([^;&]+)', r'confirm='+confirm, url)

        wget_download(url=url, filename=filename, be_quiet=be_quiet)


if __name__ == '__main__':
    main()
