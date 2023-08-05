import hashlib
import os
import os.path as osp
import re
import shlex
import subprocess
import sys
import tarfile
import zipfile

import numpy as np


# -----------------------------------------------------------------------------
# CV Util
# -----------------------------------------------------------------------------

def apply_mask(img, mask, crop=False):
    img[mask == 0] = 0

    if crop:
        where = np.argwhere(mask)
        (y_start, x_start), (y_stop, x_stop) = where.min(0), where.max(0) + 1
        img = img[y_start:y_stop, x_start:x_stop]

    return img


# -----------------------------------------------------------------------------
# Chainer Util
# -----------------------------------------------------------------------------

def copy_chainermodel(src, dst):
    from chainer import link
    assert isinstance(src, link.Chain)
    assert isinstance(dst, link.Chain)
    for child in src.children():
        if child.name not in dst.__dict__:
            continue
        dst_child = dst[child.name]
        if type(child) != type(dst_child):
            continue
        if isinstance(child, link.Chain):
            copy_chainermodel(child, dst_child)
        if isinstance(child, link.Link):
            match = True
            for a, b in zip(child.namedparams(), dst_child.namedparams()):
                if a[0] != b[0]:
                    match = False
                    break
                if a[1].data.shape != b[1].data.shape:
                    match = False
                    break
            if not match:
                print('Ignore %s because of parameter mismatch' % child.name)
                continue
            for a, b in zip(child.namedparams(), dst_child.namedparams()):
                b[1].data = a[1].data
            print('Copy %s' % child.name)


# -----------------------------------------------------------------------------
# Data Util
# -----------------------------------------------------------------------------

def extract_file(path, to_directory='.'):
    if path.endswith('.zip'):
        opener, mode = zipfile.ZipFile, 'r'
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        opener, mode = tarfile.open, 'r:gz'
    elif path.endswith('.tar.bz2') or path.endswith('.tbz'):
        opener, mode = tarfile.open, 'r:bz2'
    else:
        raise ValueError("Could not extract '%s' as no appropriate "
                         "extractor is found" % path)

    cwd = os.getcwd()
    os.chdir(to_directory)
    try:
        file = opener(path, mode)
        try:
            file.extractall()
        finally:
            file.close()
    finally:
        os.chdir(cwd)


def download(client, url, output, quiet=False):
    cmd = '{client} {url} -O {output}'.format(client=client, url=url,
                                              output=output)
    if quiet:
        cmd += ' --quiet'
    subprocess.call(shlex.split(cmd))


def check_md5(path, md5):
    is_same = hashlib.md5(open(path, 'rb').read()).hexdigest() == md5
    return is_same


def is_google_drive_url(url):
    m = re.match('^https?://drive.google.com/uc\?id=.*$', url)
    return m is not None


def download_data(pkg_name, path, url, md5, download_client=None,
                  extract=False, quiet=True):
    """Install test data checking md5 and rosbag decompress if needed."""
    if download_client is None:
        if is_google_drive_url(url):
            download_client = 'gdown'
        else:
            download_client = 'wget'
    # prepare cache dir
    cache_dir = osp.join(osp.expanduser('~/data'), pkg_name)
    if not osp.exists(cache_dir):
        os.makedirs(cache_dir)
    cache_file = osp.join(cache_dir, osp.basename(path))
    # check if cache exists, and update if necessary
    print("Checking md5 of '{path}'...".format(path=cache_file))
    if not (osp.exists(cache_file) and check_md5(cache_file, md5)):
        if osp.exists(cache_file):
            os.remove(cache_file)
        print("Downloading file from '{url}'...".format(url=url))
        download(download_client, url, cache_file, quiet=quiet)
    if osp.islink(path):
        # overwrite the link
        os.remove(path)
        os.symlink(cache_file, path)
    elif not osp.exists(path):
        if not osp.exists(osp.dirname(path)):
            os.makedirs(osp.dirname(path))
        os.symlink(cache_file, path)  # create link
    else:
        # not link and exists so skipping
        sys.stderr.write("WARNING: '{0}' exists\n".format(path))
        return
    if extract:
        print("Extracting '{path}'...".format(path=path))
        extract_file(path, to_directory=osp.dirname(path))


# -----------------------------------------------------------------------------
# Color Util
# -----------------------------------------------------------------------------

def bitget(byteval, idx):
    return ((byteval & (1 << idx)) != 0)


def labelcolormap(N=256):
    cmap = np.zeros((N, 3))
    for i in xrange(0, N):
        id = i
        r, g, b = 0, 0, 0
        for j in xrange(0, 8):
            r = np.bitwise_or(r, (bitget(id, 0) << 7-j))
            g = np.bitwise_or(g, (bitget(id, 1) << 7-j))
            b = np.bitwise_or(b, (bitget(id, 2) << 7-j))
            id = (id >> 3)
        cmap[i, 0] = r
        cmap[i, 1] = g
        cmap[i, 2] = b
    cmap = cmap.astype(np.float32) / 255
    return cmap


def visualize_labelcolormap(cmap):
    n_colors = len(cmap)
    ret = np.zeros((n_colors, 10 * 10, 3))
    for i in xrange(n_colors):
        ret[i, ...] = cmap[i]
    return ret.reshape((n_colors * 10, 10, 3))
