import glob
import platform
import re
import sys
import argparse
from tabulate import tabulate
from BeautifulSoup import BeautifulSoup as BS
from BeautifulSoup import Comment

__author__ = 'Dejan Levaja'
__email__ = 'dejan[@]levaja.com'
__license__ = 'GPLv2'
__version__ = "1.0.0"

ver = platform.platform()
table = []


def get_data(fname, ignore_ms):
    with open(fname, "rb") as f:
        raw = f.read()
    unicode_str = re.compile(u'[\u0020-\u007e]{3,}', re.UNICODE)
    strings = unicode_str.findall(raw)
    soup = BS('\n'.join(strings))
    elevator = soup.find('autoelevate')
    if elevator:
        el= elevator.string
        if str(el) == 'true':
            desc = soup.find('description')
            if desc:
                description = desc.string
            else:
                description = ''
            comments = soup.findAll(text=lambda text: isinstance(text, Comment))
            for comment in comments:
                if "Copyright" in comment:
                    manufacturer = comment.strip()
                    if 'microsoft' in manufacturer.lower():
                        if not ignore_ms:
                            text = "%s,%s,%s" % (fname, description, manufacturer)
                            table.append(text.split(','))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='Target directory.', default="C:\\Windows\\System32")
    parser.add_argument('-r', '--recursive', help='Scan subfolders as fell.', action='store_true')
    parser.add_argument('-i', '--ignore-ms', help='Ignore files manufactured by Microsoft.', action='store_true')
    args = vars(parser.parse_args())

    directory = args['directory']
    recursive = args['recursive']
    ignore_ms = args['ignore_ms']

    print '\nPlease wait, it can take some time...'

    if recursive:
        base_path = directory + '\\*.exe'
        filenames = glob.glob(base_path)
        sub_path = directory + '\\**\\*.exe'
        filenames += glob.glob(sub_path)
    else:
        base_path = directory + '\\*.exe'
        filenames = glob.glob(base_path)

    total = len(filenames)

    # progress
    for i, filename in enumerate(filenames):
        print '[%s of %s] Processing file "%s"' % (i+1, total, filename)
        get_data(filename, ignore_ms)


    # print table
    print '\n\n[!] Total found: %d' % len(table)
    headers = ['File', 'Description', 'Manufacturer']
    print tabulate(table, headers, tablefmt='grid')

    sys.exit('\n\n[!] Done.\n\n')
