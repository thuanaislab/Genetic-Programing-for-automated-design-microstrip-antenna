# bachthuan03111997@gmail.com - 2018
import GP as gp 
import initGlobal as init
import copy 



def makeGP_prog(maxSub,maxPat,maxBlue,ismaxdep):
    # makeGP_prog makes a entire GP tree.
    # whre maxSub: the maximum depth of the genSub sub-tree.
    # maxPat: the maximum depth of the genPat sub-tree.
    # maxBlue: the maximum depth of the Blue sub-tree.
    # ismaxdep: specify whether GP tree will be created with maxdepth of all branch or not.
	GP_prog = gp.node()
	Sub = init.Sub()
	if init.Re_trainning:
		import update_state as us 
		anten = init.AnT()
		Sub = init.Sub()
		L   = init.L()
		U   = init.U()
		low = init.lowlevel()
		GP = init.GP()
		#path = us.load_temporary_path()
		us.update_all_saved_parameters(anten, sub, L, U, GP, low)

	GP_prog.strname = 'GP_prog'
	GP_prog.childs = []
	GP_prog.funcORter = 'func'

	# firstly need to create the substrate tree.
	if maxSub == 1:
		# create addsub3 tree.
		gensub1 = gp.node()
		gensub1.strname = 'gensub1'
		gensub1.type = 4
		gensub1.childs = []
		gensub1.childs.append(gp.addsub3())
		gensub1.funcORter = 'func'
		GP_prog.childs.append(gensub1)
	else: # when maxSub != 1.
		pass

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


	[tree,lastnode] = gp.makeBlueTree(maxBlue,ismaxdep,0,MaxX,MaxY)
	fullbluetree = gp.genFullBlueTree(tree)

	fullbluetree = gp.updateFullBlueTree(fullbluetree,[MaxX,MaxY],1)

	if maxPat == 1:
		# create
		genpat1 = gp.node()
		genpat1.strname = 'genpat1'
		genpat1.type = 5
		genpat1.childs = []
		bluetree1 = gp.node()
		bluetree1.strname = 'bluetree1'
		bluetree1.type = 2
		bluetree1.funcORter == 'func'
		bluetree1.childs = []
		bluetree1.childs.append(fullbluetree)
		genpat1.childs.append(bluetree1)
		genpat1.funcORter = 'func'
		GP_prog.childs.append(genpat1)
		GP_prog.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(fullbluetree))
		GP_prog.childs[1].valueofnode = GP_prog.childs[1].childs[0].valueofnode


	return GP_prog

