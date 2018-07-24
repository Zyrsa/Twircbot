import os, sys, config

class pid:
    oktorun = False
    
    def __init__(self):
        pid = str(os.getpid())
        
        if os.path.isfile(config.pidfile):
            rpidfile = open(config.pidfile, 'r')
            rpidfile.seek(0)
            old_pid = rpidfile.readline()
            rpidfile.close()
            old_pid = int(old_pid)
            if self.pid_exists(old_pid):
                print('Twircbot already running, exiting...')
                sys.exit()
            else:
                os.remove(config.pidfile)
        
        pidfile = open(config.pidfile, 'w')
        pidfile.write('%s' % pid)
        pidfile.close()
        self.oktorun = True

    def pid_exists(self, pid): 
        if pid < 0: return False
        if sys.platform == 'win32':
            import ctypes
            PROCESS_QUERY_INFROMATION = 0x1000
            processHandle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFROMATION, 0,pid)
            if processHandle == 0:
                return False
            else:
                ctypes.windll.kernel32.CloseHandle(processHandle)
            return True
        else:
            if os.path.exists('/proc/%s' % pid):
                return True
            else:
                return False
    
    def unlink(self):
        os.unlink(config.pidfile)
