# fleishman_pymol
a repository for fleishman pymol scripts and stuff

please add your functions here:
if you're not sure how, it's the same as the rosetta wiki (markdown).

## interface_analyse
- input: object name, and distance (pido), with 10A as default
- action: turns all to cartoon, and interface to lines. shows interface h.bonds, and cavities.
- location: pymol_stuff/pymol_scripts/pymol_interface_analyser.py

## interface_analyse_multi
-input: distance (pido), default 10A
-perfmorms interface_analyse on all loaded objects. hides all but the first object and its h.bonds
-location: pymol_stuff/pymol_scripts/pymol_interface_analyser.py
