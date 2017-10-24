'''
jusat print the seqeunce
'''

from pymol import cmd


def get_seq(obj1):
    seq1 = ''.join(cmd.get_fastastr(obj1).split('\n')[1:])
    print(seq1)


cmd.extend("get_seq", get_seq)
