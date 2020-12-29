# this problem can be solved by http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html 


import Helper as hp
import GP as gp
import copy
import Terminalset as ts
from genscript import genscript

def load_str_tree(path):
	tree_str = ''
	with open(path) as temp:
		for i in temp:
			tree_str = tree_str + i
	return tree_str
#print(tree_str)
def str2tree(tree_str,current_index,current_ID_tree,current_depth,tree):
 	# Function convert tree under string type to datastructure in GP software.
	# Where:
	#		- tree_str : is the tree under string type.
	#		- current_index: is the current index in tree_str string sequence. " equal 0 at the initation "
	#		- current_ID_tree: is the current #### this val need be 1 in the first time. " equal 1 at the initation "
	#		- current_depth: is the depth of the current node. "equal 0 at the initation "
	#		- tree: is the GP_prog tree. " equal None at the initation "

	current_index = current_index + 1
	if current_index == len(tree_str):
		# convert completely. 
		return tree

	if tree_str[current_index] == ')' or tree_str[current_index] == ',':
		#print(tree_str[current_index])
		##print('current_depth ',current_depth)
		current_depth = current_depth - 1
		temp_depth = hp.getSubtreeFromTree(copy.deepcopy(tree),current_ID_tree) # get specified node.
		temp_depth = temp_depth.depth
		##print(temp_depth, '_____',current_depth)
		##print('current_ID_tree ' ,current_ID_tree)							 # get the depth of that node.
		while temp_depth != current_depth:
			
			current_ID_tree = current_ID_tree - 1
			temp_depth = hp.getSubtreeFromTree(copy.deepcopy(tree),current_ID_tree) # get specified node.
			temp_depth = temp_depth.depth # get the depth of that node.
			#print(temp_depth, '_____',current_depth)
		#print(current_ID_tree)	
		return str2tree(tree_str,current_index,current_ID_tree,current_depth,tree)
	elif tree_str[current_index] == '(' or (tree_str[current_index] != ')' and tree_str[current_index] != ','):
		if (tree_str[current_index] == '(') or (current_index == 1):
			current_index = current_index + 1
		if current_index == 2:
			# in here the index is in the GP_prog range.
			current_index = 0
		temp_str = ''
		while tree_str[current_index] != '(' and tree_str[current_index] != ')' and tree_str[current_index] != ',':
			# get the string name of current node.
			temp_str = temp_str + tree_str[current_index]
			current_index = current_index + 1
		current_index = current_index - 1
		#print(temp_str)

		try:
			float(temp_str) # checking whether temp_str is the red node. 
			is_red = True
		except:
			is_red = False

		if temp_str == 'GP_prog':
			tree = gp.node()
			tree.strname = 'GP_prog' # create the root node.
			tree.childs = []
			tree.funcORter = 'func'
			current_ID_tree = hp.UpdateNodeIDs(tree,0)
			gp.update_Depth_GP_tree(tree,0)
			return str2tree(tree_str,current_index,current_ID_tree,current_depth,tree)
		else:
			temp_node = hp.getSubtreeFromTree(copy.deepcopy(tree),current_ID_tree)
			t_node = gp.node()
			t_node.strname = temp_str
			if is_red: # current node string is red node. 
				t_node.funcORter = 'ter'
				t_node.isRed_TerminalNode = True
				t_node.type = 0 # red type
				t_node.valueofnode = float(temp_str)
				if temp_node.strname == 'addsub3':
					# update some variable to be suitable according to their parent node.
					t_node.isRed_SubstrateNode = True
					if len(temp_node.childs) == 2:
						t_node.special = True
				
					#temp_node.valueofnode.append(t_node.valueofnode)
				elif temp_node.strname == 'Lsubtree7':
					# update some variable to be suitable according to their parent node.
					if len(temp_node.childs) == 0:
						t_node.is_red_rota = True
					if (len(temp_node.childs)) == 5 or (len(temp_node.childs) == 6):
						t_node.is_red_coords = True
				elif temp_node.strname == 'Usubtree9':
					# update some variable to be suitable according to their parent node.
					if len(temp_node.childs) == 0:
						t_node.is_red_rota = True
					if (len(temp_node.childs)) == 7 or (len(temp_node.childs) == 8):
						t_node.is_red_coords = True
				temp_node.childs.append(t_node) #
				#current_ID_tree = current_ID_tree + 1
				current_depth = current_depth + 1

				tree = hp.replaceSubtree(tree,temp_node,temp_node.nodeID) # update new tree. 
				current_ID_tree = hp.UpdateNodeIDs(tree,0)
				gp.update_Depth_GP_tree(tree,0)
				#print('current_ID_tree ', current_ID_tree)
				#print("current_depth ",current_depth)
				#hp.drawtree(tree)
				return str2tree(tree_str,current_index,current_ID_tree,current_depth,tree)
			else:
				t_node.childs = []
				t_node.funcORter = 'func'
				t_node.valueofnode = [] 
				if temp_str == 'gensub1':
					t_node.type = 4
					########
					#temp_node.childs.append(t_node)
					#current_ID_tree = current_ID_tree + 1
					#current_depth = current_depth + 1
					######################
				elif temp_str == 'addsub3':
					t_node.type = 3 # substrate type
					t_node.numberChilds = 3
					t_node.funcORter = 'func'
				elif temp_str == 'genpat1':
					t_node.type = 5
					t_node.numberChilds = 1
				elif temp_str == 'bluetree1':
					t_node.type = 2
					t_node.numberChilds = 1
				elif temp_str == 'union2':
					t_node.type = 1
					t_node.numberChilds = 2
				elif temp_str == 'Lsubtree7':
					t_node.LeafClass = ts.Lsub_tree(10,10)
					t_node.type = 1
					t_node.numberChilds = 7
				elif temp_str == 'Usubtree9':
					t_node.LeafClass = ts.Usub_tree(10,10)
					t_node.type = 1
					t_node.numberChilds = 9

				temp_node.childs.append(t_node) #
				#current_ID_tree = current_ID_tree + 1
				current_depth = current_depth + 1

				tree = hp.replaceSubtree(tree,temp_node,temp_node.nodeID) # update new tree. 
				current_ID_tree = hp.UpdateNodeIDs(tree,0)
				gp.update_Depth_GP_tree(tree,0)
				#hp.drawtree(tree)
				#print('current_ID_tree ', current_ID_tree)
				#print("current_depth ",current_depth)
				return str2tree(tree_str,current_index,current_ID_tree,current_depth,tree)

'''
	else:
		# in here the node need be the root node.
		if current_index == 1
			current_index = current_index - 1
		temp_str = ''
		while tree_str[current_index] != '(' and tree_str[current_index] != ')' and tree_str[current_index] != ',':
			# get the string name of current node.
			temp_str = temp_str + tree_str[current_index]
			current_index = current_index + 1
		current_index = current_index - 1
		#print(temp_str)
		#print("current_depth ",current_depth)
		tree = gp.node()
		tree.strname = 'GP_prog' # create the root node.
		tree.childs = []
		tree.funcORter = 'func'
		current_ID_tree = hp.UpdateNodeIDs(tree,0)
		gp.update_Depth_GP_tree(tree,0)
		#print('current_ID_tree ', current_ID_tree)
		tree, current_index, current_ID_tree, current_depth = str2tree(tree_str,current_index,current_ID_tree,current_depth,tree)'''

def update_tree(GP_prog):
	import initGlobal as init 
	import update_state as us 
	anten = init.AnT()
	Sub = init.Sub()
	L   = init.L()
	U   = init.U()
	low = init.lowlevel()
	GP = init.GP()
	#path = us.load_temporary_path()
	us.update_all_saved_parameters(anten, Sub, L, U, GP, low)

	# calculate all of edge of substrate.
	GP_prog.childs[0].childs[0].valueofnode = []
	for i in range(3):
		GP_prog.childs[0].childs[0].valueofnode.append(GP_prog.childs[0].childs[0].childs[i].valueofnode)

	temp = GP_prog.childs[0].childs[0].valueofnode
	
	GP_prog.childs[0].valueofnode = []
	for i in range(3):
		# calculate all of the real substrate's parameters. 
		if i == 0:
			temp2 = round(((temp[i]+1)/2)*(Sub.rangeOx[1] - Sub.rangeOx[0]) + Sub.rangeOx[0],4) # Ox edge
		elif i == 1:
			temp2 = round(((temp[i]+1)/2)*(Sub.rangeOy[1] - Sub.rangeOy[0]) + Sub.rangeOy[0],4) # Oy edge.
		else:
			temp2 = round(((temp[i]+1)/2)*(Sub.rangeOz[1] - Sub.rangeOz[0]) + Sub.rangeOz[0],4) # Oz edge.
		GP_prog.childs[0].valueofnode.append(temp2)

	# Secondly create patterns.
	MaxX = GP_prog.childs[0].valueofnode[0] - Sub.decrease ### real MaxX,Y are decreased 1mm before to create
												  # any pattern unit(like L1,U1,U2,...).
	MaxY = GP_prog.childs[0].valueofnode[1] - Sub.decrease
	Zsize = GP_prog.childs[0].valueofnode[2]
	GP_prog.substrate_size = [MaxX+Sub.decrease,MaxY+Sub.decrease,Zsize]


	GP_prog.childs[1].childs[0].childs[0] = gp.updateFullBlueTree(GP_prog.childs[1].childs[0].childs[0],[MaxX,MaxY],5)
	GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(GP_prog.childs[1].childs[0].childs[0]))
	GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode

	return GP_prog

############# LOAD THE TREE

# tree_str = load_str_tree('C:/Users/DELL/Desktop/24-35Ghzz/GP2019_03_28_11h18m27s/temp/MPA_gen_1_pop_0.txt')
# tree = str2tree(tree_str,0,1,0,None)
# tree = update_tree(tree)
# [Substrate,polygons,centroid,poly_list, poly_list_type] = hp.get_all_para_for_hfss(tree) # get necessary parameters for genscript function.
# name = 'C:/Users/DELL/Desktop/Newfolder/' # name of directory would
# 																			# be used to save .vbs and .hfss file.
# #tabname = global_tabname + str(gen) + '_pop_' + str(i) # name of directory
# 																			# would be used to save .tab file. 
# genscript(Substrate,polygons,centroid,name + '.vbs',name,name + '.hfss',poly_list,poly_list_type)
# hp.drawtree(tree)

############# CHANGE TREE 