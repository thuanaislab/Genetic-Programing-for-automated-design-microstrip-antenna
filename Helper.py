# thuan.bb.hust@gmail.com 
##############################################################################################################
########## This file defines some functions to help GP processs.                                            ##
########## Functions included in this file are:                                                             ##
##										1	 drawtree(tree)  --- to draw tree structure.                    ##
##										2	 drawNodeIDs(tree)                                              ##
##                                      3    UpdateNodeIDs(tree,currentnode)                                ##
##                                      4    CreateNodeLists(tree,nodelist) -- nodelist is class type       ##
##                                      5    getSubtreeFromTree(tree,nodeID)                                ##
##                                      6    replaceSubtree(tree,subtree,nodeID)                            ##
##                                      7    calCurrentMaxDepth(node)                                       ##
##                                      8    calCurrentMaxDepth_fullTree(fulltree,nodeID)                   ##
##                                      9    updateMaxdepAble(tree,maxdepable)                              ##
##                                      10   calMaxdepAble(tree,maxBlue,nodeID)                             ##
##                                      11   calMaxdepBlueAble_fullTree(fulltree,maxBlue,nodeID)            ##
##                                      12   get_type_of_updating(node)                                     ##
##                                      13   getInfor_from_a_tree(tree,nodeID)                              ##
##                                      14   getBoundary(the_input)                                         ##
##                                      15   get2_suitable_edges_for_coaxial_cable(polygon,centroid)        ##
##                                      16   tree2str(tree)                                                 ##
##                                      17   getChrom(ind)                                                  ##
##                                      18   insert_chrom(tree,chromosome,subtree_chrom,IDlist)             ##
##############################################################################################################
import matplotlib.pyplot as plt 
import matplotlib.lines as ln 
import matplotlib.text as tx
import random
import copy
import GP as gp 
import numpy as np 

#########################################################################
##################### This part define DRAWTREE function ################
class State:
    pass
def drawtree(tree,*args):
    # DRAWTREE function is Created (2003) by SINTEF (hso@sintef.no,jtt@sintef.no,okl@sintef.no).
    # Modified by Sara Silva (sara@dei.uc.pt) in matlab version.
    # This function was rewrited by bachthuan in python version.
    # savefile to save the figure.
    
    fig,ax = plt.subplots()
    # first, count nodes.
    [tree,count] = walkTreeDepthFirst(tree,'countLeaves',[],-3,0,fig,ax)
    state = State()
    state.nodeCount = count
    state.yDist = -1
    state.x = []
    state.y = []
    # Positions leaves (euqally spaced)
    [tree,state] = walkTreeDepthFirst(tree,'positionLeaves',[],-3,state,fig,ax)
    # Position parents (midway between childs)
    [tree,state] = walkTreeDepthFirst(tree,[],'positionParents',-3,state,fig,ax)
    # Draw tree
    [tree,state] = walkTreeDepthFirst(tree,[],'drawNode',-3,state,fig,ax)
    maxX = max(state.x)
    minX = min(state.x)
    maxY = max(state.y)
    minY = min(state.y)
    ax.set_xlim(minX - 0.2,maxX + 0.2)
    ax.set_ylim(minY - 0.2,maxY + 0.2)
    plt.axis('off')
    if len(args):
        plt.savefig(args[0])

def walkTreeDepthFirst(tree,preDive,postDive,initialDepth,state,fig,ax):
    if preDive == 'countLeaves':
        [tree,state] = countLeaves(tree,initialDepth,state)
        #print(state)
    if preDive == 'positionLeaves':
        [tree,state] = positionLeaves(tree,initialDepth,state)
    if not tree.childs == None:
        for i in range(len(tree.childs)):
            [tree.childs[i],state] = walkTreeDepthFirst(tree.childs[i],preDive,postDive,initialDepth+1,state,fig,ax)
    if postDive == 'positionParents':
        [tree,state] = positionParents(tree,initialDepth,state)
    if postDive == 'drawNode':
        [tree,state] = drawNode(tree,initialDepth,state,fig,ax)
    if postDive == 'drawNodeID':
        [tree,state] = drawNodeID(tree,initialDepth,state,fig,ax)
    return [tree,state]

def countLeaves(tree, depth, count):
    if tree.childs == None:
        tree.index = count
        count = count + 1
    return [tree, count]

def positionLeaves(tree, depth, state):
    if tree.childs == None:
        if state.nodeCount <= 1:
            tree.X = 0
        else:
            tree.X = tree.index / (state.nodeCount - 1)
        tree.Y = depth * state.yDist
    return [tree,state]

def positionParents(tree, depth, state):
    if not tree.childs == None:
        x = []
        for i in range(len(tree.childs)):
            child = tree.childs[i]
            x.append(child.X)
        tree.X = mean(x)
        tree.Y = depth * state.yDist
    return [tree,state]

def drawNode(tree, depth, state,fig,ax):
    if not tree.childs == None:
        for i in range(len(tree.childs)):
            child = tree.childs[i]
            temp1 = ln.Line2D([tree.X,child.X],[tree.Y,child.Y])
            ax.add_line(temp1)
        temp2 = ln.Line2D([tree.X,tree.X],[tree.Y,tree.Y],color= 'red',marker = '^',markersize = 8)
        ax.add_line(temp2)
        opText = tree.strname
        text1 =  tx.Text(tree.X,tree.Y,opText)
        state.x.append(tree.X)
        state.y.append(tree.Y)
        #print('tree.X',tree.X,'  tree.Y',tree.Y)
        ax.add_artist(text1)
    else:
        opText = tree.strname
        #opText = 'R'
        temp3 = ln.Line2D([tree.X,tree.X],[tree.Y,tree.Y],marker = '.',markersize = 8)
        ax.add_line(temp3)
        text2 = tx.Text(tree.X,tree.Y,opText,horizontalalignment= 'center',verticalalignment = 'top')
        ax.add_artist(text2)
        state.x.append(tree.X)
        state.y.append(tree.Y)
    return [tree,state]


def mean(lst):
    return sum(lst)/len(lst)
######## ending of definition of drawtree function.
#########################################################################################################################################

def drawNodeIDs(tree):
    # DRAWTREE function is Created (2003) by SINTEF (hso@sintef.no,jtt@sintef.no,okl@sintef.no).
    # Modified by Sara Silva (sara@dei.uc.pt) in matlab version.
    # This function was rewrited by bachthuan in python version.

    fig,ax = plt.subplots()
    # first, count nodes.
    [tree,count] = walkTreeDepthFirst(tree,'countLeaves',[],-3,0,fig,ax)
    state = State()
    state.nodeCount = count
    state.yDist = -1
    state.x = []
    state.y = []
    # Positions leaves (euqally spaced)
    [tree,state] = walkTreeDepthFirst(tree,'positionLeaves',[],-3,state,fig,ax)
    # Position parents (midway between childs)
    [tree,state] = walkTreeDepthFirst(tree,[],'positionParents',-3,state,fig,ax)
    # Draw tree
    [tree,state] = walkTreeDepthFirst(tree,[],'drawNodeID',-3,state,fig,ax)
    maxX = max(state.x)
    minX = min(state.x)
    maxY = max(state.y)
    minY = min(state.y)
    ax.set_xlim(minX - 0.2,maxX + 0.2)
    ax.set_ylim(minY - 0.2,maxY + 0.2)
    plt.axis('off')
    plt.show()

def drawNodeID(tree, depth, state,fig,ax):
    if not tree.childs == None:
        for i in range(len(tree.childs)):
            child = tree.childs[i]
            temp1 = ln.Line2D([tree.X,child.X],[tree.Y,child.Y])
            ax.add_line(temp1)
        temp2 = ln.Line2D([tree.X,tree.X],[tree.Y,tree.Y],color= 'red',marker = '^',markersize = 8)
        ax.add_line(temp2)
        opText = str(tree.nodeID)
        text1 =  tx.Text(tree.X,tree.Y,opText)
        state.x.append(tree.X)
        state.y.append(tree.Y)
        #print('tree.X',tree.X,'  tree.Y',tree.Y)
        ax.add_artist(text1)
    else:
        opText = str(tree.valueofnode)
        temp3 = ln.Line2D([tree.X,tree.X],[tree.Y,tree.Y],marker = '.',markersize = 8)
        ax.add_line(temp3)
        text2 = tx.Text(tree.X,tree.Y,opText,horizontalalignment= 'center',verticalalignment = 'top')
        ax.add_artist(text2)
        state.x.append(tree.X)
        state.y.append(tree.Y)
    return [tree,state]


#################################################################################################################################
def UpdateNodeIDs(tree,currentnode):
    # update the node ID.
    currentnode = currentnode + 1
    tree.nodeID = currentnode
    if tree.childs != None:
        for i in range(len(tree.childs)):
            currentnode = UpdateNodeIDs(tree.childs[i],currentnode)
    return currentnode

#################################################################################################################################
def ResetSynthesischeck(tree,currentnode):
    tree.synthesischeck = False
    currentnode = currentnode + 1
    if tree.childs != None:
        for i in range(len(tree.childs)):
            currentnode = ResetSynthesischeck(tree.childs[i],currentnode)
    return currentnode

#################################################################################################################################
class nodelist:
    # to save all of nodeID of all node types.
    def __init__(self):
        self.redlist = []
        self.type_of_each_red = [] # save type of each of red node. like: substrate_x,y,.. rotation or coordinates,...
        #self.subtree_redlist = []  # sav
        self.subbluelist = []
        self.bluelist = []
        self.substratelist = []
        self.gensublist = []
        self.genpatlist = []
#####
def CreateNodeLists(tree,nodes):
    # Create node class from an already existing tree.
    # Members of node class include:
    #   redlist = list of nodes (under red type, type = 0)
    #   subbluelist = list of nodes under subblue type (type = 1)
    #   bluelist = list of nodes under bluetree type (type = 2)
    #   substratelist = list of nodes under substrate type (type = 3)
    #   gensublist = list of nodes under gensub type (type = 4)
    #   genpatlist = list of nodes under genpat type (type = 5).
    if tree.type == 0:
        # red type.
        nodes.redlist.append(tree.nodeID)
        if tree.isRed_SubstrateNode:
            if not tree.special:
                nodes.type_of_each_red.append('sub_oxy')
            else:
                nodes.type_of_each_red.append('sub_oz')
        else:
            if tree.is_red_rota:
                nodes.type_of_each_red.append('red_rot')
            elif tree.is_red_coords:
                nodes.type_of_each_red.append('red_coords')
            else:
                nodes.type_of_each_red.append('red')

    if tree.type == 1:
        # subblue type.
        nodes.subbluelist.append(tree.nodeID)
    if tree.type == 2:
        # blue type.
        nodes.bluelist.append(tree.nodeID)
    if tree.type == 3:
        # substrate type.
        nodes.substratelist.append(tree.nodeID)
    if tree.type == 4:
        # gensub type.
        nodes.gensublist.append(tree.nodeID)
    if tree.type == 5:
        # genpat type.
        nodes.genpatlist.append(tree.nodeID)

    if tree.childs != None:
        # search each branch of this node.
        for i in range(len(tree.childs)):
            nodes = CreateNodeLists(tree.childs[i],nodes)

    return nodes

#######################################################################################################
def getNumberFromList(alist):
    # get a random number from a list.
    temp = round(random.uniform(0,len(alist)-1))
    return alist[temp]
#######################################################################################################
def getSubtreeFromTree(tree,nodeID):
    # Notice: the tree input need be deepcopyed before applying in this function to finde subtree.
    subtree = tree
    # print(subtree)
    # print(subtree.nodeID)
    if tree.nodeID == nodeID: # node found.
        return subtree
    if tree.childs != None: # keep traversing tree to find specified node.
        for i in range(len(tree.childs)):
            subtree = getSubtreeFromTree(tree.childs[i],nodeID)
            #print('subtree_________:',subtree)
            if not subtree == None:
                if subtree.nodeID == nodeID: # node found, stop to find that node.
                    return subtree
####
def replaceSubtree(tree,subtree,nodeID):
    # replace subtree of tree with the new subtree.
    # nodeID: nodeID of the tree.
    if not tree == None:
        if tree.nodeID == nodeID:
            tree = subtree
        # nodeID of the tree has been not found.
        else:
            if tree.childs != None: # searching for other branch.
                for i in range(len(tree.childs)):
                    tree.childs[i] = replaceSubtree(tree.childs[i],subtree,nodeID)
    return tree 
#################################################################################################
def calCurrentMaxDepth(node):
    # function to calculate the maxdep of a root node input..
    # notice: the tree input must have less than two branchs
    if node.childs == None:
        dep = 0
    elif len(node.childs) == 1:
        dep = calCurrentMaxDepth(node.childs[0]) + 1
    else:
        dep = max(calCurrentMaxDepth(node.childs[0]),calCurrentMaxDepth(node.childs[1])) + 1
    return dep 
#####
def calCurrentMaxDepth_fullTree(fulltree,nodeID):
    # calculate the current maxdepth of a specified blue node in full tree.
    # notice: this function only uses for blue tree.
    fullbluetree = copy.deepcopy(fulltree.childs[1].childs[0].childs[0])
    bluetree = gp.convertFullBluetree_to_oriBluetree(fullbluetree)
    node = getSubtreeFromTree(bluetree,nodeID)
    del fullbluetree
    del bluetree
    return calCurrentMaxDepth(node)
##################################################################################################  
def updateMaxdepAble(tree,maxdepable):
    # update the maxdepth able of all node in a tree.
    tree.maxdepable = maxdepable
    if tree.childs != None:
        for i in range(len(tree.childs)):
            updateMaxdepAble(tree.childs[i],maxdepable-1)

#####
def calMaxdepAble(tree,maxBlue,nodeID):
    # calculate the maxdepable of a specified node in a tree.
    # notice: this funtion just uses for original blue tree(not fullbluetree).
    #           tree: original blue tree.
    temptree = copy.deepcopy(tree)
    updateMaxdepAble(temptree,maxBlue)
    temp1 = getSubtreeFromTree(temptree,nodeID)
    if temp1 == None:
        raise ValueError('can not find the nodeID in the tree input')
    del temptree
    return temp1.maxdepable
#####
def calMaxdepBlueAble_fullTree(fulltree,maxBlue,nodeID):
    # calculate the maxdepable of a specified blue node in a full tree.
    # notice: this function only uses for blue tree.
    fullbluetree = copy.deepcopy(fulltree.childs[1].childs[0].childs[0])
    bluetree = gp.convertFullBluetree_to_oriBluetree(fullbluetree)
    del fullbluetree
    return calMaxdepAble(bluetree,maxBlue,nodeID)

#######################################################################################
def get_type_of_updating(node):
    if node.isRed_SubstrateNode:
        if node.special:
            return 0
        else:
            return 1 # the changing after using GP operator is at substrate red node.
    elif node.isRed_TerminalNode:
        return 2 # __________________________________________ terminal red node.
    elif (node.strname == 'union2') or (node.strname == 'Lsubtree7') or (node.strname == 'Usubtree9'):
        return 3 #___________________________________________ subblue tree node(like 'union',etc).
    elif node.strname == 'addsub3':
        return 4 #___________________________________________ 'addsub3' node.
    elif node.strname == 'bluetree1':
        return 5 # __________________________________________ 'bluetree1' node.
    elif node.strname == 'genpat1':
        return 6 #___________________________________________ 'genpat1' node.
    elif node.strname == 'gensub1':
        return 7 #___________________________________________ 'gensub1' node.
    else:
        raise ValueError('can not find any of changing type after using GP operators')
###############################################################################################################
def getInfor_from_a_tree(tree,nodeID):
    # to get the strname of the specified node in a tree.
    return getSubtreeFromTree(tree,nodeID).strname


def get_all_para_for_hfss(GP_pro):
    # this function gets all parameters from a GP_tree to draw antenna through hfss software.
    result = get_all_basics_subtree_GP(GP_pro)
    length = len(result[1])
    parameters = [] # save all of coordinates of each polygon.

    for i in range(length):
        lenxy,_ = result[1][i].shape
        tempPara = np.zeros((lenxy+1,3)) # save all the vertexes of a polygon.
        for j in range(lenxy):
            tempPara[j][0] = result[1][i][j,0]
            tempPara[j][1] = result[1][i][j,1]
        tempPara[lenxy][0] = tempPara[0][0]
        tempPara[lenxy][1] = tempPara[0][1]
        parameters.append(tempPara)

    XY_centroids = GP_pro.childs[1].valueofnode.total_bounds # will include all centroid coordinates of all polygon in a specified GP_tree.
    X_centroids = [XY_centroids[0],XY_centroids[2]]
    Y_centroids = [XY_centroids[1],XY_centroids[3]]
    x_centroid = sum(X_centroids)/2
    y_centroid = sum(Y_centroids)/2
    centroid = [x_centroid,y_centroid] # save the centroid of entire polygons.
    # GP_pro.childs[0].valueofnode contains the size of substrate.
    return [GP_pro.childs[0].valueofnode,parameters,centroid,result[2],result[0]]

#####################################################################################################################
def getBoundary(the_input):
    # this function to get the boundary of a polygon in a GP_prog.
    # the_input: is the second output of the get_all_para_for_hfss function.
    # referece: https://stackoverflow.com/questions/13746284/merging-multiple-adjacent-rectangles-into-one-polygon
    points = []

    for i in range(len(the_input)):
        for j in range(len(the_input[i])-1):
            temp = (the_input[i][j][0],the_input[i][j][1])
            if temp in points:
                #print('temp ',temp)
                ind = points.index(temp)
                xxxx=points.pop(ind)
                #print('xxx',xxxx)
                #print('remove')
            else:
                points.append(temp)

    #temp = points
    sort_x = sorted(points)
    #sort_y = sorted(points, key=cmp_to_key(y_then_x))
    temp_sort = []
    for i in range(len(points)):
        temp_y = [points[i][1],points[i][0]]
        temp_sort.append(temp_y)

    sottt_y = sorted(temp_sort)

    sort_y = []
    for i in range(len(points)):
        sort_y.append((sottt_y[i][1],sottt_y[i][0]))
    edges_h = {}
    edges_v = {}

    i = 0
    while i < len(points):
        curr_y = sort_y[i][1]
        while i < len(points) and sort_y[i][1] == curr_y: #6chars comments, remove it
            #print('i ',i)
            edges_h[sort_y[i]] = sort_y[i + 1]
            edges_h[sort_y[i + 1]] = sort_y[i]
            i += 2
    i = 0
    while i < len(points):
        curr_x = sort_x[i][0]
        while i < len(points) and sort_x[i][0] == curr_x:
            edges_v[sort_x[i]] = sort_x[i + 1]
            edges_v[sort_x[i + 1]] = sort_x[i]
            i += 2

    # Get all the polygons.
    p = []
    while edges_h:
        # We can start with any point.
        polygon = [(edges_h.popitem()[0], 0)]
        while True:
            curr, e = polygon[-1]
            if e == 0:
                next_vertex = edges_v.pop(curr)
                polygon.append((next_vertex, 1))
            else:
                next_vertex = edges_h.pop(curr)
                polygon.append((next_vertex, 0))
            if polygon[-1] == polygon[0]:
                # Closed polygon
                polygon.pop()
                break
        # Remove implementation-markers from the polygon.
        poly = [point for point, _ in polygon]
        for vertex in poly:
            if vertex in edges_h: edges_h.pop(vertex)
            if vertex in edges_v: edges_v.pop(vertex)

        p.append(poly)
    '''
    for poly in p:
        #print (poly)
        x = []
        y = []
        for i in range(len(poly)):
            x.append(poly[i][0])
            y.append(poly[i][1])
        x.append(x[0])
        y.append(y[0])
        plt.plot(x,y)
        plt.show()'''
    return p

def get2_suitable_edges_for_coaxial_cable(polygon,centroid):
    # this funtion gets two suitable edges of the patch to help to draw the coaxial cable.
    # return 2 suitable edges. 
    # note: polygon is the list of the boundaries of it's patch.
    polygon = polygon[0]
    if polygon[0][0] != polygon[1][0]:
        # get oy edges.
        oy_centroid = centroid[1]
        ii = 1 #...
        two_oy_edges = []
        for i in range(int(len(polygon)/2-1)):
            temp1 = polygon[ii]
            temp2 = polygon[ii + 1]
            if oy_centroid >= min(temp1[1],temp2[1]) and oy_centroid <= max(temp1[1],temp2[1]): # suitable edge.
                if temp1[1] >= temp2[1]: # sort in oder ascending of value of y axis.
                    two_oy_edges.append((temp2,temp1))
                else:
                    two_oy_edges.append((temp1,temp2))
            ii = ii + 2
            if ii == len(polygon):
                break
        temp1 = polygon[ii]
        temp2 = polygon[0]
        if oy_centroid >= min(temp1[1],temp2[1]) and oy_centroid <= max(temp1[1],temp2[1]): # suitable edge.
            if temp1[1] >= temp2[1]:
                two_oy_edges.append((temp2,temp1))
            else:
                two_oy_edges.append((temp1,temp2))
    else:
        oy_centroid = centroid[1]
        ii = 0 # ...
        two_oy_edges = []
        #print(len(polygon)/2)
        for i in range(int(len(polygon)/2)):
            temp1 = polygon[ii]
            temp2 = polygon[ii + 1]
            if oy_centroid >= min(temp1[1],temp2[1]) and oy_centroid <= max(temp1[1],temp2[1]): # suitable edge.
                if temp1[1] >= temp2[1]:
                    two_oy_edges.append((temp2,temp1))
                else:
                    two_oy_edges.append((temp1,temp2))
            ii = ii + 2
    two_oy_edges = sorted(two_oy_edges)
    return two_oy_edges
###################################################################################################
def tree2str(tree):
  #  TREE2STR Translates a GPLAB algorithm tree into a string.
  #TREE2STR(TREE) returns the string represented by the tree,
  #in valid Matlab notation, ready for evaluation.

  # Input arguments:
  #   TREE - the tree to translate (class nest class type)
  # Output arguments:
  #   STRING - the string respresented by the tree (string)

  # See also MAKETREE

  # Copyright (C) 2003-2007 Sara Silva (sara@dei.uc.pt)
  # This file is part of the GPLAB Toolbox
    strname = tree.strname
    strname = str(strname)
    args = []
    if tree.childs != None:
        for i in range(len(tree.childs)):
            args.append(tree2str(tree.childs[i]))
    if not args == []:
        strname = strname + '(' + implode(args,',') + ')'
    return strname

def implode(pieces,delimiter):
    '''%IMPLODE    Joins strings with delimiter in between.
    %   IMPLODE(PIECES,DELIMITER) returns a string containing all the
    %   strings in PIECES joined with the DELIMITER string in between.
    %
    %   Input arguments:
    %      PIECES - the pieces of string to join (cell array), each cell is a piece
    %      DELIMITER - the delimiter string to put between the pieces (string)
    %   Output arguments:
    %      STRING - all the pieces joined with the delimiter in between (string)
    %
    %   Example:
    %      PIECES = {'ab','c','d','e fgh'}
    %      DELIMITER = '->'
    %      STRING = IMPLODE(PIECES,DELIMITER)
    %      STRING = ab->c->d->e fgh
    %
    %   See also EXPLODE, STRCAT
    %
    %   Copyright (C) 2003-2007 Sara Silva (sara@dei.uc.pt)
    %   This file is part of the GPLAB Toolbox'''
    if pieces == []:
        string = ''
    else:
        string = pieces[0]

    l = len(pieces)
    p = 0
    while p < (l-1): # more than one piece to join with the delimiter, the interesting case
        p = p + 1
        currPiece = str(pieces[p])
        string = string + delimiter + currPiece
    return string
##########################################################################################################
def getChrom(ind):
    # getChrom function gets all values of red node in GP tree.
    # where: ind is an individual, it includes tree form and nodelist type.
    # in this function the rotation red node will be not extracted.
    tree = copy.deepcopy(ind.tree)
    nodelist = copy.deepcopy(ind.nodelist)
    IDlist = [] # save all id of the nodes will be extracted.
    for i in range(len(nodelist.redlist)):
        if not (nodelist.type_of_each_red[i] == 'red_rot'):
            IDlist.append(nodelist.redlist[i])
    #print(IDlist)
    #hp.drawNodeIDs(tree)
    subtree_chrom = [] # save all subtree of each red node that will be extracted.
    chromosome = []    # save all value of each node that will be extracted.
    
    for i in range(len(IDlist)):
        subtree_chrom.append(getSubtreeFromTree(tree,IDlist[i]))
        chromosome.append(subtree_chrom[i].valueofnode)

    del tree 
    del nodelist
    return chromosome, subtree_chrom, IDlist
###########################################################################################################
def insert_chrom(or_tree,chromosome,subtree_chrom_,IDlist):
    # insert_chrom function is used to insert the red nodes into suitable tree.
    #   tree: is the tree need be inserted after the red nodes extracted.
    #   chromosome: is the list that saves all extracted values of red nodes.
    #   subtree_chrom: is the list that save all extracted red nodes.
    #   IDlist: is the list that save all ID of the extracted node.
    #       Note: The tree is used as the input of this function need be deepcopy before.
    import initGlobal as init
    Sub = init.Sub()
    if init.Re_trainning:
        import update_state as us 
        AnT = init.AnT()
        #Sub = init.Sub()
        L   = init.L()
        U   = init.U()
        low = init.lowlevel()
        GP = init.GP()
        #path = us.load_temporary_path()
        us.update_all_saved_parameters(AnT, Sub, L, U, GP, low)



    tree = copy.deepcopy(or_tree)
    subtree_chrom = copy.deepcopy(subtree_chrom_)
    #drawtree(tree)

    length = len(chromosome)

    for i in range(length):
        subtree_chrom[i].valueofnode = chromosome[i] # insert all values into subtree_chrom before insert to GP_tree(tree).

    for i in range(len(chromosome)):
        tree = replaceSubtree(tree,subtree_chrom[i],IDlist[i])
        #drawNodeIDs(tree)
    ## update tree (substrate layer).
    UpdateNodeIDs(tree,0)
    #drawtree(tree)
    tree.childs[0].childs[0].valueofnode = []
    for i in range(len(tree.childs[0].childs[0].childs)):   # resave the sizes of substrate layer into addsub3 node.
        tree.childs[0].childs[0].valueofnode.append(tree.childs[0].childs[0].childs[i].valueofnode)
    temp = tree.childs[0].childs[0].valueofnode # save the sizes of substrate layer into TEMP variable.
    
    tree.childs[0].valueofnode = []
    for i in range(3):
        # calculate all of the real substrate's parameters.
        if i == 0:
            temp2 = round(((temp[i]+1)/2)*(Sub.rangeOx[1] - Sub.rangeOx[0]) + Sub.rangeOx[0],4) # Ox edge
        elif i == 1:
            temp2 = round(((temp[i]+1)/2)*(Sub.rangeOy[1] - Sub.rangeOy[0]) + Sub.rangeOy[0],4) # Oy edge.
        else:
            temp2 = round(((temp[i]+1)/2)*(Sub.rangeOz[1] - Sub.rangeOz[0]) + Sub.rangeOz[0],4) # Oz edge.
        tree.childs[0].valueofnode.append(temp2)

    # Secondly create patterns.
    MaxX = tree.childs[0].valueofnode[0] - Sub.decrease ### real MaxX,Y are decreased 1mm before to create
                                                  # any pattern unit(like L1,U1,U2,...).
    MaxY = tree.childs[0].valueofnode[1] - Sub.decrease
    Zsize = tree.childs[0].valueofnode[2]
    tree.substrate_size = [MaxX+Sub.decrease,MaxY+Sub.decrease,Zsize]
    MaxXY = [MaxX-Sub.decrease,MaxY-Sub.decrease]
    ResetSynthesischeck(tree.childs[1].childs[0].childs[0],tree.childs[1].childs[0].childs[0].nodeID)
    tree.childs[1].childs[0].childs[0] = gp.updateFullBlueTree(tree.childs[1].childs[0].childs[0],MaxXY,4)
    tree.childs[1].childs[0].valueofnode = gp.get_val_frombluetree(copy.deepcopy(tree.childs[1].childs[0].childs[0]))
    tree.childs[1].valueofnode = tree.childs[1].childs[0].valueofnode

    del subtree_chrom
    del temp
    del temp2

    return tree
######################################################################################################
def help_get_all_basic_subtree_GP(fullbluetree,result):
    # this function to help get_all_basics_subtree_GP work.
    # the result must be a list.
    if fullbluetree.strname == 'Lsubtree7':
        result[0].append(fullbluetree.LeafClass.strname)
        result[1].append(fullbluetree.LeafClass.X)
        result[2].append(fullbluetree.LeafClass.polygon)
    elif fullbluetree.strname == 'Usubtree9':
        result[0].append(fullbluetree.LeafClass.strname)
        result[1].append(fullbluetree.LeafClass.X)
        result[2].append(fullbluetree.LeafClass.polygon)
    else: #fullbluetree.strname = 'union2':
        for i in range(2):
            result = help_get_all_basic_subtree_GP(fullbluetree.childs[i],result)
    return result
def get_all_basics_subtree_GP(GP_pro):
    # This function find all coordinates of each basic subtree like U,L in the GP_prog tree. 
    bluetree = copy.deepcopy(GP_pro.childs[1].childs[0].childs[0])
    result = [[],[],[]]
    result = help_get_all_basic_subtree_GP(bluetree,result)
    del bluetree
    return result
