import subprocess
import paramiko
import os
import re
import tempfile
import datetime
from configparser import ConfigParser
import winreg
from time import sleep

def main():
	winTmpDisp = "sshcom.txt"
	#check if temporary settings directory exists makes if not
	tmpPaths = setup()
	params = getnCheckCfg(tmpPaths['ini_loc'])
	#find out the session display
	remot_tmp = setuptmp(params['linuxtmpdir'])
	data = [tmpPaths['tmp_dir'], remot_tmp['lnxP']]
	#get display number
	cmd = f"echo $DISPLAY > {remot_tmp['lnxP']}"
	lnxCmdWrDisp(os.path.join(tmpPaths['tmp_dir'],winTmpDisp), cmd, params['username'], params['ip'] )
	#find display for VNC
	sleep(1)
	remot_tmp = setuptmp(params['linuxtmpdir'])
	cmd = f"ls /etc/systemd/system | grep vncserver > {remot_tmp['lnxP']}"
	lnxCmdWrDisp(os.path.join(tmpPaths['tmp_dir'],winTmpDisp), cmd, params['username'], params['ip'] )
	#read it back to windows
	path_to_disp = retreive(params['ip'], params['sshport'], params['username'], data, 'dispAnswer.txt')
	display = readDisplay(path_to_disp)
	
	data = [tmpPaths['tmp_dir'], remot_tmp['lnxP']]
	path_to_port = retreive(params['ip'], params['sshport'], params['username'], data, 'VNCAnswers.txt')
	vnc_disp = getVNCNo(params['username'], path_to_port)
	if params['debug'] == 'False':
		cleanup(tmpPaths['tmp_dir'],tmpPaths['ini_loc'])
	fmDisp = splitDisp(display)
	
	configureEnv(fmDisp,vnc_disp,params['puttysession'])
	launchputty(params['puttysession'])
	cleanupXming()
	sleep(3)

def cleanup(tmpDIR, ignore):
	print("cleaning up files")
	tmpFiles = os.listdir(tmpDIR)
	print("tmpFiles: ", tmpFiles)
	print("ignore: ", ignore)
	for file in tmpFiles:
		print("file: ",file)
		full = os.path.join(tmpDIR,file)
		if file in ignore:
			print('ignoring: ', file)
		else:
			print("delete: ", full)
			try:
				os.remove(full)
			except OSError:
				print("was not able to delete", full)

def getVNCNo(name, path):
	print("user defined name", name)
	with open(path, "r") as f:
		Lines = f.readlines()
		print("Lines: ",Lines)
		for line in Lines:
			print("VNCfile:",line)
			fname = re.search("(?<=-)(.*?)(?=@)", line).group()
			print("fname: ", fname)
			if fname == name:
				return re.search("(?<=:)(.*?)(?=\.)", line).group().replace("\n", "")
			
		print("No match for user name")
		print(f"Warning: was not able to find a display for {name}")
		return 0

def setup():
	print("########################################\n")
	print("Please ensure pageant has your key running before continuing!")
	print("press enter to continue")
	print("########################################\n")
	tmp=input('>>')
	tmpDN = 'EDA_Script'
	iniN = 'launchPutty.ini'
	#get temp dir
	tmpD = tempfile.gettempdir()
	#check my folder and ini exists
	fulltmpD = os.path.join(tmpD,tmpDN)
	fulltmpini = os.path.join(fulltmpD,iniN)
	#create ini if not exist
	try:	
		if os.path.isdir(fulltmpD):
			createINI(fulltmpini)
		else:
			os.mkdir(fulltmpD)
			createINI(fulltmpini)
	except OSError:
		print("Could not write ini file:", fulltmpini)
		input("press enter to exit program")
		exit()
	#returns temporary paths
	return {'ini_loc':fulltmpini,'tmp_dir':fulltmpD}


def usrInp():
    print("########################################\n")
    username = input(">>Input ssh username: ")
    print("########################################\n")
    return {'username': username}


def launchputty(profile):
	ret = subprocess.call(['putty.exe', '-load', 'linux_con'])

def changeHKEYcurrentUser(loc, data):
	try:	
		with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as hkey:
			with winreg.OpenKey(hkey, loc,0,winreg.KEY_ALL_ACCESS) as sub_key:
				winreg.SetValueEx(sub_key,data[0],0,winreg.REG_SZ,data[1])
	except Exception as error:
		print('ERROR: Caught error: ' + repr(error))
		print('ERROR-msg: Please correct the ini file to reflect your ssh profile name')
		tmp = input("Press Enter to escape program")
		exit()

def configureEnv(dispInfo, vncdisp, session):
	#xming launching
	disp = f":{dispInfo['dispNo']}"
	ret = subprocess.Popen(['xming.exe', disp, '-multiwindow'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
	#adjusting ESI
	disp = '{\"0|DISPLAY\":\"%s\"}'% dispInfo['display'] 
	data = ['EnvVars', disp]
	print("new regestry value: ",data)
	changeHKEYcurrentUser('SOFTWARE\Tanner EDA\esi64\ESI settings',data)
	#adjusting putty
	data = ['X11Display', dispInfo['display']]
	print("new regestry value: ",data)
	keypath = f'SOFTWARE\SimonTatham\PuTTY\Sessions\{session}'
	changeHKEYcurrentUser(keypath,data)
	#adjustVNC settings
	portNo = constructNo(vncdisp)

	if  portNo != 0:
		portdata = f"L{portNo}=localhost:{portNo}"
		data = ['PortForwardings', portdata]
		print("new regestry value: ",data)
		keypath = f'SOFTWARE\SimonTatham\PuTTY\Sessions\{session}'
		changeHKEYcurrentUser(keypath,data)
	
	

def constructNo(disp):
	dispNo = int(disp)
	no = 5900
	if dispNo != 0 and dispNo < 10:
		no = no + dispNo
		return no
	else:
		return 0


def splitDisp(display):
	try:
		dispNo = re.search("(?<=:)[\w+.-]+", display)
		dispNo = dispNo.group()
		dispNo = re.search(".*(?=\.)",dispNo)
		ip = re.search(".+?(?=:)", display)	
	except Exception as error:
		print('Caught error: ' + repr(error))
		print(f'error in display variable being returned by remote machine: {display}')
		tmp = input("Press Enter to escape program")
		exit()
	print(f'display: {display}')
	return {'ip':ip.group(),'dispNo':dispNo.group(), 'display':display}

def cleanupXming():
	tmp = os.system("taskkill /im XLaunch.exe /f")
	tmp = os.system("taskkill /im Xming.exe /f")

def createINI(file):
	if os.path.isfile(file):
		return 0
	else:
		input = usrInp()
		config = ConfigParser()
		config['remote_settings'] = {
			'ip': "10.8.12.20",
			'sshport': '22',
			'displayIPnNo': "localhost:",
			'linuxtmpDIR': "/tmp",
			'puttysession': 'linux_con',
			'username': input['username']
		}
		config['debug'] = {
			'debug': 'False'
		}
		
		with open(file, 'w') as f:
			config.write(f)

def getnCheckCfg(file):
	pars = ConfigParser()
	try:
		pars.read(file)
	except OSError:
		print("Could not write ini file:", file)
		input("press enter to exit program")
		exit()
	cfgVar = {}
	if 'remote_settings' in pars and 'debug' in pars:
		for sec in pars.sections():
			for key in pars.items(sec):
				cfgVar[key[0]] = key[1]
	return cfgVar

def lnxCmdWrDisp(filepath, cmd, user, ip):
	try:
		f = open(filepath, "w")
		f.write(cmd)
		f.close()
	except OSError:
		print("Could not write file:", filepath)
		input("press enter to exit program")
		exit()
	srv = subprocess.call(['putty.exe', '-X', user + '@' + ip, '-m', filepath])

def setuptmp(tmpdir):
	now = datetime.datetime.now()
	timeStr = now.strftime("%d_%m_%Y_%H_%M_%S")
	linuxtmpDIR = f"{tmpdir}/EDA_dispqueery_{timeStr}.txt"
	lnxdir = {'lnxP':linuxtmpDIR}
	return lnxdir

def connect(ip, port, user):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, port=port,  username=user, allow_agent=True)
	return ssh

def retreive(ip, port, user, path, name):
	full_path = os.path.join(path[0], name)
	client = connect(ip, port, user)
	ftp_client=client.open_sftp()
	ftp_client.get(path[1],full_path)
	ftp_client.close()
	client.close()
	return full_path

def readDisplay(fname):
	try:
		f = open(fname, 'r')
		data = f.readlines()
		f.close()
		if len(data) == 1:
			if re.search("^localhost:", data[0]):
				cleanupD=data[0].replace("\n", "")
				return cleanupD
			else:
				raise Exception(f'unexpected value: {data[0]}')
		else:
			raise Exception('file contains unexpected contents')
	except OSError:
		print("Could not open/read file:", fname)
		tmp = input("Press Enter to escape program")
		exit()
	except Exception as error:
		print('Caught error: ' + repr(error))
		tmp = input("Press Enter to escape program")
		exit()
if __name__ == "__main__":
	main()



