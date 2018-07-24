import time, config, pid, irc, db, log

pid = pid.pid()
irc = irc.irc()
db = db.db()
log = log.log()

db.get_raffle_status()

if pid.oktorun:
    try:
        while True:
            time.sleep(1)
            # Output
            out = db.get_next_output(time.time())
            if out:
                sendStr = 'PRIVMSG '+ out[1] +' :'+ out[2] +'\n'
                print(sendStr)
                irc.sendmsg(sendStr)
                log.logmsg(sendStr, False)
                db.delete_output(out[0])

            try:
                msg = irc.getmsg()
                print(msg)
                
                # Reconnect if disconnected
                if len(msg) == 0:
                    irc.connect()
                
                # Prevent Timeout
                if irc.ping(msg):
                    irc.pong(msg)
                
                # Log mentions of us
                if msg.find('PRIVMSG') != -1 and msg.casefold().find(config.ownernick) != -1:
                    log.logmsg(msg)
                
                # Commands in #selfchannel
                if irc.isselfchannel(msg):
                    if irc.isowner(msg):
                        if msg.find('!test') != -1:
                            ts = float(time.time() + 3)
                            chan = str(config.selfchannel)
                            msg = str('bot online')
                            db.write_output(ts, chan, msg)
                        elif msg.find('!online') != -1:
                            ts = float(time.time() + 3)
                            chan = str(config.selfchannel)
                            msg = str('Twircbot is online.')
                            db.write_output(ts, chan, msg)
                        elif msg.find('!joinraffle') != -1:
                            ts = float(time.time() + 3)
                            chan = str(config.selfchannel)
                            msg = str('Will join raffles.')
                            db.set_raffle_status('on')
                            db.write_output(ts, chan, msg)
                        elif msg.find('!nojoinraffle') != -1:
                            ts = float(time.time() + 3)
                            chan = str(config.selfchannel)
                            msg = str('Automatic raffle joining turned off.')
                            db.set_raffle_status('off')
                            db.write_output(ts, chan, msg)
                        elif msg.find('!rafflestatus') != -1:
                            ts = float(time.time() + 3)
                            chan = str(config.selfchannel)
                            rafflestatus = db.get_raffle_status()
                            if rafflestatus == 'on':
                                msg = str('Automatic raffle joining is on.')
                            else:
                                msg = str('Not joining raffles.')
                            db.write_output(ts, chan, msg)

                # Commands and whatnot in #targetchannel
                if irc.istargetchannel(msg):
                    if irc.isshenbot(msg):
                        if msg.find('started a Heist type !heist to help them out.') != -1:
                            ts = float(time.time() + 3)
                            chan = str(config.channel)
                            msg = str('!heist')
                            db.write_output(ts, chan, msg)
                        if msg.find('Stage 1 passed with') != -1:
                            words = msg.split(' ')
                            points = words[-2]
                            points = int(points)
                            ts = time.time()
                            db.new_heist(ts, points)
                        if msg.find('Stage 2 passed with') != -1:
                            words = msg.split(' ')
                            points = words[-2]
                            points = int(points)
                            db.update_heist(points)
                        if msg.find('Stage 3 passed with') != -1:
                            words = msg.split(' ')
                            points = words[-2]
                            points = int(points)
                            db.update_heist(points)
                        if msg.find('Stage 4 passed with') != -1:
                            words = msg.split(' ')
                            points = words[-2]
                            points = int(points)
                            db.update_heist(points)
                            score = db.get_last_heist_score()
                            score = round(score - 1000)
                            ts = float(time.time() + 1)
                            chan = str(config.channel)
                            if score > 1:
                                msg = str('Yay, '+ str(score) +' points profit. shenTea')
                            elif score == 1:
                                msg = str('Yay, '+ str(score) +' point profit. shenTea')
                            elif score == -1:
                                msg = str('No, my point shenRage')
                            elif score < -1:
                                msg = str('No, my '+ str(abs(score)) +' points shenRage')
                            else:
                                msg = str('No profit but no loss either. shenFacepalm')
                            db.write_output(ts, chan, msg)
                        if msg.find('Stage 1 Failed with') != -1:
                            db.new_heist(ts, 0)
                        if msg.find('Stage 2 Failed with') != -1:
                            score = db.get_last_heist_score()
                            score = round(score - 1000)
                            ts = float(time.time() + 1)
                            chan = str(config.channel)
                            if score > 1:
                                msg = str('Yay, '+ str(score) +' points profit. shenTea')
                            elif score == 1:
                                msg = str('Yay, '+ str(score) +' point profit. shenTea')
                            elif score == -1:
                                msg = str('No, my point shenRage')
                            elif score < -1:
                                msg = str('No, my '+ str(abs(score)) +' points shenRage')
                            else:
                                msg = str('No profit but no loss either. shenFacepalm')
                            db.write_output(ts, chan, msg)
                        if msg.find('Stage 3 Failed with') != -1:
                            score = db.get_last_heist_score()
                            score = round(score - 1000)
                            ts = float(time.time() + 1)
                            chan = str(config.channel)
                            if score > 1:
                                msg = str('Yay, '+ str(score) +' points profit. shenTea')
                            elif score == 1:
                                msg = str('Yay, '+ str(score) +' point profit. shenTea')
                            elif score == -1:
                                msg = str('No, my point shenRage')
                            elif score < -1:
                                msg = str('No, my '+ str(abs(score)) +' points shenRage')
                            else:
                                msg = str('No profit but no loss either. shenFacepalm')
                            db.write_output(ts, chan, msg)
                        if msg.find('Stage 4 Failed with') != -1:
                            score = db.get_last_heist_score()
                            score = round(score - 1000)
                            ts = float(time.time() + 1)
                            chan = str(config.channel)
                            if score > 1:
                                msg = str('Yay, '+ str(score) +' points profit. shenTea')
                            elif score == 1:
                                msg = str('Yay, '+ str(score) +' point profit. shenTea')
                            elif score == -1:
                                msg = str('No, my point shenRage')
                            elif score < -1:
                                msg = str('No, my '+ str(abs(score)) +' points shenRage')
                            else:
                                msg = str('No profit but no loss either. shenFacepalm')
                            db.write_output(ts, chan, msg)
                        if msg.find('Type !Raffle in subchat for your chance to win') != -1:
                            rafflestatus = db.get_raffle_status()
                            if rafflestatus == 'on':
                                ts = float(time.time() + 3)
                                chan = str(config.subchan +':'+ config.shenchannelid +':'+ config.shensubchat)
                                msg = str('!raffle')
                                db.write_output(ts, chan, msg)
                        if msg.find('Congratulations to') != -1:
                            if msg.casefold().find(' '+ config.ownernick) != -1:
                                rafflestatus = db.get_raffle_status()
                                if rafflestatus == 'on':
                                    db.set_raffle_status('off')

                # Commands and whatnot in #subchannel
                if irc.issubchannel(msg):
                    if irc.isshenbot(msg):
                        if msg.find('Type !Raffle for your chance to win') != -1:
                            rafflestatus = db.get_raffle_status()
                            if rafflestatus == 'on':
                                ts = float(time.time() + 3)
                                chan = str(config.subchan +':'+ config.shenchannelid +':'+ config.shensubchat)
                                msg = str('!raffle')
                                db.write_output(ts, chan, msg)
                        if msg.find('Congratulations to') != -1:
                            if msg.casefold().find(' '+ config.ownernick) != -1:
                                rafflestatus = db.get_raffle_status()
                                if rafflestatus == 'on':
                                    db.set_raffle_status('off')

            except Exception:
                continue
    finally:
        pid.unlink()