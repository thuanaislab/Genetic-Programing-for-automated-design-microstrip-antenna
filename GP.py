# this file includes: 
#                   - makeBluetree()
#                   - synthesisBlueTree()
#                   - genFullBlueTree()
#                   - convertFullBluetree_to_oriBluetree()
#                   - get_val_frombluetree()
#                   - addsub3()
# bachthuan03111997@gmail.com
import random
import geopandas as gpd
import Terminalset as ts


##############################################################################
######################## This part is the part of Genetic Programming process.
class node:   # Define a node of tree.
# node class to save some attributes of that node.
    def __init__(self):
        self.childs = None
        self.numberChilds = 0;
        self.strname = ''
        self.nodeID = 0                # the ID of that node in tree.
        self.funcORter = 'ter'         # 'ter' is the terminal node, else 'func' is the function node.
        self.valueofnode = 0           # the value of that node. Ex: the value of the polygon type under Dataframe type.
        self.numNodes  = 0             # number of node in current node that it contains.
        self.maxNodeID = 0             # max ID of node in current node that it contains.
        self.synthesischeck = False
        self.LeafClass = None          # this attribute to save leaf class.
        self.type = None               # Type of the node like red,blue,substrate, etc.
        self.isRed_SubstrateNode = False 
        self.isRed_TerminalNode = False
        self.special = False           # to show it's the third parameter of addsub tree or not
        self.is_red_rota = False       # to specify whether node is represented for rotation or not.
        self.is_red_coords = False     # to specify whether node is represented for coords or not.
        self.depth = 0                 # to show it's depth.

def makeBlueTree(maxdep,ismaxdepth,lastnode,MaxX,MaxY):
    # NOTICE THAT: THIS FUNCTION RELATES TO NUMBER OF TERMINAL SET (now system has two terminals: lsubtree and Usubtree)
    # MAXDEP is the maximum of depth that tree has(integer).
    # ISMAXDEPTH whether tree is created by all branch is maxdep or not(boolean).
    # LASTNODE is the last node id of previous tree(integer).
    # MaxX is the maximum length of X axis.
    # MaxY is the maximum length of Y axis.
    # note: 
        # makeBlueTree is the recursive function.
    # maxdep = maxdep - 1.
    # RETURN: [tree,lastnode].
    thisnode = lastnode + 1
    tree = node()
    if ismaxdepth: # Full method.
        if maxdep == 0:
            # we must chose a terminal.
            LorU = random.randint(0,1) # 0 is the Ltree else is the Utree.
            if LorU == 0:
                xtype = random.randint(1,4)
                temp = ts.Lsub_tree(MaxX,MaxY,xtype)
                tree.strname = temp.strname
                tree.nodeID = thisnode
                tree.funcORter = 'ter'
                tree.valueofnode = temp.polygon
                tree.LeafClass = temp   # save class object.
                tree.type = 1
            else:
                xtype = random.randint(1,4)
                temp = ts.Usub_tree(MaxX,MaxY,xtype)
                tree.strname = temp.strname
                tree.nodeID = thisnode
                tree.funcORter = 'ter'
                tree.valueofnode = temp.polygon
                tree.LeafClass = temp
                tree.type = 1
        else:
            maxdep = maxdep - 1
            # all atributes of this node must be a function.
            tree.numberChilds = 2
            tree.nodeID = thisnode
            tree.childs = []
            tree.strname = 'union2'
            tree.funcORter = 'func'
            tree.type = 1
            for i in range(2):
                temp1 = makeBlueTree(maxdep,ismaxdepth,thisnode,MaxX,MaxY)
                tree.childs.append(temp1[0])
                lastnode = temp1[1]
                thisnode = lastnode + 1
    else: #### Grow method.
        if maxdep == 0:
            # we must chose a terminal.
            LorU = random.randint(0,1) # 0 is the Ltree else is the Utree.
            if LorU == 0:
                xtype = random.randint(1,4)
                temp = ts.Lsub_tree(MaxX,MaxY,xtype)
                tree.strname = temp.strname
                tree.nodeID = thisnode
                tree.funcORter = 'ter'
                tree.type = 1
                tree.valueofnode = temp.polygon
                tree.LeafClass = temp
            else:
                xtype = random.randint(1,4)
                temp = ts.Usub_tree(MaxX,MaxY,xtype)
                tree.strname = temp.strname
                tree.nodeID = thisnode
                tree.funcORter = 'ter'
                tree.type = 1
                tree.valueofnode = temp.polygon
                tree.LeafClass = temp
        else:
            # we can choose randomly type of node(terminal node or function node)
            chose = random.randint(0,1)
            if chose == 1:
                # we must chose a terminal type for this node.
                LorU = random.randint(0,1) # 0 is the Ltree else is the Utree.
                if LorU == 0:
                    xtype = random.randint(1,4)
                    temp = ts.Lsub_tree(MaxX,MaxY,xtype)
                    tree.strname = temp.strname
                    tree.nodeID = thisnode
                    tree.funcORter = 'ter'
                    tree.type = 1
                    tree.valueofnode = temp.polygon
                    tree.LeafClass = temp
                else:
                    xtype = random.randint(1,4)
                    temp = ts.Usub_tree(MaxX,MaxY,xtype)
                    tree.strname = temp.strname
                    tree.nodeID = thisnode
                    tree.funcORter = 'ter'
                    tree.type = 1
                    tree.valueofnode = temp.polygon
                    tree.LeafClass = temp
            else:
                # chose the function node.
                maxdep = maxdep - 1
                # all atributes of this node must be a function.
                tree.numberChilds = 2
                tree.nodeID = thisnode
                tree.childs = []
                tree.strname = 'union2'
                tree.funcORter = 'func'
                tree.type = 1
                for i in range(2):
                    temp1 = makeBlueTree(maxdep,ismaxdepth,thisnode,MaxX,MaxY)
                    tree.childs.append(temp1[0])
                    lastnode = temp1[1]
                    thisnode = lastnode + 1

    tree.numNodes = thisnode - tree.nodeID + 1
    tree.maxNodeID = lastnode + 1
    return [tree,lastnode]

def synthesisBlueTree(tree):
    # This function is used for systhesis all polygons of tree, and update the valueofnode in function node in tree.

    if tree.childs == None or tree.synthesischeck == True: # case 6.
        if not tree.synthesischeck == True:
            tree.synthesischeck = True
    else:
        if (tree.childs[0].synthesischeck == False) and (tree.childs[1].synthesischeck == False) and (tree.childs[0].childs == None) and (tree.childs[1].childs==None):
            tree.valueofnode = union(tree.childs[0].valueofnode,tree.childs[1].valueofnode)
            #print('Union ',tree.nodeID)
            tree.synthesischeck = True     # case 1

        elif (tree.childs[0].synthesischeck == True) and (tree.childs[1].synthesischeck == True): # case 5
            tree.valueofnode = union(tree.childs[0].valueofnode,tree.childs[1].valueofnode)
            #print('Union ',tree.nodeID)
            tree.synthesischeck = True

        elif (tree.childs[0].synthesischeck == True) and (tree.childs[1].synthesischeck == False): # case 2.
            if tree.childs[1].childs == None:
                tree.valueofnode = union(tree.childs[0].valueofnode,tree.childs[1].valueofnode)
                #print('Union ',tree.nodeID)
                tree.synthesischeck = True
            else:
                synthesisBlueTree(tree.childs[1])
        elif (tree.childs[0].synthesischeck == False) and (tree.childs[1].synthesischeck == True): # case 3
            if tree.childs[0].childs == None:
                tree.valueofnode = union(tree.childs[0].valueofnode,tree.childs[1].valueofnode)
                #print('Union ',tree.nodeID)
                tree.synthesischeck = True
            else: 
                synthesisBlueTree(tree.childs[0])
        else: # case 4
            for i in range(len(tree.childs)):
                synthesisBlueTree(tree.childs[i])
    if (tree.synthesischeck == False):
        synthesisBlueTree(tree)
    return tree


def genFullBlueTree(tree):
    # NOTICE THAT: THIS FUNCTION RELATES TO NUMBER OF TERMINAL SET (now system has two terminals: lsubtree and Usubtree)
    # tree: this tree is the output of makeBlueTree function.
    if (tree.strname == 'L1') or (tree.strname == 'L2') or (tree.strname == 'L3') or (tree.strname == 'L4'):
        tree.strname = 'Lsubtree7'
        tree.funcORter = 'func'
        # branch 1 -- the rotation angle (0,90,180,270).
        #        2,3 -- the coordinate of shapesubtree.
        #        4,5,6,7 -- x1,x2,y1,y2 each of them relates with each of edge L shape.
        tree.childs = []
        for i in range(7):
            temp = node()
            if i == 0:
                temp.is_red_rota = True
            if i == 5 or i  == 6:
                temp.is_red_coords = True
            temp.valueofnode = round(random.uniform(-1,1),2)
            temp.strname = str(temp.valueofnode)
            temp.funcORter = 'ter'
            temp.isRed_TerminalNode = True
            temp.type = 0
            tree.childs.append(temp)
    elif (tree.strname == 'U1') or (tree.strname == 'U2') or (tree.strname == 'U3') or (tree.strname == 'U4'):
        tree.strname = 'Usubtree9'
        tree.funcORter = 'func'
        # branch 1 -- the rotation angle (0,90,180,270).
        #        2,3 -- the coordinate of shapesubtree.
        #        4,5,6,7,8,9 -- x1,x2,x3,y1,y2,y3 each of them relates with each of edge U shape.
        tree.childs = []
        for i in range(9):
            temp = node()
            if i == 0:
                temp.is_red_rota = True
            if i == 7 or i  == 8:
                temp.is_red_coords = True
            temp.valueofnode = round(random.uniform(-1,1),2)
            temp.strname = str(temp.valueofnode)
            temp.funcORter = 'ter'
            temp.isRed_TerminalNode = True
            temp.type = 0
            tree.childs.append(temp)
    else: # tree.strname == 'union'
        for i in range(len(tree.childs)):
            genFullBlueTree(tree.childs[i])

    return tree

def convertFullBluetree_to_oriBluetree(fullbluetree):
    # NOTICE THAT: THIS FUNCTION RELATES TO NUMBER OF TERMINAL SET (now system has two terminals: lsubtree and Usubtree)
    # fulbluetree (class type)
    # convert fullbluetree to original blutree to sinthesis.
    if fullbluetree.strname == 'Lsubtree7':
        fullbluetree.funcORter = 'ter'
        fullbluetree.childs = None
        fullbluetree.strname = fullbluetree.LeafClass.strname
        fullbluetree.numberChilds = 0
        #fullbluetree.valueofnode = fullbluetree.LeafClass.polygon
        fullbluetree.synthesischeck = False
    elif fullbluetree.strname == 'Usubtree9':
        fullbluetree.funcORter = 'ter'
        fullbluetree.childs = None
        fullbluetree.strname = fullbluetree.LeafClass.strname
        fullbluetree.numberChilds = 0
        #fullbluetree.valueofnode = fullbluetree.LeafClass.polygon
        fullbluetree.synthesischeck = False
    else: #fullbluetree.strname = 'union2':
        for i in range(2):
            fullbluetree.childs[i] = convertFullBluetree_to_oriBluetree(fullbluetree.childs[i])
    bluetree = fullbluetree
    bluetree = synthesisBlueTree(bluetree)
    return bluetree
def updateFullBlueTree(fullbluetree,MaxXY,updateType):
    # update all of nodes in fullbluetree after initing for gp operation.
    # updateType = 1 : initilize all terminal shapes correspondly.
    # updateType = 2 : change specified terminal shape correspondly after GP operation(like crossover, mutation,...).
    # updateType = 3 : change specified terminal shape (maxXY) after GP operation.
    # updateType = 4 : change all atributes of all terminal shapes in GP tree after using Lowlevel-optimizer. 
 
    if not ((updateType == 1) or (updateType == 2) or (updateType == 3) or (updateType == 4) or  (updateType == 5)):
        raise ValueError('the updateType must be 1 or 2 or 3.')
    if fullbluetree.strname == 'Lsubtree7':
        #print('Lsub, ID ',fullbluetree.nodeID)
        temp = []
        for i in range(7):
            temp.append(fullbluetree.childs[i].valueofnode)
            fullbluetree.childs[i].strname = str(fullbluetree.childs[i].valueofnode)
        fullbluetree.LeafClass.resestMaxXY(MaxXY[0],MaxXY[1])
        fullbluetree.LeafClass.initchange(temp)
        fullbluetree.valueofnode = fullbluetree.LeafClass.polygon
        fullbluetree.synthesischeck = False

    elif fullbluetree.strname == 'Usubtree9':
        #print('Usub, ID ',fullbluetree.nodeID)
        temp = []
        for i in range(9):
            temp.append(fullbluetree.childs[i].valueofnode)
            fullbluetree.childs[i].strname = str(fullbluetree.childs[i].valueofnode)
        fullbluetree.LeafClass.resestMaxXY(MaxXY[0],MaxXY[1])
        fullbluetree.LeafClass.initchange(temp)
        fullbluetree.valueofnode = fullbluetree.LeafClass.polygon
        fullbluetree.synthesischeck = False
        
    else: #fullbluetree.strname = 'union2':
        for i in range(2):
            fullbluetree.childs[i] = updateFullBlueTree(fullbluetree.childs[i],MaxXY,updateType)
    bluetree = fullbluetree
    #bluetree = synthesisBlueTree(bluetree)
    #del temp
    return bluetree

#def update_a_specified_node_in_FullBlueTree(fullbluetree)

def get_val_frombluetree(tree):
    temptree = convertFullBluetree_to_oriBluetree(tree)
    return temptree.valueofnode

############## 
           ### define function set.
def union(polygon1,polygon2):
    return gpd.overlay(polygon1,polygon2,how = 'union')


#def genFulltree()

def addsub3():
    # create randomly new substrate.
    temp = node()
    temp.strname = 'addsub3'
    temp.funcORter = 'func'
    temp.type =  3   # substrate type
    temp.numberChilds = 3
    temp.childs = []
    temp.valueofnode = []
    for i in range(3):
        temp2 = node()
        temp2.valueofnode = round(random.uniform(-1,1),2)
        temp2.strname = str(temp2.valueofnode)
        temp2.funcORter = 'ter'
        temp2.isRed_SubstrateNode = True
        temp2.isRed_TerminalNode = True
        temp2.type = 0   # red type
        if i == 2:
            temp2.special = True
        temp.childs.append(temp2)
        temp.valueofnode.append(temp2.valueofnode)
    return temp


def update_Depth_GP_tree(tree,current_dep):
    # update the maxdepth able of all node in a tree.
    tree.depth = current_dep
    if tree.childs != None:
        for i in range(len(tree.childs)):
            update_Depth_GP_tree(tree.childs[i],current_dep+1)

    
    
    
    
    
    
    
    
