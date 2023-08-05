import os.path as osp


def get_data_dir():
    this_dir = osp.dirname(osp.abspath(__file__))
    return osp.realpath(osp.join(this_dir, '_data'))
