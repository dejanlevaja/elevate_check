import os
import platform
import sys
import pefile
import argparse
from tabulate import tabulate
from BeautifulSoup import BeautifulSoup as BS
from BeautifulSoup import Comment
from fnmatch import fnmatch


# READ https://www.greyhathacker.net/?p=796
__author__ = 'Dejan Levaja'
__email__ = 'dejan[@]levaja.com'
__license__ = 'GPLv2'
__version__ = "1.1.0"

ver = platform.platform()
table = []

def list_all_files(root, pattern, recursive):
    allfiles = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                fpath = os.path.join(path, name)
                allfiles.append(fpath)
        if not recursive:
            return allfiles
            break

    return allfiles

def get_data(manifest, fname, ignore_ms):
    # print '\nFILENAME: %s' % fname
    # print 'MANIFEST: """%s"""' % manifest

    if manifest:
        soup = BS(manifest)
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

def get_manifest(fname):
    pe = pefile.PE(fname)
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            name = "%s" % pefile.RESOURCE_TYPE.get(resource_type.struct.Id)
            if name and hasattr(resource_type, 'directory'):
                for resource_id in resource_type.directory.entries:
                    if hasattr(resource_id, 'directory'):
                        for resource_lang in resource_id.directory.entries:
                            manifest = pe.get_data(
                                resource_lang.data.struct.OffsetToData,
                                resource_lang.data.struct.Size)
                            if 'MANIFEST' in name:
                                return manifest


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


    filenames = list_all_files(directory, "*.exe", recursive)

    #filenames = ['C:\Windows\System32\wusa.exe']
    total = len(filenames)


    # progress
    for i, filename in enumerate(filenames):
        print '[%s of %s] Processing file "%s"' % (i+1, total, filename)
        manifest = get_manifest(filename)
        get_data(manifest, filename, ignore_ms)




    # print table
    print '\n\n[!] Total found: %d' % len(table)
    headers = ['File', 'Description', 'Manufacturer']
    print tabulate(table, headers, tablefmt='grid')

    sys.exit('\n\n[!] Done.\n\n')
