# coding=utf-8 
import py_compile
import os, sys

def ispy(file):
	return 'py' in file.split('.')[-1]

def ispyc(file):
	return 'pyc' in file.split('.')[-1]	
	
def compile(rootpath):
	for root, dirs, files in os.walk(rootpath):
		for file in files:
			if ispy(file):
				filename = os.path.join(root, file)
				py_compile.compile(filename)
				
def removeSrc(rootpath):
	for root, dirs, files in os.walk(rootpath):
		for file in files:
			if ispy(file) and not ispyc(file):
				filename = os.path.join(root, file)
				os.remove(filename)
				
def main():
	ROOT_PATH = os.path.abspath(sys.path[0])
	compile(ROOT_PATH)
	removeSrc(ROOT_PATH)

if __name__ == "__main__":
	main()
