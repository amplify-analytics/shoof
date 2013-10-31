import os
from hurry.filesize import alternative, size


def rsize(path):
    return size(path, system=alternative)


def get_home():
    return os.path.expanduser('~')


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def list_dir(path, level=0):
    """
    get a dictionary of file paths in this file
    """
    directory_listing = []

    for root, dirs, files in walklevel(path, level=level):
        #import pdb; pdb.set_trace()

        # get all directories (as paths)
        if dirs:
            found = [{'path': root + '/' + f,
                      'name': f,
                      'type': 'dir',
                      'rsize': rsize(get_size(root + '/' + f)),
                      'size': get_size(root + '/' + f),
                      }
                     for f in dirs
                     #if os.path.isdir(f)
                     ]
            directory_listing.extend(found)

        # get all files (as paths)
        if files:
            found = [{'path': root + '/' + d,
                      'name': d,
                      'type': 'file',
                      'rsize': rsize(os.path.getsize(root + '/' + d)),
                      'size': os.path.getsize(root + '/' + d),
                      }
                     for d in files
                     ]
            directory_listing.extend(found)

    sorted_directory_listing = []
    if directory_listing:
        sorted_directory_listing = sorted(
            directory_listing, key=lambda k: k['size']
            )

    total_size = sum([d['size'] for d in directory_listing])
    return (sorted_directory_listing, total_size)


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size



from collections import namedtuple

_ntuple_diskusage = namedtuple('usage', 'total used free')

def disk_usage(path):
    """Return disk usage statistics about the given path.

    Returned valus is a named tuple with attributes 'total', 'used' and
    'free', which are the amount of total, used and free space, in bytes.
    """
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return _ntuple_diskusage(total, used, free)


def path_to_tree(input_path, level=2):
    # boo hoo hoo
    # if is file, return name, size
    # if is dir, call list_tree
# 
#     import pdb; pdb.set_trace()

    if level == 0:
        return

    dir_list = list_dir(input_path, level=0)[0]
    found_nodes = []

    for pobj in dir_list:
        node = {}

        if os.path.isdir(pobj['path']):
            # is a dir do stuff
            rlevel = level - 1
            children = path_to_tree(pobj['path'], rlevel)
            if children:
                node = {'name': pobj['name'],
                        'children': children
                        }
            else:
                #pass
                node = {'name': pobj['name'],
                        'size': pobj['size']
                        }
            if node:
                found_nodes.append(node)

        else:
            node['name'] = pobj['name']
            node['size'] = pobj['size']
            if node:
                found_nodes.append(node)
    return found_nodes


# References:
# http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
