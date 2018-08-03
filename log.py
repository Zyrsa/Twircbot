import time, config

class log:
    __ts = 0

    def find_nth(self, haystack, needle, n):
        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start+len(needle))
            n -= 1
        return start

    def logmsg(self, msg = '', incoming = True):
        if incoming:
            user = msg[ 1 : msg.find('!') ]
            text = msg[ (self.find_nth(msg, ':', 2) + 1) : len(msg) ]
        else:
            user = config.nick
            text = msg[ (msg.find(':') + 1) : len(msg) ]
            text = text.strip('\n')

        timestamp = time.strftime('%H:%M:%S', time.gmtime())
        logmsg = timestamp +' <'+ user +'> '+ text +'\n'

        logfile = config.logfile
        if logfile.endswith('.log'):
            logfile = logfile[ 0 : (len(logfile) - 4) ] + time.strftime('-%Y-%m-%d', time.gmtime()) + '.log' 
        else:
            logfile = logfile + time.strftime('-%Y-%m-%d', time.gmtime())

        logfile = open(logfile, 'a+')
        logfile.write(logmsg)
        logfile.close()
