from multiprocessing import Process, Queue
import os,signal
import commands, subprocess
import time

def getFileDetails(filename):
	filename = filename.rsplit('.',1)
	exe = filename[1]
	filename = filename[0].rsplit('/',1)
	file = filename[1]
	path = filename[0]
	return path, file, exe

def openAndPrint(fileName):
	f=open(fileName)
	Str=""
	for row in f:
		Str=Str+row.strip()
	return Str

def getCompilationStatus(compilation_args):
    compilation_result = {}
    start = time.time()
    popen = subprocess.Popen(compilation_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print popen
    stop = time.time()
    compilation_result['stdout'] = popen.stdout.read()
    compilation_result['stderr'] = popen.stderr.read()
    compilation_result['exe_time'] = stop - start
    return compilation_result

def getOutputStatus(execution_args, q):
    execution_result = {}
    start = time.time()
    popen = subprocess.Popen(execution_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stop = time.time()
    execution_result['stdout'] = popen.stdout.read()
    execution_result['stderr'] = popen.stderr.read()
    execution_result['exe_time'] = stop - start
    q.put(execution_result)

def timer(timeout):
	time.sleep(timeout)

def compile(path, fname, exe, lan, timeout):
	compilation_status = {'stdout':"",'stderr':"",'exe_time':""}
	execution_status = {}
	final_status = {}

	execution_command = ""
	if exe=="c":
		args = ("gcc -o "+path+"/"+fname+" "+path+"/"+fname+"."+exe)
		compilation_status = getCompilationStatus(args)
		execution_command = (path+"/"+fname+" < "+path+"/"+fname+"_input.txt")
	elif exe=="java":
		args = ("javac "+path+"/"+fname+"."+exe)
		compilation_status = getCompilationStatus(args)
		execution_command = ("java -cp "+path+" "+fname)
	elif exe=="cpp":
		args = ("g++ -o "+path+"/"+fname+" "+path+"/"+fname+"."+exe)
		compilation_status = getCompilationStatus(args)
		execution_command = (path+"/"+fname+" < "+path+"/"+fname+"_input.txt")
	elif exe=="py" and lan=="py":
		execution_command = ("python "+path+"/"+fname+"."+exe+" < "+path+"/"+fname+"_input.txt")
	elif exe=="py" and lan=="py3":
		execution_command = ("python3 "+path+"/"+fname+"."+exe+" < "+path+"/"+fname+"_input.txt")
	else:
		final_status['valid_selection']="False"
		return final_status

	final_status['valid_selection']="True"
	if compilation_status['stderr']=="":
		final_status['compilation_status']="True"
		final_status['compilation_error']=""
		q = Queue()
		checkoutput = ""
		p1 = Process(target=getOutputStatus, args=(execution_command,q,))
		p2 = Process(target=timer, args=(timeout,))
		p1.start()
		p2.start()

		while p1.is_alive() and p2.is_alive():
			continue

		if p1.is_alive():
			final_status['execution_status'] = "False"
			final_status['execution_error'] = "Terminated due to timeout"
			final_status['execution_output'] = ""
			os.kill(p1.pid,signal.SIGKILL)
		else:
			checkoutput = q.get()
			os.kill(p2.pid,signal.SIGKILL)

			if checkoutput['stderr']=="":
				final_status['execution_status'] = "True"
				final_status['execution_error'] = ""
				final_status['execution_output'] = checkoutput['stdout']
				final_status['execution_time'] = checkoutput['exe_time']
			else:
				final_status['execution_status'] = "False"
				final_status['execution_error'] = checkoutput['stderr']
	else:
		final_status['compilation_status']="False"
		final_status['compilation_error']=compilation_status['stderr']
	return final_status

def getCompile(filename, lan, timeout):
	path,file,exe = getFileDetails(filename)
	return compile(path, file, exe, lan, timeout)

if __name__=="__main__":
	filename="../compile/123/java/example.java"
	print getCompile(filename, 'java', 10)
