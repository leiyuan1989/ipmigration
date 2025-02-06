import sys
import os
import datetime

class Logger(object):
    def __init__(self, filename='default.log', add_flag=True, stream=sys.stdout):
        self.terminal = stream
        self.log_file_dir=str(os.getcwd())+r"/log/"
        self._mkdir(self.log_file_dir)
        print("filename:", filename)
        self.filename=self.log_file_dir+filename
        self.add_flag=add_flag
        #self.log = open(filename, 'w', encoding="utf-8")
        
    def _mkdir(self,path):
        folder=os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("set up new log folder:", path)
            print("---- Successful ----")
        else:
            print("Exist log folder:", path)

    def write(self, message):
        if self.add_flag:
            with open(self.filename, "a+") as log:
                self.terminal.write(message)
                log.write(message)
        else:
            with open(self.filename, "w") as log:
                self.terminal.write(message)
                log.write(message)

    def flush(self):
	    pass
    
    
def record_log(log_flag, logfilename_prefix):
    date_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logfilename=logfilename_prefix+date_time+".log"
    if log_flag:
        sys.stdout = Logger(logfilename)

'''
date_time=datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
filename="test_"+date_time+".log"
sys.stdout = Logger(filename)

# now it works
#print("print something")
#print("output")
'''


