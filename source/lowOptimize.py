import Helper as hp 
import initGlobal as init 
lowinit = init.lowlevel()

def lowlevel_optimizer(ind,state,pop_num ):
	print('running low-level optimizer for generation ',state.gen,'population ', pop_num)
	chromosome, subtree_chrom, IDlist = hp.getChrom() # get chromosome from tree and other atributes.

	num = len(chromosome) # number of values will be optimize.
	list_chrom = 
	