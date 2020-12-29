import os
import Helper as hp
import FindSp as fs
import initGlobal as init
from genscript import genscript_short_pin, Find_feed_point
import helpRunning as hrun
import numpy as np 

def SP_data_collection(dirFolder, tree):
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

	# save the string tree.
	f = open(dir_data_out + 'tree.txt','w')
	f.write(hp.tree2str(tree))
	f.close()

	list_short_point = fs.create_list_point(tree)
	print(len(list_short_point))

	[Substrate,polygons,centroid,poly_list, poly_list_type] = hp.get_all_para_for_hfss(tree) # get necessary parameters for genscript function.

	feed_point = Find_feed_point(Substrate, polygons, centroid, poly_list, poly_list_type)


	list_short_point = fs.update_list([feed_point], list_short_point) # update list_shortting pin points, delete the 
	print(len(list_short_point))

	save_list_point = np.zeros((len(list_short_point),2))

	# f = open(dir_data_out + 'list_point.txt','w')
	# f.write(str(list_short_point))
	# f.close()

	global_name = dir_data_run + 'shortting_pin'
	global_name_tab = dir_data_out + 'shortting_pin'

	for i in range(len(list_short_point)):
		save_list_point[i][0] = list_short_point[i][0]
		save_list_point[i][1] = list_short_point[i][1]
		name = global_name + str(i) # name of directory would
		nametab = global_name_tab + str(i)
																	# be used to save .vbs and .hfss file.
		genscript_short_pin(Substrate,polygons,centroid,name + '.vbs', nametab, name + '.hfss', poly_list, poly_list_type, list_short_point[i])

	np.savetxt(dir_data_out + 'list_point.txt', save_list_point, delimiter=',')

	class state:
		pass 
	state.lowlevel = False
	state.gen = 1000
	hrun.RunPopScript(len(list_short_point), global_name, 0, len(init.PCnames),state)
	#list_fitness = []

	save_fitness = np.zeros(len(list_short_point))

	for i in range(len(list_short_point)):
		[fitness,_,_,_] = hpr.assignFitness(global_name_tab,i)
		#list_fitness.append(fitness)
		save_list_point[i] = fitness

	np.savetxt(dir_data_out+'fitness.txt', save_fitness, delimiter=',')




# testttttttttttttttttttttttttttttttt
import str2tree as s2t
tree_str = s2t.load_str_tree('C:/Users/HupeCRD/Desktop/24-35Ghzz/GP2019_03_28_11h18m27s/temp/MPA_gen_1_pop_2.txt')
tree = s2t.str2tree(tree_str,0,1,0,None)
#hp.drawtree(tree)
tree = s2t.update_tree(tree)
#tree.childs[1].valueofnode.plot()

SP_data_collection("C:\\Users\\HupeCRD\\Desktop\\",tree)

