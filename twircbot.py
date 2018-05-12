import time, config, irc, log, pid

irc = irc.IRC()
log = log.LOG()
pid = pid.PID()

joinraffle = False

if pid.oktorun:
    try:
        while 1:
            time.sleep(0.25)

            try:
                msg = irc.getmsg()
                print(msg)
                #if msg.find('PRIVMSG') != -1:
                #    log.logmsg(msg)

                # Reconnect if disconnected
                if len(msg) == 0:
                    irc.connect()

                # Prevent Timeout
                if irc.ping(msg):
                    irc.pong(msg)
                    
                # Commands in #selfchannel
                if irc.isselfchannel(msg):
                    if irc.isowner(msg):
                        if msg.find('!online') != -1:
                            time.sleep(10)
                            sendStr = 'PRIVMSG '+ config.selfchannel +' :Twircbot is online.\n'
                            irc.sendmsg(sendStr)
                            #log.logmsg(sendStr, False)
                        elif msg.find('!joinraffle') != -1:
                            time.sleep(10)
                            joinraffle = True
                            sendStr = 'PRIVMSG '+ config.selfchannel +' :Will join raffles.\n'
                            irc.sendmsg(sendStr)
                            #log.logmsg(sendStr, False)
                        elif msg.find('!rafflestatus') != -1:
                            time.sleep(10)
                            if joinraffle == True:
                                sendStr = 'PRIVMSG '+ config.selfchannel +' :Currently joining raffles.\n'
                            else:
                                sendStr = 'PRIVMSG '+ config.selfchannel +' :Not joining raffles.\n'
                            irc.sendmsg(sendStr)
                            #log.logmsg(sendStr, False)

                # Commands and whatnot in #targetchannel
                if irc.istargetchannel(msg):
                    if irc.isshenbot(msg):
                        if msg.find('started a Heist type !heist to help them out.') != -1:
                            sendStr = 'PRIVMSG '+ config.channel +' :!heist\n'
                            irc.sendmsg(sendStr)
                            #log.logmsg(sendStr, False)
                        if msg.find('Type !Raffle for your chance to win') != -1:
                            if joinraffle == True:
                                sendStr = 'PRIVMSG '+ config.channel +' :!raffle\n'
                                irc.sendmsg(sendStr)
                                #log.logmsg(sendStr, False)
                        if msg.find('Congratulations to') != -1:
                            if msg.find(' zyrsa ') != -1:
                                joinraffle = False
                
                # Commands and whatnot in #subchannel
                if irc.issubchannel(msg):
                    if irc.isshenbot(msg):
                        if msg.find('Type !Raffle for your chance to win') != -1:
                            if joinraffle == True:
                                sendStr = 'PRIVMSG #chatrooms:'+ config.shenchannelid +':'+ config.shensubchat +' :!raffle\n'
                                irc.sendmsg(sendStr)
                                #log.logmsg(sendStr, False)
                        if msg.find('Congratulations to') != -1:
                            if msg.find(' zyrsa ') != -1:
                                joinraffle = False

            except Exception:
                continue
    finally:
        pid.unlink()
