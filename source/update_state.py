import datetime 
import os
import numpy as np
import initGlobal as init

def create_Folder():
	# function for create all the ne
	path1 = 'C:/Opt_files'
	path_share = 'C:/HFSS_shared'
	if not os.path.exists(path_share):
		os.makedirs(path_share)
	if not os.path.exists(path1):
		os.makedirs(path1)
	now = datetime.datetime.now()
	now = str(now)

	# check whether run parallelly or not, then if yes the path need be changed.
	if not len(init.PCnames) == 1:
		path1 = '\\\\' + init.PCnames[0] + '\\Opt_files' 
	# print(now)
	out = ''
	signal = 0
	off = 0
	for i in range(len(now)):
		t = now[i]
		# out = out + now[i]
		if (t == '-') or (t == ':') or (t == '.') or (t == ' '):
			if t == ':':
				if signal == 0:
					out = out + 'h'
					signal = 1
				else:
					out = out + 'm'
			elif t == '.':
				off = 1
				out = out + 's'
			else:
				out = out + '_'
		else:
			if off == 0:
				out = out + t
	path2 = path1 + '/GP' + out + '/'
	path3 = path2 + 'temp' + '/'
	if not os.path.exists(path3):
		os.makedirs(path3)
	path4 = path2 + 'temp_tab' + '/'
	if not os.path.exists(path4):
		os.makedirs(path4)
	path5 = path2 + 'lowlevel' + '/'
	path6 = path5 + 'temp' + '/'
	if not os.path.exists(path6):
		os.makedirs(path6)
	path7 = path5  + 'temp_tab' + '/'
	if not os.path.exists(path7):
		os.makedirs(path7)
	return [path1, path2, path3, path4, path5, path6, path7]



def save_specifications(AnT, Sub, L, U, GP, lowlevel, path_for_num, path_for_text):
	# This function saves all nescesaries parameter for running.
	# Notice that: The input vals like AnT, Sub, L, U are class object. 
	num_save = []
	num_save.append(AnT.c) # 1
	num_save.append(AnT.fC) # 2
	num_save.append(AnT.fStart) # 3
	num_save.append(AnT.fStop) # 4
	num_save.append(AnT.npoints) # 5
	num_save.append(AnT.Band_fitness[0]) # 6
	num_save.append(AnT.Band_fitness[1]) # 7
	num_save.append(AnT.Point_start_eval) # 8
	num_save.append(AnT.Point_stop_eval) # 9
	num_save.append(AnT.Center_start_eval) # 10
	num_save.append(AnT.Center_stop_eval) # 11
	num_save.append(Sub.rangeOx[0]) # 12 
	num_save.append(Sub.rangeOx[1]) # 13 
	num_save.append(Sub.rangeOy[0]) # 14
	num_save.append(Sub.rangeOy[1]) # 15
	num_save.append(Sub.rangeOz[0]) # 16
	num_save.append(Sub.rangeOz[1]) # 17
	num_save.append(Sub.addition) # 18
	num_save.append(Sub.decrease) # 19
	num_save.append(L.rangex1[0]) # 20
	num_save.append(L.rangex1[1]) # 21
	num_save.append(L.rangex2[0]) # 22
	num_save.append(L.rangex2[1]) # 23
	num_save.append(L.rangey1[0]) # 24
	num_save.append(L.rangey1[1]) # 25
	num_save.append(L.rangey2[0]) # 26
	num_save.append(L.rangey2[1]) # 27
	num_save.append(U.rangex1[0]) # 28
	num_save.append(U.rangex1[1]) # 29
	num_save.append(U.rangex2[0]) # 30
	num_save.append(U.rangex2[1]) # 31
	num_save.append(U.rangex3[0]) # 32
	num_save.append(U.rangex3[1]) # 33
	num_save.append(U.rangey1[0]) # 34
	num_save.append(U.rangey1[1]) # 35
	num_save.append(U.rangey2[0]) # 36
	num_save.append(U.rangey2[1]) # 37
	num_save.append(U.rangey3[0]) # 38
	num_save.append(U.rangey3[1]) # 39
	num_save.append(GP.maxBlue)   # 40
	num_save.append(GP.numpop)    # 41
	num_save.append(AnT.Point_start_eval_2)  #42
	num_save.append(AnT.Point_stop_eval_2)   #43
	num_save.append(AnT.Center_start_eval_2) #44
	num_save.append(AnT.Center_stop_eval_2)  #45
	np.savetxt(path_for_num, num_save, delimiter = ',')

	file = open(path_for_text,'w')
	file.write(AnT.substrate_material) 
	file.write(',')
	file.write(AnT.resultsDir) # path2
	file.write(',')
	file.write(AnT.tmpDir) # path3
	file.write(',')
	file.write(AnT.tmpTab) # path4
	file.write(',')
	file.write(AnT.Antenna_Name)
	file.write(',')
	file.write(lowlevel.tmpDir) # path 6
	file.write(',')
	file.write(lowlevel.tmpTab) # path 7
	file.write(',')
	file.close()

def update_path(path2, path3, path4, path6, path7, AnT, low):
	# update the path.
	AnT.resultsDir = path2
	AnT.tmpDir = path3
	AnT.tmpTab = path4
	low.tmpDir = path6
	low.tmpTab = path7

def update_path_low(AnT, low):
	path = get_str()
	# update the path for lowlevel optimizer. 
	AnT.resultsDir = path[1]
	AnT.tmpDir = path[2]
	AnT.tmpTab = path[3]
	low.tmpDir = path[5]
	low.tmpTab = path[6]

def get_str():
	import initGlobal as init 
	# get all the essential string parameters like substrate material, paths, antenna name in saved file.
	path = load_temporary_path()
	path = path + init.save_names
	str_txt = ''
	out = []
	temp_out = ''
	with open(path) as temp:
		for i in temp:
			str_txt = str_txt + i
	#print(str_txt)
	for i in range(len(str_txt)):
		if str_txt[i] == ',':
			out.append(temp_out)
			temp_out = ''
		else:
			temp_out = temp_out + str_txt[i]
	return out

def get_parameters_array():

	import initGlobal as init 
	path = load_temporary_path()
	path = path + init.save_paras 
	return np.loadtxt(path,delimiter = ',')


def update_all_saved_parameters(AnT, Sub, L, U, GP, lowlevel):
	# This function saves all nescesaries parameter for running.
	# Notice that: The input vals like AnT, Sub, L, U are class object. 
	array_parameters = get_parameters_array()
	list_name = get_str()


	AnT.c = array_parameters[0] # 1
	AnT.fC = array_parameters[1] # 2
	AnT.fStart = array_parameters[2] # 3
	AnT.fStop = array_parameters[3] # 4
	AnT.npoints = int(array_parameters[4]) # 5
	AnT.Band_fitness[0] = array_parameters[5] # 6
	AnT.Band_fitness[1] = array_parameters[6] # 7
	AnT.Point_start_eval = int(array_parameters[7]) # 8
	AnT.Point_stop_eval = int(array_parameters[8]) # 9
	AnT.Center_start_eval = int(array_parameters[9]) # 10
	AnT.Center_stop_eval = int(array_parameters[10]) # 11
	Sub.rangeOx[0] = array_parameters[11] # 12 
	Sub.rangeOx[1] = array_parameters[12] # 13 
	Sub.rangeOy[0] = array_parameters[13] # 14
	Sub.rangeOy[1] = array_parameters[14] # 15
	Sub.rangeOz[0] = array_parameters[15] # 16
	Sub.rangeOz[1] = array_parameters[16] # 17
	Sub.addition = array_parameters[17] # 18
	Sub.decrease = array_parameters[18] # 19
	L.rangex1[0] = array_parameters[19] # 20
	L.rangex1[1] = array_parameters[20] # 21
	L.rangex2[0] = array_parameters[21] # 22
	L.rangex2[1] = array_parameters[22] # 23
	L.rangey1[0] = array_parameters[23] # 24
	L.rangey1[1] = array_parameters[24] # 25
	L.rangey2[0] = array_parameters[25] # 26
	L.rangey2[1] = array_parameters[26] # 27
	U.rangex1[0] = array_parameters[27] # 28
	U.rangex1[1] = array_parameters[28] # 29
	U.rangex2[0] = array_parameters[29] # 30
	U.rangex2[1] = array_parameters[30] # 31
	U.rangex3[0] = array_parameters[31] # 32
	U.rangex3[1] = array_parameters[32] # 33
	U.rangey1[0] = array_parameters[33] # 34
	U.rangey1[1] = array_parameters[34] # 35
	U.rangey2[0] = array_parameters[35] # 36
	U.rangey2[1] = array_parameters[36] # 37
	U.rangey3[0] = array_parameters[37] # 38
	U.rangey3[1] = array_parameters[38] # 39
	GP.maxBlue   = int(array_parameters[39]) # 40
	GP.numpop    = int(array_parameters[40]) # 41
	AnT.Point_start_eval_2 = int(array_parameters[41])
	AnT.Point_stop_eval_2 = int(array_parameters[42])
	AnT.Center_start_eval_2 = int(array_parameters[43])
	AnT.Center_stop_eval_2 = int(array_parameters[44])  
	#np.savetxt(path_for_num, num_save, delimiter = ',')

	#file = open(path_for_text,'w')
	AnT.substrate_material = list_name[0]
	AnT.resultsDir = list_name[1] # path2
	#file.write(',')
	AnT.tmpDir = list_name[2] # path3
	#file.write(',')
	AnT.tmpTab = list_name[3] # path4
	#file.write(',')
	AnT.Antenna_Name = list_name[4]
	#file.write(',')
	lowlevel.tmpDir = list_name[5] # path 6
	#file.write(',')
	lowlevel.tmpTab = list_name[6] # path 7
	#file.write(',')
	#file.close()

def save_temporary_path(path):
	# remove and save the main path for the current program.
	if os.path.exists('temporary_path.txt'):
		os.remove('temporary_path.txt')
	f = open('temporary_path.txt','w')
	f.write(path)
	f.close()

def load_temporary_path(path = 'temporary_path.txt'):
	# load the main path for current program.
	import initGlobal as init
	if init.Re_trainning:
		str_txt = init.Re_trainning_folder
	else:
		str_txt = ''
		with open(path) as temp:
			for i in temp:
				str_txt = str_txt + i
	return str_txt


'''
a = get_parameters_array('C:/Users/DELL/Desktop/num.txt')
b = get_str('C:/Users/DELL/Desktop/text.txt')



AnT = init.AnT()
Sub = init.Sub()
L   = init.L()
U   = init.U()
low = init.lowlevel()
path = create_Folder()
#print(path)
update_path(path[1],path[2],path[3],path[5],path[6],AnT,low)
update_all_saved_parameters(AnT, Sub, L, U, low,a,b)
save_temporary_path(AnT.resultsDir)'''
