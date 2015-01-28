from pymol import cmd

def residuesInSelection(selection=""):

	if selection == "":
		print "usage: residuesInSelection(selection)"
		return

	Taken = {}
	mysel = cmd.get_model(selection)
	natom = len(mysel.atom)
	for i in range(natom):
		Taken[mysel.atom[i].resi] = True

	mylist = []
	for i in Taken.keys():
		mylist.append(int(i))

	mylist.sort()
	return mylist
