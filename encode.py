# -*- coding: utf-8 -*-
import sys, os, shutil, traceback, time
from chardet.universaldetector import UniversalDetector

encodes = {
	"gb2312" : "gb18030",
	"gbk": "gb18030",
	"utf-8": "utf-8"
}

class HeEncodingEx(Exception):
	def __init__(self, msg):
		Exception.__init__(self, msg)

def printRed(s):
    return"%s[31;2m%s%s[0m"%(chr(27), s, chr(27))


def printGreen(s):
	return"%s[32;2m%s%s[0m"%(chr(27), s, chr(27))    

def gb(encoding):
	if encoding is None:
		raise HeEncodingEx, 'unknow encoding'
	encoding = encoding.strip().lower()
	return encodes[encoding] if encoding in encodes else encoding		

def transferToEncoding(filename, toCode):
	if os.path.isdir(filename):
		print "error:not file"
		return False

	try:
		detector = UniversalDetector()
		f = open(filename, 'r')
		ls = f.readlines()
		f.close()

		# 如果空文件没法探测到，所以直接跳出做提示即可
		if len(ls) == 0: 
			print printRed(filename), printRed(' is blank file, can not detect encoding')
			return False;

		# 探测编码
		for l in ls:
			detector.feed(l)
			if detector.done: break
		detector.close()
		
		encode = gb(detector.result['encoding'])
		if encode.lower() != toCode.lower():
			f = open(filename, 'w')
			print printGreen(filename) + ' ====> ' + toCode + ' SUCCESS'
			for l in ls:
				f.write(unicode(l, encode).encode(toCode))
			f.close()
		else:
			pass		
	except Exception, e:
		traceback.print_exc()
		print 'exception'
	finally:
		print
		print
	return True
	

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "input filename toCoding"
		sys.exit(1)

	# default transfer to gbk
	toCode = sys.argv[2] if len(sys.argv) > 2 else "GBK"
	filename = sys.argv[1]
	filterSuffix = sys.argv[3] if len(sys.argv) > 3 else ".js"
	if os.path.isfile(filename):
		transferToEncoding(filename, toCode)
	else:
		import threading
		# 开启多个线程
		THREAD_NUM = 10
		# lock = threading._allocate_lock()

		def fetchAndProcess(files, func):
			while len(files):
				# lock.acquire()
				if len(files) == 0:
					break
				try:
					file_ = files.pop()
				except IndexError, e:
					print e
					break
				# print threading.currentThread(), " thread Count: ", threading.activeCount(), " got : ", file_, " toCode: ", toCode
				# print printGreen(file_), '====> ', toCode, 'is success'
				# lock.release()	
				func(file_, toCode)

		all_files = []
		for base, folders, files in os.walk(filename):
			if not base.endswith(os.sep):
				base += os.sep
			for file_ in files:
				
				if file_.endswith(filterSuffix):
					# print file_, '--'
					all_files.append(base + file_)

		if 1:
			num = THREAD_NUM
			threads = []
			while num:
				num -= 1
				threads.append(threading.Thread(target=fetchAndProcess, args=(all_files, transferToEncoding)))

			for thread_ in threads:
				thread_.start()

			for thread_ in threads:
				thread_.join()										


