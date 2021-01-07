# this file defines all of genetic operators used in GP process.
#						include:- crossover(pop,proRed,prosubBlue,proBlue,proSubstrate,proGensub,proGenpat)
#								- mutaion(pop,proRed,prosubBlue,proBlue,proSubstrate,proGensub,proGenpat)
#								- update_tree_after_GP_operation(GP_prog,nodeID,typeChange) # to help two above functions.
# bachthuan03111997@gmail.com
import Helper as hp
import copy
import initGlobal as init 
import GP as gp
import random
inGP = init.GP()
if init.Re_trainning:
        import update_state as us 
        AnT = init.AnT()
        Sub = init.Sub()
        L   = init.L()
        U   = init.U()
        low = init.lowlevel()
        inGP = init.GP()
        #path = us.load_temporary_path()
        us.update_all_saved_parameters(AnT, Sub, L, U, inGP, low)
def crossover(pop,state,proRed,prosubBlue,proBlue,proSubstrate,proGensub,proGenpat):
	# input arguments:
	#			POP - the population need be applied GP operators.
	#			PRORED - the probality whether the red node is picked to apply GP operators.
	#			PROSUBBLUE - _____________________ subblue node ______________________________.
	#			PROBLUE - ________________________ bluetree node______________________________.
	#			...............................................................................
	# Generate a child tree using crossover and previous generation of program.

	# top 20% of population (based on perfomance) is included in selection.


	## select two parents.
	# wait the hfss evaluation ____________________________________________________________________

	# this part is to test crossover function..................................
	lenth_pop = len(pop)
	num1 = round(random.uniform(0,state.numRepro + int(lenth_pop/4)))
	num2 = round(random.uniform(0,lenth_pop-1))
	num1 = state.curFitness[num1][1]
	num2 = state.curFitness[num2][1]
	parent1 = copy.deepcopy(pop[num1]); # the two parents are fixed to test this function.
	parent2 = copy.deepcopy(pop[num2]);
	#..........................................................................
	#hp.drawtree(parent1.tree)
	#hp.drawNodeIDs(parent1.tree)
	#hp.drawtree(parent2.tree)
	#hp.drawNodeIDs(parent2.tree)
	#parent1.tree.childs[1].valueofnode.plot()
	#parent2.tree.childs[1].valueofnode.plot()

	length = 100 # total length of list.
	lenRed = int(proRed*length)
	lensubBlue = int(prosubBlue*length)
	lenBlue = int(proBlue*length)
	lenSubstrate = int(proSubstrate*length)
	lenGensub = int(proGensub*length)
	lenGenpat = int(proGenpat*length)

	# Create list of crossover type.
	# Ex: cross_type_list = [1,1,1,1,1,1,1,2,2,2,2,2] then pick randomly a element form it.
	cross_type_list = [0 for i in range(lenRed)] # red
	subBluetemp = [1 for i in range(lensubBlue)]
	bluetemp = [2 for i in range(lenBlue)]
	Substratetemp = [3 for i in range(lenSubstrate)]
	Gensubtemp = [0 for i in range(lenGensub)] # It should be 4. It will be changed when this program is improved.
	Genpattemp = [1 for i in range(lenGenpat)] # It should be 5 

	cross_type_list = cross_type_list + subBluetemp + bluetemp + Substratetemp + Gensubtemp + Genpattemp
	#print(len(cross_type_list))
	#print(cross_type_list)
	cross_type = hp.getNumberFromList(cross_type_list)

	# get two nodeIDs of two tree parents.
	# cross_type = 1
	if cross_type == 0:
		cross1 = hp.getNumberFromList(parent1.nodelist.redlist)
		#while not (cross1 > 6):
		#	cross1 = hp.getNumberFromList(parent1.nodelist.redlist)
		#cross1 = 6
		cross2 = hp.getNumberFromList(parent2.nodelist.redlist)
	elif cross_type == 1: # cross operation in blue type.
		cross1 = hp.getNumberFromList(parent1.nodelist.subbluelist)
		cross2 = hp.getNumberFromList(parent2.nodelist.subbluelist)
		while (hp.calCurrentMaxDepth_fullTree(parent2.tree,cross2) > hp.calMaxdepBlueAble_fullTree(parent1.tree,inGP.maxBlue,cross1)):
			# checking to make sure that the maxdep of new node satifies the maxdepable of original node.
			# if not, find the new node that satisfaction 
			cross1 = hp.getNumberFromList(parent1.nodelist.subbluelist)
			cross2 = hp.getNumberFromList(parent2.nodelist.subbluelist)
			#print('cross1 blue: ',cross1)
			#print('cross2 blue: ',cross2)
			#print('____________________________________________________________________')
	elif cross_type == 2:
		cross1 = hp.getNumberFromList(parent1.nodelist.bluelist) # blue tree.
		cross2 = hp.getNumberFromList(parent2.nodelist.bluelist)
	elif cross_type == 3:
		cross1 = hp.getNumberFromList(parent1.nodelist.substratelist)
		cross2 = hp.getNumberFromList(parent2.nodelist.substratelist)
	'''
	elif cross_type == 4:
		cross1 = hp.getNumberFromList(parent1.nodelist.gensublist)
		cross2 = hp.getNumberFromList(parent2.nodelist.gensublist)
	else:
		cross1 = hp.getNumberFromList(parent1.nodelist.genpatlist)
		cross2 = hp.getNumberFromList(parent2.nodelist.genpatlist)'''

	# get subtree from parent2 (with node cross2 as the root)
	#print(cross_type)
	#print(cross1)
	#print(cross2)
	subtree2 = hp.getSubtreeFromTree(copy.deepcopy(parent2.tree),cross2) # this subtree to replace a node at parent 1.
	#hp.drawtree(subtree2)

	subtree1 = hp.getSubtreeFromTree(copy.deepcopy(parent1.tree),cross1) # get this tree to find the type of updating.

	#print('node1.valueofnode ',subtree1.valueofnode)
	#print('node2.valueofnode ',subtree2.valueofnode)

	changing_type = hp.get_type_of_updating(subtree1) # get the type of changing in the tree structure after applying any GP operators.

	#print('changing_type = ',changing_type)

	child1 = hp.replaceSubtree(parent1.tree,subtree2,cross1)
	hp.UpdateNodeIDs(child1,0)
	#hp.drawtree(child1)
	#hp.drawNodeIDs(child1)
	#print('before update: ',child1.substrate_size)
	#child1.childs[1].valueofnode.plot()
	child1 = update_tree_after_GP_operation(child1,cross1,changing_type)
	
	#print('after update: ',child1.substrate_size)
	#child1.childs[1].valueofnode.plot()

	
	#hp.drawNodeIDs(child1)
	#hp.drawtree(child1)

	return child1

def mutation(pop,state,proRed,prosubBlue,proBlue,proSubstrate,proGensub,proGenpat):
	# Generate a child tree using mutation and previous generation of program.
	# input arguments:
	#			POP - the population need be applied GP operators.
	#			PRORED - the probality whether the red node is picked to apply GP operators.
	#			PROSUBBLUE - _____________________ subblue node ______________________________.
	#			PROBLUE - ________________________ bluetree node______________________________.
	#			...............................................................................

	# top 20% of population (based on perfomance) is included in selection.


	## select 1 parent to participate in mutation operation.
	# wait the hfss evaluation ____________________________________________________________________

	# this part is to test mutation function..................................
	lenth_pop = len(pop)
	num1 = round(random.uniform(0,lenth_pop-1))
	num1 = state.curFitness[num1][1]
	parent1 = copy.deepcopy(pop[num1]); # the two parents are fixed to test this function.
	


	#..........................................................................
	#hp.drawtree(parent1.tree)
	#hp.drawNodeIDs(parent1.tree)
	#parent1.tree.childs[1].valueofnode.plot()

	# preprocess for creating list of mutation type.
	length = 100 # total length of list.
	lenRed = int(proRed*length) # need be the integer.
	lensubBlue = int(prosubBlue*length)
	lenBlue = int(proBlue*length)
	lenSubstrate = int(proSubstrate*length)
	lenGensub = int(proGensub*length)
	lenGenpat = int(proGenpat*length)

	# Create list of mutation type.
	# Ex: cross_type_list = [1,1,1,1,1,1,1,2,2,2,2,2] then pick randomly a element from it.
	mut_type_list = [0 for i in range(lenRed)] # red
	subBluetemp = [1 for i in range(lensubBlue)]
	bluetemp = [2 for i in range(lenBlue)]
	Substratetemp = [3 for i in range(lenSubstrate)]
	Gensubtemp = [0 for i in range(lenGensub)] # It should be 4. It will be changed when this program is improved.
	Genpattemp = [1 for i in range(lenGenpat)] # It should be 5 

	mut_type_list = mut_type_list + subBluetemp + bluetemp + Substratetemp + Gensubtemp + Genpattemp
	#print(len(mut_type_list))
	#print(mut_type_list)
	mut_type = hp.getNumberFromList(mut_type_list) # get type of changing in the tree structure after applying any GP operators.

	#mut_type = 1

	if mut_type == 0:
		mut = hp.getNumberFromList(parent1.nodelist.redlist)
		#mut = 5
	elif mut_type == 1:
		mut = hp.getNumberFromList(parent1.nodelist.subbluelist)
	#elif mut_type == 2:
	#	mut = hp.getNumberFromList(parent1.nodelist.bluelist)
	else:
		mut = hp.getNumberFromList(parent1.nodelist.substratelist)

	#print('mut_type: ',mut_type)
	#print('mut: ',mut)

	subtree1 = hp.getSubtreeFromTree(copy.deepcopy(parent1.tree),mut)
	#print('subtree1: ',subtree1.valueofnode)

	changing_type = hp.get_type_of_updating(subtree1)

	#print('before update: ',parent1.tree.substrate_size)

	#print('changing_type: ',changing_type)
	#parent1.tree.childs[1].valueofnode.plot()

	if (changing_type == 0) or (changing_type == 1) or (changing_type == 2):
		# in these types, the changing happended at red node.
		temp = gp.node()
		temp.valueofnode = round(random.uniform(-1,1),2)
		#print('temp.valueofnode: ',temp.valueofnode)
		temp.strname = str(temp.valueofnode)
		temp.funcORter = 'ter'
		temp.type = 0
		child1 = hp.replaceSubtree(parent1.tree,temp,mut)
		hp.UpdateNodeIDs(child1,0)
		child1 = update_tree_after_GP_operation(child1,mut,changing_type)
	elif changing_type == 3:
		# in this type, the changing happended at 'bluetree1' node.
		MaxX = parent1.tree.substrate_size[0]
		MaxY = parent1.tree.substrate_size[1]
		[temp1,temp2] = gp.makeBlueTree(inGP.maxBlue,False,0,MaxX,MaxY) # create a new bluetree.
		#hp.drawtree(temp1)

		while (hp.calCurrentMaxDepth(temp1) > hp.calMaxdepBlueAble_fullTree(parent1.tree,inGP.maxBlue,mut)):
			# checking to get the suitable bluetree that satified the maxdepable of original node.
			[temp1,temp2] = gp.makeBlueTree(inGP.maxBlue,False,0,MaxX,MaxY)
		#hp.drawtree(temp1)
		temp1 = gp.genFullBlueTree(temp1)
		temp1 = gp.updateFullBlueTree(temp1,[MaxX,MaxY],1)
		child1 = hp.replaceSubtree(parent1.tree,temp1,mut)
		hp.UpdateNodeIDs(child1,0)
		child1.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(child1.childs[1].childs[0].childs[0]))
		child1.childs[1].valueofnode = child1.childs[1].childs[0].valueofnode
	elif changing_type == 4:
		temp = gp.addsub3()
		child1 = hp.replaceSubtree(parent1.tree,temp,mut)
		hp.UpdateNodeIDs(child1,0)
		child1 = update_tree_after_GP_operation(child1,mut,changing_type)
	else: # changing_type == 5
		MaxX = parent1.tree.substrate_size[0] - Sub.decrease
		MaxY = parent1.tree.substrate_size[1] - Sub.decrease
		[temp1,temp2] = gp.makeBlueTree(inGP.maxBlue,False,0,MaxX,MaxY)
		temp1 = gp.genFullBlueTree(temp1)
		temp1 = gp.updateFullBlueTree(temp1,[MaxX,MaxY],1)
		bluetree1 = gp.node()
		bluetree1.strname = 'bluetree1'
		bluetree1.type = 2
		bluetree1.funcORter == 'func'
		bluetree1.childs = []
		bluetree1.childs.append(temp1)
		child1 = hp.replaceSubtree(parent1.tree,bluetree1,mut)
		child1.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(child1.childs[1].childs[0].childs[0]))
		child1.childs[1].valueofnode = child1.childs[1].childs[0].valueofnode
	#print('after update: ',child1.substrate_size)
	#hp.drawtree(child1)
	#child1.childs[1].valueofnode.plot()
	return child1


def update_tree_after_GP_operation(GP_prog,nodeID,typeChange):
	Sub = init.Sub() # to get some initial parameter of substrate.
	if typeChange == 1 or typeChange == 0:
		# calculate all of edge of substrate.
		if typeChange == 1:
			# in this type, the changing happended in red node of Terminal subtree.
			for i in range(2):
				# update some parameters for terminal red node.
				GP_prog.childs[0].childs[0].valueofnode[i] = GP_prog.childs[0].childs[0].childs[i].valueofnode
				GP_prog.childs[0].childs[0].childs[i].isRed_SubstrateNode = True
				GP_prog.childs[0].childs[0].childs[i].isRed_TerminalNode = True
				GP_prog.childs[0].childs[0].childs[i].special = False
				GP_prog.childs[0].childs[0].childs[2].is_red_rota = False
				GP_prog.childs[0].childs[0].childs[2].is_red_coords = False

			temp = GP_prog.childs[0].childs[0].valueofnode
			#Sub = init.Sub()
			for i in range(2):
				# recompute the normal size of each edge of substrate size.
				if i == 0:
					temp2 = round(((temp[i]+1)/2)*(Sub.rangeOx[1] - Sub.rangeOx[0]) + Sub.rangeOx[0],4)
				else:
					temp2 = round(((temp[i]+1)/2)*(Sub.rangeOy[1] - Sub.rangeOy[0]) + Sub.rangeOy[0],4)
				GP_prog.childs[0].valueofnode[i] = temp2
				GP_prog.childs[0].childs[0].valueofnode[i] = temp2
			#.
			MaxX = GP_prog.childs[0].valueofnode[0]  # update the maximum each edge of substrate size.
			MaxY = GP_prog.childs[0].valueofnode[1]
			GP_prog.substrate_size = [MaxX,MaxY,GP_prog.childs[0].valueofnode[2]]
			MaxXY = [MaxX-Sub.decrease,MaxY-Sub.decrease]
			GP_prog.childs[1].childs[0].childs[0] = gp.updateFullBlueTree(GP_prog.childs[1].childs[0].childs[0],MaxXY,3)
			GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(GP_prog.childs[1].childs[0].childs[0]))
			GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode
			#FullBlueTree = copy.deepcopy(GP_prog.childs[1].childs[0].childs[0])

		else: # typeChange == 0.
			# in this type, the changing happended in terminal red node of substrate tree, so it's not affect to other tree structure.
			#Sub = init.Sub()
			temp = GP_prog.childs[0].childs[0].childs[2].valueofnode
			GP_prog.childs[0].childs[0].valueofnode[2] = round(((temp+1)/2)*(Sub.rangeOz[1] - Sub.rangeOz[0]) + Sub.rangeOz[0],4)
			GP_prog.substrate_size[2] = GP_prog.childs[0].childs[0].valueofnode[2]
			GP_prog.childs[0].childs[0].childs[2].isRed_SubstrateNode = True
			GP_prog.childs[0].childs[0].childs[2].isRed_TerminalNode = False
			GP_prog.childs[0].childs[0].childs[2].special = True
			GP_prog.childs[0].childs[0].childs[2].is_red_rota = False
			GP_prog.childs[0].childs[0].childs[2].is_red_coords = False
	elif typeChange == 3:
		# in this type, the changing happended in the subblue node(like 'union','Lsubtree7',etc).
		#Sub = init.Sub()
		MaxX = GP_prog.substrate_size[0]
		MaxY = GP_prog.substrate_size[1]
		MaxXY = [MaxX-Sub.decrease,MaxY-Sub.decrease]
		subtree = hp.getSubtreeFromTree(copy.deepcopy(GP_prog),nodeID)
		subtree = gp.updateFullBlueTree(subtree,MaxXY,3)
		GP_prog = hp.replaceSubtree(GP_prog,subtree,nodeID)
		hp.UpdateNodeIDs(GP_prog,0)
		GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(GP_prog.childs[1].childs[0].childs[0]))
		GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode
	elif typeChange == 2:
		# in this type, the changing happended in the terminal red node of blue tree.
		#Sub = init.Sub()
		node = hp.getSubtreeFromTree(copy.deepcopy(GP_prog),nodeID)
		node.isRed_TerminalNode = True
		node.isRed_SubstrateNode = False
		node.special = False
		GP_prog = hp.replaceSubtree(GP_prog,node,nodeID)
		iii = 0 # this variable to know what type of the changing node.
		while not ((hp.getInfor_from_a_tree(copy.deepcopy(GP_prog),nodeID) == 'Lsubtree7') or (hp.getInfor_from_a_tree(copy.deepcopy(GP_prog),nodeID) == 'Usubtree9')):
			# find the suitable nodeID of the terminal node.
			# for example: from L-red node you find the L node, like that for U node.
			nodeID = nodeID - 1
			iii = iii + 1
		if (hp.getInfor_from_a_tree(copy.deepcopy(GP_prog),nodeID)) == 'Lsubtree7':
			type_termial = 'Lsubtree7'
		else:
			type_termial = 'Usubtree9'

		node = hp.getSubtreeFromTree(copy.deepcopy(GP_prog),nodeID)
		if type_termial == 'Lsubtree7':
			if iii == 1:
				node.childs[iii-1].is_red_rota = True
				node.childs[iii-1].is_red_coords = False
			elif iii == 6 or iii == 7:
				node.childs[iii-1].is_red_coords = True
				node.childs[iii-1].is_red_rota = False
			else:
				node.childs[iii-1].is_red_rota = False
				node.childs[iii-1].is_red_coords = False
		else:
			if iii == 1:
				node.childs[iii-1].is_red_rota = True
				node.childs[iii-1].is_red_coords = False
			elif iii == 8 or iii == 9:
				node.childs[iii-1].is_red_coords = True
				node.childs[iii-1].is_red_rota = False
			else:
				node.childs[iii-1].is_red_rota = False
				node.childs[iii-1].is_red_coords = False
		MaxX = GP_prog.substrate_size[0]
		MaxY = GP_prog.substrate_size[1]
		MaxXY = [MaxX-Sub.decrease,MaxY-Sub.decrease]
		node = gp.updateFullBlueTree(node,MaxXY,2)
		GP_prog = hp.replaceSubtree(GP_prog,node,nodeID)
		hp.UpdateNodeIDs(GP_prog,0)
		GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(GP_prog.childs[1].childs[0].childs[0]))
		GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode
	elif typeChange == 4:
		# in this type, the changing happeded in the 'addsub1' node.
		temp = GP_prog.childs[0].childs[0].valueofnode
		
		for i in range(3):
			# recaclulate all sizes of the substrate size.
			if i == 0:
				temp1 = round(((temp[i]+1)/2)*(Sub.rangeOx[1] - Sub.rangeOx[0]) + Sub.rangeOx[0],4)
			elif i == 1:
				temp1 = round(((temp[i]+1)/2)*(Sub.rangeOy[1] - Sub.rangeOy[0]) + Sub.rangeOy[0],4)
			else:
				temp1 = round(((temp[i]+1)/2)*(Sub.rangeOz[1] - Sub.rangeOz[0]) + Sub.rangeOz[0],4)
			GP_prog.childs[0].valueofnode[i] = temp1
			GP_prog.substrate_size[i] = temp1
		MaxXY = [GP_prog.substrate_size[0]-Sub.decrease,GP_prog.substrate_size[1] - Sub.decrease]
		GP_prog.childs[1].childs[0].childs[0] = gp.updateFullBlueTree(GP_prog.childs[1].childs[0].childs[0],MaxXY,3)
		GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(GP_prog.childs[1].childs[0].childs[0]))
		GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode
	elif typeChange == 5:
		# in this type, the changing happended at 'bluetree1'.
		MaxXY = [GP_prog.substrate_size[0]-Sub.decrease,GP_prog.substrate_size[1] - Sub.decrease]
		GP_prog.childs[1].childs[0].childs[0] = gp.updateFullBlueTree(GP_prog.childs[1].childs[0].childs[0],MaxXY,3)
		GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(GP_prog.childs[1].childs[0].childs[0]))
		GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode

	return GP_prog







