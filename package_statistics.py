import sys
import os
import re
import gzip
import io
import requests
import logging
from hashlib import md5
from optparse import OptionParser
from operator import itemgetter
from itertools import groupby

CACHE_PATH = '/var/tmp'

parser = OptionParser()
parser.add_option('--mirror', dest='mirror', default='http://ftp.uk.debian.org/debian/dists/stable/main/')
parser.add_option('--arch', dest='arch', default='amd64')
parser.add_option('--level', dest='level', default='INFO')
parser.add_option('--cache', dest='cache', action='store_true', default=False, help='Use local cache')
options, args = parser.parse_args()

# add logging
log = logging.getLogger()
hldr = logging.StreamHandler(sys.stdout)
hldr.setFormatter(logging.Formatter('%(asctime)s [%(name)-20s] %(levelname)-8s> %(message)s'))
log.setLevel(getattr(logging, options.level.upper()))
log.addHandler(hldr)

log.info('Starting stats script')

def save_cache(cache_file, content):
    with open(cache_file, 'wb') as f:
        f.write(content)


def download_file(url):
    """Downloading externally hosted file"""
    cache_file = os.path.join(CACHE_PATH, md5(url.encode('latin-1')).hexdigest())

    if options.cache and os.path.exists(cache_file) and os.stat(cache_file).st_size > 0:
        log.info('Using file from cache: {}'.format(cache_file))
        return open(cache_file, 'rb').read()

    log.info('Fetching contents file: {}'.format(url))
    r = requests.get(url, allow_redirects=True)

    if options.cache and not os.path.exists(cache_file):
        save_cache(cache_file, r.content)
    return r.content


def gunzip(data):
    """Unzipping content"""
    obj_in = io.BytesIO()
    obj_in.write(data)
    obj_in.seek(0)
    with gzip.GzipFile(fileobj=obj_in, mode='rb') as fo:
        unzipped_data = fo.read()

    return unzipped_data


def stats(data):
    """
    Collecting stats based in Contents file, exampe structure

    usr/share/ifeffit/cldata/91.dat                         contrib/science/ifeffit
    usr/share/ifeffit/cldata/92.dat                         contrib/science/ifeffit

    """
    log.info('Generating stats')
    results = []
    pkgs = re.findall(rb'\s+(.*?)\n', data)
    for key, group in groupby(pkgs):
        results.append((key, len(list(group))))
    return results


def top_list(stats_data, number_of_results=10):
    """Sorting by the best results"""
    if stats_data:
        log.info('Sorting results')
        return sorted(stats_data, key=itemgetter(1), reverse=True)[:number_of_results]
    log.warning('Invalid stats data: {}'.format(stats_data))


def print_line(elem_1, elem_2, elem_3):
    log.info("{}|{}|{}".format(
            str(elem_1).rjust(2),
            str(elem_2).rjust(100),
            str(elem_3).rjust(20)
        ))


def pretty_print_results(data):
    """Pretty print stats"""
    print_line("No", "package name", "number of files")

    for i, v in enumerate(data if data else []):
        print_line(i + 1, v[0], v[1])

def main():
    download_url = "{}Contents-{}.gz".format(options.mirror, options.arch)
    data = download_file(download_url)
    if data:
        result = stats(gunzip(data))
        top_items = top_list(result)
        pretty_print_results(top_items)
    else:
        log.error('Problem with fetching data')


if __name__ == "__main__":
    main()
