import pymol
from pymol import cmd, stored, util

aa_single_to_triplet = {'A': 'ALA', 'C': 'CYS', 'D': 'ASP', 'E': 'GLU', 'F': 'PHE', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
                        'K': 'LYS', 'L': 'LEU', 'M': 'MET', 'N': 'ASN', 'P': 'PRO', 'Q': 'GLN', 'R': 'ARG', 'S': 'SER',
                        'T': 'THR', 'V': 'VAL', 'W': 'TRP', 'Y': 'TYR'}
aa_triplet_to_single = {value: key for key, value in aa_single_to_triplet.items()}
ABC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
       'W', 'X', 'Y', 'Z']

def interface_analyser(name, dist_cuoff=10, animate=True):
    '''
DESCRIPTION
    displays the chains in different colors, showas cavity surfaces, and h.bonds with an interface cutoff
    of 10 (default)
    '''
    # cmd.hide("lines")
    cmd.select("interface", "none")
    alphabet = list(('abcdefghijklmnopqrstuvwxyz').upper())
    for letter in alphabet:
        chainname = "chain" + letter
        cmd.select(chainname, "%s and chain %s and not hetatm and not symbol w" % (name, letter))
        if cmd.count_atoms("chain%s" % (letter)) > 0:
            interfacename = "interface" + letter
            cmd.select("not_this_chain", "%s and not hetatm and not symbol w and not %s" % (name, chainname))
            cmd.select(interfacename, "%s and byres %s and (not_this_chain around %s)" % (name, chainname, str(dist_cuoff)))
            cmd.select("interface", "interface or %s" % (interfacename))
            cmd.delete("not_this_chain")
            cmd.delete("interface" + letter)
            cmd.delete("chain%s" % (letter))
        else:
            cmd.delete(chainname)
    cmd.hide("lines", name)
    cmd.show("lines", "interface")
    cmd.show("cartoon")
    cmd.dist("%s_h.bonds" % name, "interface", "interface", quiet=1, mode=2, label=0, reset=1,)
    cmd.enable("%s_h.bonds" % name)
    cmd.show("surface", "all")
    cmd.set('surface_cavity_mode', 1)
    util.color_chains("(all and elem c)", _self=cmd)
    if animate:
        cmd.zoom("interface", animate=-1)
        cmd.orient("interface", animate=-1)
    cmd.delete("interface")
    cmd.remove("(all) and hydro")
cmd.extend("interface_analyse", interface_analyser)


def load_and_analyse(list, dist_cutoff=10):
    '''
DESCRIPTION
    :param list: a list of PDBs to analyse
    :param dist_cutoff: distance cutoff for interface definition
    :return: shows the interface h.bonds, and cavities for all PDBs in the list
    '''
    first = True
    with open(list, 'r') as IN:
        for line in IN:
            if not line.endswith('.pdb'):
                line = line.rstrip() + '.pdb'
            cmd.load(line, line)
            if first:
                first_name = line[:-4]
            interface_analyser(line[:-4], dist_cuoff=dist_cutoff, animate=False)
            cmd.disable('all')
    util.mass_align(first_name, 0, _self=cmd)
    cmd.enable('all')
cmd.extend("load_and_analyse", load_and_analyse)


def show_pssm(pssm_file, selection='sele'):#, tell_1st_pdb_name=False, tell_2nd_pdb_name=False):
    '''
    DESCRIPTION
    :param selection: a selected residue
    :param pssm_file: path to relevant pssm file
    :return: shows a histogram of the residue's PSSM
    '''
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from subprocess import call as call
    import numpy as np

    selection_details = {}
    # cmd.color(4, selection)
    selection_details['raw'] = cmd.get_pdbstr(selection).split('\n')[1]
    selection_details['aa_type'] = selection_details['raw'].split()[3]
    selection_details['chain'] = selection_details['raw'].split()[4]
    selection_details['seq_position'] = selection_details['raw'].split()[5]
    selection_details['pdb_object_name'] = cmd.get_object_list(selection)[0]
    # name_split = selection_details['pdb_object_name'].split('_')
    # if tell_1st_pdb_name:
    #     print 'got 1st', tell_1st_pdb_name
    #     selection_details['pdb_name_chian_A'] = tell_1st_pdb_name
    #     if tell_2nd_pdb_name:
    #         selection_details['pdb_name_chian_B'] = tell_2nd_pdb_name
    # elif 'AB' in name_split:
    #     selection_details['pdb_name'] = name_split[0]
    if selection_details['chain'] != 'A':
        residue = {'residues': []}
        cmd.iterate('chain B', 'residues.append(resi)', space=residue)
        target_strand = set(residue.get('residues'))
        upto_chain = min(target_strand)
        selection_details['seq_position'] = int(selection_details['seq_position']) - int(upto_chain) + 1
    with open(pssm_file, 'r') as pssm_in:
        for line in pssm_in:
            if len(line.rstrip()) > 0:
                if line.split()[0] == 'A':
                    header = line.lower()
                if str(line.split()[0]) == str(int(selection_details['seq_position'])):
                    data_line = line
    header = header.split()[0:20]
    data_line = data_line.split()[0:22]
    header[header.index(aa_triplet_to_single[selection_details['aa_type']].lower())] = \
        aa_triplet_to_single[selection_details['aa_type']].upper()
    msg = ''
    for i in range(0, 20):
        msg += header[i] + ' ' + data_line[i+2] + '    '
    print msg

    header_upper = []
    [header_upper.append(x.upper()) for x in header]
    int_data = []
    [int_data.append(int(x)) for x in data_line[2:]]
    ind = np.arange(20)
    fig = plt.figure(figsize=(6, 5))
    ax = plt.subplot(111)
    ax.bar(ind, int_data)
    ax.set_ylabel('Frequency')
    ax.set_xticks(np.arange(20)+0.5)
    ax.set_xticklabels(header_upper)
    ax.get_children()[header.index(aa_triplet_to_single[selection_details['aa_type']])+2].set_color('r')
    ax.get_children()[header_upper.index(data_line[1].upper())+2].set_color('g')
    ax.set_xlabel('Amino Acid')
    ax.set_title('PSSM for ' + selection_details['aa_type'] + str(int(selection_details['seq_position'])) +
                 '\nRed: current, Green: WT')
    plt.savefig('/Users/jonathan/Desktop/test_1.png')
    plt.close()
    call(['open', '/Users/jonathan/Desktop/test_1.png'])
    # call(['osascript', '~/PycharmProjects/pymol_stuff/move_preview_to_right_for_pssm_pymol\ copy.scpt'])
cmd.extend("show_pssm", show_pssm)


def hot_spot_spheres(dist=4, sele='sele'):
    cmd.select('hot-spot', sele)
    cmd.select("sele", "(sele around " + str(dist) + ")", enable=1)
    cmd.show("spheres", 'sele')
    cmd.show("spheres", sele)
    cmd.show("spheres", "hot-spot")
    cmd.do('set sphere_transparency, 0.6, sele')
    cmd.select('around_hot-spot', 'sele')
    # cmd.delete('sele')
    # cmd.select('sele', 'hot-spot')
    # cmd.delete('hot-spot')
    # cmd.enable('sele')
cmd.extend("hot_spot_spheres", hot_spot_spheres)


def hot_spot_hide():
    cmd.hide("spheres", 'hot-spot')
    cmd.hide("spheres", 'around_hot-spot')
    cmd.delete('hot-spot')
    cmd.delete('around_hot-spot')
cmd.extend('hot_spot_hide', hot_spot_hide)


def interface_analyse_multi(dist=10):
    cmd.disable('all')
    all_objects = cmd.get_object_list()
    for obj in all_objects:
        print 'analysing', obj
        interface_analyser(obj, dist, animate=False)
        cmd.disable(obj)
        cmd.disable(obj + '_h.bonds')
    cmd.do('order *, yes')
    cmd.zoom(all_objects[0], animate=-1)
    cmd.orient(all_objects[0], animate=-1)
    cmd.enable(all_objects[0])
    cmd.enable(all_objects[0] + '_h.bonds')
cmd.extend('interface_analyse_multi', interface_analyse_multi)


cmd.set_key('ALT-H', hot_spot_spheres)
cmd.set_key('ALT-G', hot_spot_hide)