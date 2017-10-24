'''
returns if a slected PROLINE is cis or trans
'''

from pymol import cmd


def is_pro_cis_or_trans(obj, resi, chain=None):
    gen_sel = '%s and chain %s and resi %s ' % (obj, chain, resi)
    cmd.select('temp_O', '%s and chain %s and resi %i and name O' % (obj, chain,
                                                                    int(resi)-1))
    cmd.select('temp_C', '%s and chain %s and resi %i and name C' % (obj, chain,
                                                                    int(resi)-1))
    cmd.select('temp_N', '%s and name N' % gen_sel)
    cmd.select('temp_CD', '%s and name CD' % gen_sel)

    dihedral = cmd.get_dihedral('temp_O', 'temp_C', 'temp_N', 'temp_CD', state=0)
    if -170 <= dihedral <= 190:
        cis_or_trans = 'trans'
    elif -10 <= dihedral <= +10:
        cis_or_trans = 'cis'
    else:
        cis_or_trans = 'unknown'
    print('the dihedral is %.2f, I think it is %s' % (dihedral, cis_or_trans))

    for atom in ['O', 'C', 'N', 'CD']:
        cmd.delete('temp_%s' % atom)


cmd.extend("is_pro_cis_or_trans", is_pro_cis_or_trans)
