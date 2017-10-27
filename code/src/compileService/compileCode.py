from multiprocessing import Process, Queue
import os,signal
import commands
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

def getCompilationStatus(command_str):
	return commands.getoutput(command_str)

def getOutputStatus(command_str, q):
	q.put(commands.getoutput(command_str))

def timer(timeout):
	time.sleep(timeout)

def compile(path, fname, exe, lan, timeout):
	compilation_status = ""
	execution_command = ""

	if exe=="c":
		compilation_status = getCompilationStatus("gcc -o "+path+"/"+fname+" "+path+"/"+fname+"."+exe)
		execution_command += path+"/"+fname+" < "+path+"/"+fname+"_input.txt"
	elif exe=="java":
		compilation_status = getCompilationStatus("javac "+path+"/"+fname+"."+exe)
		execution_command += "java -cp "+path+" "+fname
	elif exe=="cpp":
		compilation_status = getCompilationStatus("g++ -o "+path+"/"+fname+" "+path+"/"+fname+"."+exe)
		execution_command += path+"/"+fname+" < "+path+"/"+fname+"_input.txt"
	elif exe=="py" and lan=="py":
		execution_command += "python "+path+"/"+fname+"."+exe+" < "+path+"/"+fname+"_input.txt"
	elif exe=="py" and lan=="py3":
		execution_command += "python3 "+path+"/"+fname+"."+exe+" < "+path+"/"+fname+"_input.txt"
	else:
		return "Please select language from specified one only"

	if compilation_status=="":
		q = Queue()
		checkoutput = ""
		p1 = Process(target=getOutputStatus, args=(execution_command,q,))
		p2 = Process(target=timer, args=(timeout,))
		p1.start()
		p2.start()

		while p1.is_alive() and p2.is_alive():
			continue

		if p1.is_alive():
			checkoutput = "Terminated due to timeout"
			os.kill(p1.pid,signal.SIGKILL)
			#p1.terminate()
			#p2.terminate()
		else:
			checkoutput = q.get()
			os.kill(p2.pid,signal.SIGKILL)
		return checkoutput
	else:
		return compilation_status

def getCompile(filename, lan, timeout):
	path,file,exe = getFileDetails(filename)
	return compile(path, file, exe, lan, timeout)

if __name__=="__main__":
	filename="../compile/123/java/example.java"
	print getCompile(filename, 'java', 10)
