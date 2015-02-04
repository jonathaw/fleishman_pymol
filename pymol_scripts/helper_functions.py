import pymol
from pymol import cmd, stored, util


def get_selection_details(selection):
    selection_details = {}
    selection_details['raw'] = cmd.get_pdbstr(selection).split('\n')[1]
    selection_details['aa_type'] = selection_details['raw'].split()[3]
    selection_details['chain'] = selection_details['raw'].split()[4]
    selection_details['seq_position'] = selection_details['raw'].split()[5]
    selection_details['pdb_object_name'] = cmd.get_object_list(selection)[0]
    return selection_details