import pymol
from pymol import cmd, stored, util
import helper_functions as hf


def get_chain_sequence(selection='sele'):
    '''
    DESCRIPTION:
    :param selection: the selected object in pymol
    :return: fasta sequence for the selection's chain
    '''
    selection_details = hf.get_selection_details(selection)
    seq = cmd.get_fastastr('chain ' + selection_details['chain']).rstrip()
    seq = seq.split('\n')
    seq = seq[0] + '_' + selection_details['chain'] + '\n' + ''.join(seq[1:])
    print seq
cmd.extend('get_chain_sequence', get_chain_sequence)


def get_object_sequence(selection='sele'):
    '''
    DESCRIPTION
    :param selection: the selected object in pymol
    :return: the object's sequence
    '''
    print cmd.get_fastastr(hf.get_selection_details(selection)['pdb_object_name'])
cmd.extend('get_object_sequence', get_object_sequence)