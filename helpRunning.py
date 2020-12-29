# bachthuan03111997@gmail.com - 2018
import initGlobal as init 
import os
import time 
from pathlib import Path 
import numpy as np
import parallel 
inAnT = init.AnT() # get the essential parameters of antenna from initglobal.py 
inGP = init.GP() # get the essential parameters of GP process from initGlobal.py file. note: this's global parameter.
lowinit = init.lowlevel()

import update_state as us 
lowinit = init.lowlevel()
inAnT = init.AnT()
inGP = init.GP() # get the essential parameters of GP process from initGlobal.py file. note: this's global parameter.
if init.Re_trainning:
	inAnT = init.AnT()
	Sub = init.Sub()
	L   = init.L()
	U   = init.U()
	lowinit = init.lowlevel()
	inGP = init.GP()
	#path = us.load_temporary_path()
	us.update_all_saved_parameters(inAnT, Sub, L, U, inGP, lowinit)

def RunPopScript(poplength,dirName,runFrom,numComp,state):
	# state: save all of current variables in GP process.
	# poplength is the length of population
	# dirName is the vbs file name directory.
	# runFrom is the specified ID of indiviudal to start running scripts.
	# numComp is the number of computer gived to run scripts. 
	# note: inAnT is the global parameter that get from initGlobal.py file.
	#		it need be declared before this function.
	print('Start running all of the scripts.')
	poplength = poplength - 1 # need be minused 1 because the saved directory names start from 0. 
	i = runFrom
	parallel_signal = numComp != 1
	if not parallel_signal:
		while(i < poplength):
			#if i > poplength:
			#	break
			# run a specified number of scripts.
			print('Run script ',i)
			theHFSS1 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
			print(theHFSS1)
			i = i + 1
			os.system(theHFSS1) # run specified script
			for other in range(init.numProcess[0]-1):
				# for running enough number of scripts in per run.
				if (i < poplength):
					print('Run script ',i)
					theHFSS2 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
					i = i + 1
					os.system(theHFSS2) # run specified script
			done = False    
			start_time = time.time()
			while not done:
				# check to see wheather all script is done.
				if not state.gen == 1000:
					print('generation: ',state.gen,"/",inGP.numgen)
				else:
					print('run scripts shortting pin '+ str(i) + '/' + str(poplength))

				if state.lowlevel:
					print("RUNNING LOWLEVEL ..... population ", state.population_num,"/",inGP.numpop)
					print("LOWLEVEL FITNESS: ",state.current_low_fitness)
					print("lowlevel_k: ", state.lowlevel_k ,"/",lowinit.number_search_step)
				done = check_Done(0,start_time)
				if (state.gen > 1) and (state.gen != 1000):
					# if not state.lowlevel:
					# 	print('current best fitness: ',state.best_hisFitness[-1])
					# else:
					# 	print('current best fitness: ',state.best_hisFitness_inlow)
					print('current fitness: ',state.curFitness)

	else:
		while i < poplength:

			for i_kill in range(numComp): # all computers need be killed the hfss and related process.
				kill_hfss(i_kill)

			print('Run script ',i) 
			# run the local computer.
			theHFSS1 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
			print(theHFSS1)
			i = i + 1
			os.system(theHFSS1) # run specified script
			for other in range(init.numProcess[0]-1):
				# for running enough number of scripts in per run.
				if (i < poplength):
					print('Run script ',i)
					theHFSS2 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
					i = i + 1
					os.system(theHFSS2) # run specified script
			# done = False    
			# run for other remote computer.
			for xxx in range(len(init.PCnames) -1):
				if i < poplength:
					xx = xxx + 1 # get the correct index of current computer.
					cur_num_of_scripts = init.numProcess[xx]
					if (i + cur_num_of_scripts) >= poplength:  # not enough scripts to run following the expectation
						cur_num_of_scripts = poplength - i + 1 	   # recompute the number of script for current computer.
					parallel.runScripts_on_remote(i, cur_num_of_scripts, dirName, init.PCnames[xx]) # run
					i = i + cur_num_of_scripts  			   # update the index.

			start_time = []
			for no_time in range(numComp):
				start_time.append(time.time())

			all_done = np.zeros(numComp)
			all_done_signal = False
			while not all_done_signal:
				# check to see wheather all script is done.
				print('generation: ',state.gen,"/",inGP.numgen)
				print('script i = ', i)
				if state.lowlevel:
					print("RUNNING LOWLEVEL ..... population ", state.population_num,"/",inGP.numpop)
					print("LOWLEVEL FITNESS: ",state.current_low_fitness)
					print("lowlevel_k: ", state.lowlevel_k ,"/",lowinit.number_search_step)
				for i_check in range(numComp):
					if check_Done(i_check,start_time[i_check]):
						all_done[i_check] = 1
				all_done_signal = sum(all_done) == numComp

				if state.gen > 1:
					# if not state.lowlevel:
					# 	print('current best fitness: ',state.best_hisFitness[-1])
					# else:
					# 	print('current best fitness: ',state.best_hisFitness_inlow)
					print('current fitness: ',state.curFitness)

				if (sum(all_done) >= 1) and (sum(all_done) < numComp):
					list_done = np.where(all_done==1)[0] # save all indexs of computers that have done running the scripts.
					for run_c in range(len(list_done)):
						if (list_done[run_c] == 0) and (i < poplength):
							# continue running on local computer.
							print('Run script ',i) 
							# run the local computer.
							theHFSS1 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
							print(theHFSS1)
							i = i + 1
							os.system(theHFSS1) # run specified script
							for other in range(init.numProcess[0]-1):
								# for running enough number of scripts in per run.
								if (i < poplength):
									print('Run script ',i)
									theHFSS2 = 'start ' + inAnT.hfssExePath + ' /RunScriptAndExit ' + dirName + str(i) + '.vbs'
									i = i + 1
									os.system(theHFSS2) # run specified script
							all_done[0] = 0
							start_time[0] = time.time()
						if (list_done[run_c] != 0) and (i < poplength):
							# continue running for other remote computer.
							if i < poplength:
								xx = list_done[run_c] # get the index of current computer.
								cur_num_of_scripts = init.numProcess[xx]
								if (i + cur_num_of_scripts) >= poplength:  # not enough scripts to run following the expectation
									cur_num_of_scripts = poplength - i + 1     # recompute the number of script for current computer.
								parallel.runScripts_on_remote(i, cur_num_of_scripts, dirName, init.PCnames[xx]) # run
								i = i + cur_num_of_scripts   			   # update the index.
								all_done[list_done[run_c]] = 0
								start_time[list_done[run_c]] = time.time()


			

	print('Done running all scripts.')
###################################################################################################################
def check_Done(i,start_time):
	#-- check to see if hfss is still running on this computer.
	#-- i is specified computer number need be ckecked.
	#-- start_time: is the start point of time to check wheather the scrpit running out of time?.
	# note: inAnT is the global parameter that get from initGlobal.py file.
	#		it need be declared before this function.
	done = False
	# name file to store task list info.
	#file = r'\\' + init.PCnames[0] + r'C:\HFSS_shared'+'/' + init.PCnames[i-1] +'_procs.txt'
	file = '\\\\' + init.PCnames[0] + '\\HFSS_shared'+'\\' + init.PCnames[i] + '_procs.txt'
	# file = \\DESKTOP-K6646BG\HFSS_shared\DESKTOP-K6646BG_procs.txt
	# check for running processes.
	if not i == 0:
		remote_com = init.PCnames[i]
		theSys = r'pslist \\' + init.PCnames[i] +' -u ' + init.users_and_pass[remote_com][0] + ' -p ' \
		+ init.users_and_pass[remote_com][1]  + ' hfss > ' + file
	else: 
		theSys = r'pslist \\' + init.PCnames[i] + ' hfss > ' + file
	os.system(theSys)
	# pslist \\CRD02-PC chrom > C:\HFSS_shared/CRD02-PC_procs.txt
	non_blank_count = 0
	with open(file) as infp:
		for line in infp:
			if line.strip():
				non_blank_count += 1
	if init.PCnames[i] == 'CRD-SERVER':
		done = non_blank_count==4
	else:
		done = non_blank_count==2
	# check for time up
	if (not done):
		if (time.time() - float(start_time) > inAnT.maxTime*60) :
#     if (lineCount(file[i]) > 2) # kill open processes:
			print(r'timer has expired\killing open HFSS files on ' + init.PCnames[i])
			kill_hfss(i)
			done = 1
	return done
#####################################################################################################################3
def assignFitness(nameDir,gen):
	# evaluate the S11.
	# output: - the fitness.
	#		  - S11(fre,S11).
	# nameDir: .tab file source.
	# note: inAnT and inGP are the global parameter that get from initGlobal.py file.
	#		they need be declared before this function.
	file = Path(nameDir)
	if not file.is_file():
		return [100,None,False,False]
	else:
		Fre,S11 = np.genfromtxt(file,dtype = float,skip_header=1, unpack=True)
		Fre_band1 = Fre[inAnT.Point_start_eval:inAnT.Point_stop_eval]
		Fre_band2 = Fre[inAnT.Point_start_eval_2:inAnT.Point_stop_eval_2]
		Band = S11[inAnT.Point_start_eval:inAnT.Point_stop_eval]
		Band_2 = S11[inAnT.Point_start_eval_2:inAnT.Point_stop_eval_2]   ########### new 
		#count = 0
		fitness = 0
		signal_start_i = False # the signal reveals whether the loop encourter first point < -10 or not. 
		signal_stop_i  = False
		for i in range(len(Band)):
			#if Band[i] < -10:
				#count = count + 1 # count the number of points that have S11 < -10
			if Band[i] < -10:
				fitness = fitness + Band[i] - 10*(Band[i]/-10)**2 # penalty the point s11 << -10
			else:
				fitness = fitness + Band[i]

			if Band[i] <= -10 and (not signal_start_i):
				start_i = i
				signal_start_i = True

			if signal_start_i and (not signal_stop_i):
				if (i > start_i):
					if Band[i] >= -10:
						signal_stop_i = True
						stop_i = i
					if (i == (len(Band) -1)) and (Band[i] <= -10):
						signal_stop_i = True
						stop_i = i
		if signal_stop_i and signal_start_i:
			bandwidth_1 = Fre_band1[stop_i] - Fre_band1[start_i]     # fitness for bandwidth 1.
			fitness = fitness - 6000*bandwidth_1					 # bandwidth 
			print(6000*bandwidth_1)

		signal_start_i = False # the signal reveals whether the loop encourter first point < -10 or not. 
		signal_stop_i  = False
		for i in range(len(Band_2)):									###### new
			if Band_2[i] < -10:
				fitness = fitness + Band_2[i] - 10*(Band_2[i]/-10)**2
			else:
				fitness = fitness + Band_2[i]

			if Band_2[i] <= -10 and (not signal_start_i):
				start_i = i
				signal_start_i = True

			if signal_start_i and (not signal_stop_i):
				if (i > start_i):
					if Band_2[i] >= -10:
						signal_stop_i = True
						stop_i = i
					if (i == (len(Band_2) -1)) and (Band_2[i] <= -10):
						signal_stop_i = True
						stop_i = i
		if signal_stop_i and signal_start_i:
			bandwidth_2 = Fre_band2[stop_i] - Fre_band2[start_i]     # fitness for bandwidth 2.
			fitness = fitness - 6000*bandwidth_2
			print(6000*bandwidth_2)


		min_S11_1 = min(Band)                                           # changed
		min_S11_2 = min(Band_2) # new 
		so_best_1 = S11[inAnT.Center_start_eval:inAnT.Center_stop_eval]
		so_best_2 = S11[inAnT.Center_start_eval_2:inAnT.Center_stop_eval_2]
		exist1 = False
		exist2 = False
		exist_band2 = False
		if ((min_S11_1 in so_best_1) and (min_S11_1 < -10)) or ((min_S11_2 in so_best_2) and (min_S11_2 < -10)):
			print('exist a best fitness')
			exist1 = True
			fitness = fitness - 100
			if fitness < inGP.overcome_fitness:
				exist2 = True
		if ((min_S11_1 in so_best_1) and (min_S11_1 < -10)) and ((min_S11_2 in so_best_2) and (min_S11_2 < -10)):
			fitness = fitness - 100
			exist_band2 = True
		if exist1 and exist_band2:
			fitness = fitness - 200


		if (min(Band) > -10) and (min(Band_2) > -10) and (min(S11) < -10):
			fitness = sum(S11)

	return [fitness,[Fre,S11],exist1,exist2]

def kill_hfss(i):
	# kill any open processes related to HFSS on specified computer
	# i is the specified index of computer.
	filename = ['hfss', 'G3dMesher', 'hf3d', 'HFSSCOMENGINE']
	remote_com = init.PCnames[i]

	for ii in range(len(filename)):
		if not i ==0:
			os.system('pskill \\\\' + init.PCnames[i] + ' -u ' + init.users_and_pass[remote_com][0] + ' -p ' + init.users_and_pass[remote_com][1]\
			+ ' ' + filename[ii])
		else:
			os.system('pskill \\\\' + init.PCnames[i] + ' ' + filename[ii])