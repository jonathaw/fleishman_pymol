'''
goes over the sequences, naively, no alignment is done and makes a selection
of ALL the changed positions
'''
from pymol import cmd
from pymol import stored


def find_mutations(obj1, obj2, sel_name='mutations'):
    from pymol import stored, CmdException

    if cmd.count_atoms(obj1) == 0:
        print '%s is empty'%obj1
        return
    if cmd.count_atoms(obj2) == 0:
        print '%s is empty'%obj2
        return

    seq1 = ''.join(cmd.get_fastastr(obj1).split('\n')[1:])
    seq2 = ''.join(cmd.get_fastastr(obj2).split('\n')[1:])

    muts = []
    for i, aa in enumerate(seq1):
        if aa != seq2[i]:
            muts.append(i)

    if not muts:
        print('no mutations')
        return

    percent = 100 * float(len(muts)) / float(len(seq1))
    print 'found %i mutations with %s, which is %.2f' % (len(muts), obj2,
                                                         percent)

    # this is a correction for PDBs that are not renumbered, also if there's
    # a MEM residue in the middle of the numbering...
    stored.resis = []
    stored.resns = []
    cmd.iterate(obj1, 'stored.resis.append(resi)')
    cmd.iterate(obj1, 'stored.resns.append(resn)')
    resnums = sorted(list(set([int(a) for a, n in zip(stored.resis,
                                                      stored.resns)
                               if n != 'MEM'])))
    seq_num_resnum = {ind+1: val for ind, val in enumerate(resnums)}

    muts_s = ['%s' % str(seq_num_resnum[a+1]) for a in muts]
    muts_sel = '((%s and resi %s) or (%s and resi %s))' % (obj1,
                                                           '+'.join(muts_s),
                                                           obj2,
                                                           '+'.join(muts_s))
    cmd.select(sel_name, muts_sel)


cmd.extend("find_mutations", find_mutations)


def find_mutations_multi(ref, names, sel_prefix=''):
    """find_mutations_multi

    :param ref: reference object to compare all others to
    :param names: name regex to choose
    :param sel_prefix: a prefix to add to the selections
    """
    if cmd.count_atoms(ref) == 0:
        print '%s is empty' % ref
        return
    obj_lst = cmd.get_object_list('(%s)' % names)
    print obj_lst
    for obj in obj_lst:
        find_mutations(ref, obj, '%smuts_%s_%s' % (sel_prefix, ref, obj))


cmd.extend("find_mutations_multi", find_mutations_multi)
