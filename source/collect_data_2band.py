# thuan.bb.hust@gmail.com
import os
import Helper as hp
import FindSp as fs
import initGlobal as init
from genscript import genscript_short_pin, Find_feed_point
import helpRunning as hrun
import numpy as np 

def SP_data_collection(dirFolder, list_short):
	# first the folder for saving the data need be created.
	dir_data = dirFolder + 'data/'
	dir_data_run = dir_data + 'run/'
	dir_data_out = dir_data + 'out/'

	if not os.path.exists(dir_data):
		os.makedirs(dir_data)
	if not os.path.exists(dir_data_run):
		os.makedirs(dir_data_run)
	if not os.path.exists(dir_data_out):
		os.makedirs(dir_data_out)
	# done make folder.
	list_short_point = list_short
	print(len(list_short_point))


	global_name = dir_data_run + 'shortting_pin'
	global_name_tab = dir_data_out + 'shortting_pin'



	# create the vbs files.
	for i in range(len(list_short_point)):
		true = open(dirFolder + 'true.vbs').read()
		true = true.replace('"XCenter:=", "15.748590mm", _', '"XCenter:=", "' + str(list_short_point[i][0]) + 'mm", _')
		true = true.replace('"YCenter:=", "12.435995mm", _', '"YCenter:=", "' + str(list_short_point[i][1]) + 'mm", _')
		true = true.replace('"C:/Opt_files/GP2019_03_28_11h18m27s/lowlevel/temp_tab/MPA_gen_14_pop_2_step_k1_d_0.tab"', '"' + global_name_tab + str(i) + '.tab' +'"')
		f = open(global_name + str(i) + '.vbs', 'w')
		f.write(true)
		f.close()


	class state:
		pass 
	state.lowlevel = False
	state.gen = 1000
	hrun.RunPopScript(len(list_short_point), global_name, 0, len(init.PCnames),state)
	#list_fitness = []

	save_fitness = np.zeros(len(list_short_point))

	for i in range(len(list_short_point)):
		[fitness,_,_,_] = hrun.assignFitness(global_name_tab,i)
		#list_fitness.append(fitness)
		save_fitness[i] = fitness

	np.savetxt(dir_data_out+'fitness.txt', save_fitness, delimiter=',')



dirFolder = 'C:/Users/HupeCRD/Dropbox/LabWork/paper2/'
list_point = np.loadtxt(dirFolder + 'list_point.txt',delimiter = ',')
SP_data_collection(dirFolder, list_point)


