# fleishman_pymol
a repository for fleishman pymol scripts and stuff

please add your functions here:
if you're not sure how, it's the same as the rosetta wiki (markdown).

## structure analysis functions:
### interface_analyse
- input: object name, and distance (pido), with 10A as default
- action: turns all to cartoon, and interface to lines. shows interface h.bonds, and cavities.
- location: pymol_stuff/pymol_scripts/pymol_interface_analyser.py

### interface_analyser_with_surface
- inut object name, distance cutoff and chosen chain
- same as interface_analyse just that the chosen chain (default A) is showen as surface, and no cavities

### interface_analyse_multi
- input: distance (pido), default 10A
- perfmorms interface_analyse on all loaded objects. hides all but the first object and its h.bonds
- location: pymol_stuff/pymol_scripts/pymol_interface_analyser.py

### show hot-spot
- shows spheres for adjacent atoms. selection without transperancy, surrounding atoms with
- input: dist cutoff for 'around', default is 4 and selection (default sele)
- output: shows selection in spheres, and sourrounding in transperant spheres
- hot-key: ALT H
- hot-key to turn off: ALT G

## sequence related functions
### get_chain_sequence
- inout the selected object in pymol
- output fasta sequence for the selection's chain

### get_object_sequence
- inout: the selected object in pymol
- output:the object's sequence