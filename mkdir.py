# -*- coding: utf-8 -*-
import os, sys
import shutil


def mkDirs(dirName):
	subDirs = ['_html', 'css', 'js', 'res-inc', 'tpl']
	for d in subDirs:
		os.makedirs('./' + dirName + os.sep + d)

	copyShell(dirName)	

def copyShell(dirName):
	shellDir = os.path.split(os.path.realpath(__file__))[0]
	shutil.copy(shellDir + os.sep + 'build.sh', dirName)

if __name__ == '__main__':
	dirName = raw_input('请输入要生产的目录：')
	listDir = os.listdir(os.getcwd())
	if dirName in listDir:
		print '你要创建的目录' + dirName + '已经存在，请认真检查'
		exit(0)

	mkDirs(dirName);


