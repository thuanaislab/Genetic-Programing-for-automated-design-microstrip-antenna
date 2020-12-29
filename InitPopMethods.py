############################################################################
# This file defines some methods to init population in GP process.
#                       Include: growinit() -- grow method.
#                                fullinit() -- full method.
#                                ramphaft() -- ramp of half method.
# bachthuan03111997@gmail.com - 2018
import GP_prog
import Helper as hp 
class Individual:
    pass
def restruct_ind(tree,ID):
    # this function restructs an existed individual. 
    ind = Individual()
    ind.id = ID 
    ind.tree = tree
    temp = hp.nodelist()
    ind.nodelist = hp.CreateNodeLists(tree,temp)
    ind.fitness = []
    ind.ReturnLoss = [] 
    ind.polygon = ind.tree.valueofnode

    return ind 

def NewInd(lastid,maxSub,maxPat,maxBlue,ismaxdepth):
    # Create new individual for a population.

    ## INPUT: 
        # LASTID the last identifier used for a indiviual(integer).
        # MAXDEP the maximum of depth in that individual(integer).
        # ISMAXDEPTH whether Individual is created with maxdep of all or not(boolean).
        # MaxX is the maximum length of X axis.
        # MaxY is the maximum length of Y axis.
    ## OUTPUT:
        # [ind,lastid]

        ind = Individual()
        LastID = lastid + 1
        ind.id = LastID
        tree = GP_prog.makeGP_prog(maxSub,maxPat,maxBlue,ismaxdepth)
        hp.UpdateNodeIDs(tree,0)
        ind.tree = tree
        temp = hp.nodelist()
        ind.nodelist = hp.CreateNodeLists(tree,temp)
        ind.fitness = []
        ind.ReturnLoss = [] 
        ind.polygon = ind.tree.valueofnode

        return [ind,LastID]

def growinit(popsize,maxSub,maxPat,maxBlue,lastid):
    # POPSIZE: the number of individuals need be created.
    # MAXDEP the maximum of depth in that individual(integer).
    # MaxX is the maximum length of X axis.
    # MaxY is the maximum length of Y axis.
    pop = []
    for i in range(popsize):
        [ind,lastid] = NewInd(lastid,maxSub,maxPat,maxBlue,False)
        pop.append(ind)
    return [pop,lastid]

def fullinit(popsize,maxSub,maxPat,maxBlue,lastid):
    pop = []
    for i in range(popsize):
        [ind,lastid] = NewInd(lastid,maxSub,maxPat,maxBlue,True)
        pop.append(ind)
    return [pop,lastid]

def rampinit(popsize,maxSub,maxPat,maxBlue,rate):
    # Rate: is the rate of number grow ind in all popsize.
    growsize = int(popsize*rate)
    fullsize = popsize - growsize
    pop = []
    [growpop,lastid] = growinit(growsize,maxSub,maxPat,maxBlue,0)
    for i in range(len(growpop)):
        pop.append(growpop[i])
    [fullpop,lastid] = fullinit(fullsize,maxSub,maxPat,maxBlue,lastid)
    for i in range(len(fullpop)):
        pop.append(fullpop[i])

    return pop 

        
