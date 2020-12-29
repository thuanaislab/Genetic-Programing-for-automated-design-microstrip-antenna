# bachthuan03111997@gmail.com - 2018

import initGlobal as init

import matplotlib.pyplot as plt 
# from testFunctionFitness import fitness
import os
import time
import shutil

# import ANN_lowOptimize as anlow 
import update_state as us 

import str2tree 
######################################################### MAIN ######################################################

lowlevel = init.lowlevel()
first_time = time.time()
inAnT = init.AnT() # get the essential parameters of antenna from initglobal.py
inGP = init.GP() # get the essential parameters of GP process from initGlobal.py file. note: this's global parameter.
L = init.L()
U = init.U()
Sub = init.Sub()
if not init.Re_trainning:
	path = us.create_Folder() # create folder for program.
	us.update_path(path[1], path[2], path[3], path[5], path[6], inAnT, lowlevel)
	us.save_specifications(inAnT, Sub, L, U, inGP, lowlevel, inAnT.resultsDir + init.save_paras, inAnT.resultsDir + init.save_names)
	us.save_temporary_path(inAnT.resultsDir)
else:
	us.update_all_saved_parameters(inAnT, Sub, L, U, inGP, lowlevel)

mydir = inAnT.tmpTab
mydir_hfss = inAnT.tmpDir



import helpRunning as hpr
import InitPopMethods as initpop
import Helper as hp
from genscript import genscript
import GPoperators as op 
import DS_lowOptimize as dslow



class state: # define a state object to save some necessary results.
    pass 
#import os
state.lowlevel = False
state.best_hisFitness = []
state.curFitness = [] # to save all current fitness.
state.name_best_his = []


if not init.Re_trainning:
	#state.best_hisFitness = []
	gen = 1 # current generation.

	pop = initpop.rampinit(inGP.numpop,inGP.maxSub, inGP.maxPat, inGP.maxBlue,inGP.rate) #-- init population by rampinit method.
else:
	state.best_hisFitness.append(0)
	gen = init.start_gen_for_retraining
	pop = []
	ind_path = inAnT.tmpDir + inAnT.Antenna_Name + '_gen_' + str(init.start_gen_for_retraining) + '_pop_'
	for re in range(int(inGP.numpop)):
		temp_str = str2tree.load_str_tree(ind_path + str(re) + '.txt')
		temp_tree = str2tree.str2tree(temp_str,0,1,0,None)
		temp_tree = str2tree.update_tree(temp_tree)
		pop.append(initpop.restruct_ind(temp_tree, re + 1))
	signal_first_gen = True 


# print(len(pop))
# time.sleep(10000)



global_name = inAnT.tmpDir + inAnT.Antenna_Name + '_gen_'
global_tabname = inAnT.tmpTab + inAnT.Antenna_Name + '_gen_'
global_out_text_name = inAnT.resultsDir + inAnT.Antenna_Name  + '_gen_'

for iii in range(inGP.numgen):
	state.gen = gen 
	print('generating ',len(pop), ' scripts at generation ',gen)

		# if iii == 0: # this case is the initial part.
	for i in range(len(pop)):
		temp = pop[i].tree
		[Substrate,polygons,centroid,poly_list, poly_list_type] = hp.get_all_para_for_hfss(temp) # get necessary parameters for genscript function.
		name = global_name + str(gen) + '_pop_' + str(i) # name of directory would
																	# be used to save .vbs and .hfss file.
		tabname = global_tabname + str(gen) + '_pop_' + str(i) # name of directory
																	# would be used to save .tab file. 
		genscript(Substrate,polygons,centroid,name + '.vbs',tabname,name + '.hfss',poly_list,poly_list_type)
		f = open(name + '.txt','w')
		f.write(hp.tree2str(pop[i].tree))
		f.close()
		print('genscript is done.')
		#time.sleep(10000)

	## Run all scripts to get .tab file.
	nameDir = inAnT.tmpDir + inAnT.Antenna_Name + '_gen_' + str(gen) + '_pop_'  # file name direction of the vbs file.
	if gen == 1 or signal_first_gen:
		# This case is initial part.
		hpr.RunPopScript(len(pop),nameDir,0,len(init.PCnames),state)
	else:
		# other.
		hpr.RunPopScript(len(pop),nameDir,numRepro,len(init.PCnames),state)

	### evaluate and assign the fitness of each model.
	############################################################################################3
	nameDir_tab = inAnT.tmpTab + inAnT.Antenna_Name + '_gen_' + str(gen) + '_pop_' # file name directory to tab file.
	if gen == 1 or signal_first_gen:
		signal_first_gen = False
		for i in range(len(pop)):
			spec_nameDir_tab = nameDir_tab + str(i) + '.tab'
			[pop[i].fitness, pop[i].ReturnLoss,p,q] = hpr.assignFitness(spec_nameDir_tab,gen) # update the fitness of each individual.
			if pop[i].fitness < inGP.desired_fitness:
				shutil.copy2(global_name + str(gen) + '_pop_' + str(i) + '.vbs', inAnT.resultsDir)
				shutil.copy2(global_name + str(gen) + '_pop_' + str(i) + '.txt', inAnT.resultsDir)
				shutil.copy2(spec_nameDir_tab, inAnT.resultsDir)
				#hp.drawtree(pop[i].tree,inAnT.resultsDir + '_gen_' + str(gen) + '_pop_' + str(i))
				f = open(global_out_text_name + str(gen) + '_pop_' + str(i) + '.txt','w')
				#f.write(hp.tree2str(pop[i].tree))
				#f.write('#')
				f.write('fitness: ' + str(pop[i].fitness))
				f.write('#')
				f.write('time: ' + str((time.time() - first_time)/60))
				f.write('#')
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
				shutil.copy2(global_name + str(gen) + '_pop_' + str(i) + '.txt', inAnT.resultsDir)
				shutil.copy2(global_name + str(gen) + '_pop_' + str(i) + '.vbs', inAnT.resultsDir)
				shutil.copy2(spec_nameDir_tab, inAnT.resultsDir)
				#hp.drawtree(pop[i].tree,inAnT.resultsDir + '_gen_' + str(gen) + '_pop_' + str(i))
				f = open(global_out_text_name + str(gen) + '_pop_' + str(i) + '.txt','w')
				#f.write(hp.tree2str(pop[i].tree))
				#f.write('#')
				f.write('fitness: ' + str(pop[i].fitness))
				f.write('#')
				f.write('time: ' + str((time.time() - first_time)/60))
				f.write('#')
				if p:
					f.write("_____exist best fitness")
					if q:
						f.write("___ that is better than overcome_desired")
				f.close()
	#testxxxx = []
	#testyyyy = []
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
	##############################################################################
	#########################################################################################################################
	########################################################## LOWLEVEL OPTIMIZER ###########################################
	if lowlevel.lowoptimize:
		print("RUNNING LOWLEVEL OPTIMIZER ......")
		for i in range(len(pop)):
			state.population_num = i 
			pop[i] = dslow.lowlevel_optimizer(pop[i],state,i)


	state.lowlevel = False
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
	name_best = inAnT.Antenna_Name + '_gen_' + str(gen) + '_pop_' + str(state.curFitness[0][1])
	state.name_best_his.append(name_best)
	#print(testyyyy)
	#plt.plot(testxxxx,testyyyy)
	#plt.show()
	if iii == (inGP.numgen-1):
		indexlist = []
		for i in range(len(state.curFitness)): # get all of the indexes of all individual.
			indexlist.append(state.curFitness[i][1])
		from collect_data_shorttingpin import SP_data_collection
		SP_data_collection(inAnT.resultsDir, pop[indexlist[0]].tree) 
		
	


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
	f = open(inAnT.resultsDir + '/best_hisFitness.txt','w')
	f.write(str(state.best_hisFitness))
	f.close()


print(state.best_hisFitness)
f = open(inAnT.resultsDir + '/best_hisFitness.txt','w')
f.write(str(state.best_hisFitness))
f.close()
f = open(inAnT.resultsDir + 'name_best_his.txt','w')
f.write(str(state.name_best_his))
f.close()


