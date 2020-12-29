# bachthuan03111997@gmail.com - 2018
import GPoperators as op 
import initGlobal as init
import InitPopMethods as initpop
import Helper as hp
from genscript import genscript
import matplotlib.pyplot as plt 
# from testFunctionFitness import fitness
import os
import time
import shutil
import DS_lowOptimize as dslow
import ANN_lowOptimize as anlow 

import helpRunning as hpr 
######################################################### MAIN ####################################################33
lowlevel = init.lowlevel()
first_time = time.time()
inAnT = init.AnT() # get the essential parameters of antenna from initglobal.py 
mydir = inAnT.tmpTab
mydir_hfss = inAnT.tmpDir
filelist = [ f for f in os.listdir(mydir) if f.endswith(".tab") ]
for f in filelist:    # delete all before files.
    os.remove(os.path.join(mydir, f))

filelist = [ f for f in os.listdir(mydir_hfss) if (f.endswith(".hfss") or f.endswith(".vbs") or f.endswith(".txt"))]
for f in filelist: # delete all before files.
    os.remove(os.path.join(mydir_hfss, f))


class state: # define a state object to save some necessary results.
    pass 
#import os
state.lowlevel = False
state.best_hisFitness = []
inGP = init.GP() # get the essential parameters of GP process from initGlobal.py file. note: this's global parameter.
gen = 1 # current generation.

pop = initpop.rampinit(inGP.numpop,inGP.maxSub, inGP.maxPat, inGP.maxBlue,inGP.rate) #-- init population by rampinit method.



global_name = inAnT.tmpDir + inAnT.Antenna_Name + '_gen_'
global_tabname = inAnT.tmpTab + inAnT.Antenna_Name + '_gen_' 

for iii in range(inGP.numgen):
	state.gen = gen 
	# before run the next generation, all of the tab file need be deleted.
	filelist = [ f for f in os.listdir(mydir) if f.endswith(".tab") ]
	for f in filelist:
		os.remove(os.path.join(mydir, f))
	# be fore run the next gen, all of the hfss file in temp need be deleted.
	filelist = [ f for f in os.listdir(mydir_hfss) if (f.endswith(".hfss") or f.endswith(".vbs") or f.endswith(".txt"))]
	for f in filelist: # delete all before files.
		os.remove(os.path.join(mydir_hfss, f))
	## generate all scripts.
	print('generating ',len(pop), ' scripts at generation ',gen)

	if iii == 0: # this case is the initial part.
		for i in range(len(pop)):
			temp = pop[i].tree
			[Substrate,polygons,centroid,poly_list, poly_list_type] = hp.get_all_para_for_hfss(temp) # get necessary parameters for genscript function.
			name = global_name + str(gen) + '_pop_' + str(i) # name of directory would
																			# be used to save .vbs and .hfss file.
			tabname = global_tabname + str(gen) + '_pop_' + str(i) # name of directory
																			# would be used to save .tab file. 
			genscript(Substrate,polygons,centroid,name + '.vbs',tabname,name + '.hfss',poly_list,poly_list_type)
	else:
		# this case is the next part of initial part.
		for i in range(numRepro,len(pop)):
			temp = pop[i].tree
			[Substrate,polygons,centroid,poly_list, poly_list_type] = hp.get_all_para_for_hfss(temp) # get necessary parameters for genscript function.
			name = global_name + str(gen) + '_pop_' + str(i) # name of directory would
																			# be used to save .vbs and .hfss file.
			tabname = global_tabname + str(gen) + '_pop_' + str(i) # name of directory
																			# would be used to save .tab file. 
			genscript(Substrate,polygons,centroid,name + '.vbs',tabname,name + '.hfss',poly_list,poly_list_type)
	print('genscript is done.')

	## Run all scripts to get .tab file.
	nameDir = inAnT.tmpDir + inAnT.Antenna_Name + '_gen_' + str(gen) + '_pop_'  # file name direction of the vbs file.
	if gen == 1:
		# This case is initial part.
		hpr.RunPopScript(len(pop),nameDir,0,1,state)
	else:
		# other.
		hpr.RunPopScript(len(pop),nameDir,numRepro,1,state)
	

	################################################

	### evaluate and assign the fitness of each model.
	############################################################################################3
	nameDir_tab = inAnT.tmpTab + inAnT.Antenna_Name + '_gen_' + str(gen) + '_pop_' # file name directory to tab file.
	if gen == 1:
		for i in range(len(pop)):
			spec_nameDir_tab = nameDir_tab + str(i) + '.tab'
			[pop[i].fitness, pop[i].ReturnLoss,p,q] = hpr.assignFitness(spec_nameDir_tab,gen) # update the fitness of each individual.
			if pop[i].fitness < inGP.desired_fitness:
				shutil.move(global_name + str(gen) + '_pop_' + str(i) + '.hfss', inAnT.resultsDir)
				#hp.drawtree(pop[i].tree,inAnT.resultsDir + '_gen_' + str(gen) + '_pop_' + str(i))
				f = open(inAnT.resultsDir + '_gen_' + str(gen) + '_pop_' + str(i) + '.txt','w')
				f.write(hp.tree2str(pop[i].tree))
				f.write('fitness: ' + str(pop[i].fitness))
				f.write('time: ' + str((time.time() - first_time)/60))
				if p:
					f.write("_____exist best fitness")
					if q:
						f.write("___ that is better than overcome_desired")
				f.close()
	else:
		for i in range(numRepro,len(pop)):
			spec_nameDir_tab = nameDir_tab + str(i) + '.tab'
			[pop[i].fitness, pop[i].ReturnLoss,p,q] = hpr.assignFitness(spec_nameDir_tab,gen) # update the fitness of each individual.
			if pop[i].fitness < inGP.desired_fitness:
				shutil.move(global_name + str(gen) + '_pop_' + str(i) + '.hfss', inAnT.resultsDir)
				#hp.drawtree(pop[i].tree,inAnT.resultsDir + '_gen_' + str(gen) + '_pop_' + str(i))
				f = open(inAnT.resultsDir + '_gen_' + str(gen) + '_pop_' + str(i) + '.txt','w')
				f.write(hp.tree2str(pop[i].tree))
				f.write('fitness: ' + str(pop[i].fitness))
				f.write('time: ' + str((time.time() - first_time)/60))
				if p:
					f.write("_____exist best fitness")
					if q:
						f.write("___ that is better than overcome_desired")
				f.close()
	#testxxxx = []
	#testyyyy = []
	##############################################################################
	#########################################################################################################################
	########################################################## LOWLEVEL OPTIMIZER ###########################################
	if lowlevel.lowoptimize:
		print("RUNNING LOWLEVEL OPTIMIZER ......")
		for i in range(len(pop)):
			state.population_num = i 
			pop[i] = dslow.lowlevel_optimizer(pop[i],state,i)


		
	state.curFitness = [] # to save all current fitness.
	for i in range(len(pop)):
		#testxxxx.append(i)
		#testyyyy.append(pop[i].fitness)
		state.curFitness.append(pop[i].fitness) # save all of the fitness in current population.
	temp2 = []
	for i in range(len(state.curFitness)):
		temp = (state.curFitness[i],i)       # temporary tuple saves specified fitness and ID of that individual.
		temp2.append(temp)
	#print(temp2)
	#print(sorted(temp2))
	state.curFitness = sorted(temp2) # sort for ranking all individual in current population.

	state.best_hisFitness.append(state.curFitness[0][0]) # save current best fitness and best fitness in the past.
	#print(testyyyy)
	#plt.plot(testxxxx,testyyyy)
	#plt.show()
	
	


	##########################################################################################################################
	########################## Create next generation.
	newpop = []
	numRepro = round(inGP.reprorate*inGP.numpop) # number of replication individual.
	state.numRepro = numRepro
	numCross = round(inGP.crossrate*inGP.numpop) # number of crossover individual.
	numMuta = inGP.numpop - numRepro - numCross # numbe of mutation individual.
	# create list of index that is the best.
	indexlist = []
	for i in range(len(state.curFitness)): # get all of the indexes of all individual.
		indexlist.append(state.curFitness[i][1])

	for i in range(numRepro):
		newpop.append(pop[indexlist[i]])   # replication part.
	# apply the operator.
	for i in range(numCross):
		ind = initpop.Individual()
		ind.tree = op.crossover(pop,state,inGP.proRed,inGP.prosubBlue,inGP.proBlue,inGP.proSubstrate,inGP.proGensub,inGP.proGenpat)
		ind.fitness = []
		ind.ReturnLoss = []
		temp = hp.nodelist()
		ind.nodelist = hp.CreateNodeLists(ind.tree,temp)
		newpop.append(ind)
	# apply the operator.
	for i in range(numMuta):
		ind = initpop.Individual()
		ind.tree = op.mutation(pop,state,inGP.proRed,inGP.prosubBlue,inGP.proBlue,inGP.proSubstrate,inGP.proGensub,inGP.proGenpat)
		ind.fitness = []
		ind.ReturnLoss = []
		temp = hp.nodelist()
		ind.nodelist = hp.CreateNodeLists(ind.tree,temp)
		newpop.append(ind)

	gen = gen + 1
	#print(len(pop))
	#print(len(newpop))
	pop = newpop
	#best_hisGP.append(pop[state.curFitness[0][1]])
	#raise


print(state.best_hisFitness)
f = open(r'C:\Opt_files\best\best_hisFitness.txt','w')
f.write(str(state.best_hisFitness))
f.close()

