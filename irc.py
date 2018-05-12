import socket, ssl, config

class IRC:
    __sock = 0
    
    def __init__(self):
        self.connect()
        
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock = ssl.wrap_socket(sock)
        print('Connecting to %s:%s' % (config.server, config.port))
        self.__sock.connect((config.server, config.port))
        self.__sock.setblocking(False)
        if config.password != '':
            self.sendmsg('PASS '+ config.password +'\n')
        self.sendmsg('USER '+ config.nick +' '+ config.nick +' '+ config.nick +' :Twircbot\n')
        self.sendmsg('NICK '+ config.nick +'\n')
        self.sendmsg('JOIN '+ config.selfchannel +'\n')
        self.sendmsg('JOIN '+ config.channel +'\n')
        self.sendmsg('JOIN #chatrooms:'+ config.shenchannelid +':'+ config.shensubchat +'\n')
        self.sendmsg('CAP REQ :twitch.tv/membership\n')
        #self.sendmsg('CAP REQ :twitch.tv/tags\n')
        self.sendmsg('CAP REQ :twitch.tv/commands\n')
    
    def sendmsg(self, msg):
        self.__sock.send(bytes(msg, 'UTF-8'))
        
    def getmsg(self):
        msg = self.__sock.recv(2040).decode('UTF-8')
        msg = msg.strip('\n\r')
        return msg
    
    def ping(self, msg = ''):
        if msg.find('PING') != -1:
            return True
        else:
            return False
    
    def pong(self, msg = ''):
        self.sendmsg('PONG '+ msg.split() [1] +'\r\n')
        
    def isselfchannel(self, msg = ''):
        if msg.find(' PRIVMSG %s :' % (config.selfchannel)) != -1:
            return True
        else:
            return False
    
    def istargetchannel(self, msg = ''):
        if msg.find(' PRIVMSG %s :' % (config.channel)) != -1:
            return True
        else:
            return False
    
    def issubchannel(self, msg = ''):
        if msg.find(' PRIVMSG #chatrooms:%s:%s :' % (config.shenchannelid, config.shensubchat)) != -1:
            return True
        else:
            return False
    
    def isshenbot(self, msg = ''):
        if msg.startswith(':%s PRIVMSG ' % (config.shenbot)):
            return True
        else:
            return False
    
    def isowner(self, msg = ''):
        if msg.startswith(':%s PRIVMSG ' % (config.owner)):
            return True
        else:
            return False