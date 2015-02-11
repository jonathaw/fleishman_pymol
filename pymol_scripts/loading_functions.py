import pymol
from pymol import cmd, stored, util


def load_pdbs_by_regex(name_string):
    import re
    import os
    file_list = os.listdir('.')

