# thuan.bb.hust@gmail.com - 2019

import os 
import initGlobal as init
ant = init.AnT()

def run_remote(remote_com):
	# for runing the batch file on remote computer.
	
	print('running the batch file on ' + remote_com +' computer')
	dirname = '\\\\' + remote_com + '\\' + 'HFSS_shared' + '\\' + remote_com + 'batch_file' + '.bat'

	theSys = 'psexec ' + '\\\\' + remote_com + ' -u ' + init.users_and_pass[remote_com][0] + ' -p ' + init.users_and_pass[remote_com][1] \
	+ ' -i -d ' + dirname
	print(theSys)
	os.system(theSys)



def write_batch_file(i, num, remote_com, dirname):
	# function writes a batch file for running vbs file on specified remote computer.
	# where: i - is the start ID of vbs file.
	#		 num - is the number of vbs file that will be executed parallelly.
	#		 remote_com is the specified name of remote computer. 
	#		 local_com is the name of local cumputer.
	print('wrtting batch file for ' + remote_com + ' computer')
	name = '\\\\' + init.PCnames[0] + '/HFSS_shared/' + remote_com + 'batch_file' + '.bat'
	f = open(name,'w')
	for ii in range(num):
		iii = ii + i # start at specified point.
		theSys = 'start ' + ant.hfssExePath + ' /RunScriptAndExit ' + dirname + str(iii) +'.vbs'
		f.write(theSys + '\n')
	f.close()

def copy_to_remote(remote_com):
	# copy batch file to remote computer. 
	print('copy batch file to ' + remote_com + ' computer')
	remote_folder = '\\\\' + remote_com + '\\' + 'HFSS_shared'

	theSys = 'copy ' + '\\\\' + init.PCnames[0] + '\\' + 'HFSS_shared' + '\\' + remote_com + 'batch_file' + '.bat ' + remote_folder

	os.system(theSys)

def runScripts_on_remote(start, num, dirname, remote_com):
	# firstly, batch file need be created.
	write_batch_file(start, num, remote_com, dirname)
	# copy batch file to remote computer.
	copy_to_remote(remote_com)
	# then execute it.
	run_remote(remote_com)