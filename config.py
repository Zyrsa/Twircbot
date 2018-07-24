# irc server & port, twitch as default since twircbot
server = 'irc.chat.twitch.tv'
port = 6697

# your nick
nick = 'NICK'
# oauth
password = 'PASSWORD'

# target channel
channel = '#CHANNEL'
# your nick
selfchannel = '#SELFCHANNEL'

#
# These things you'll have to figure out yourself for your
# intended use. This is to join "sub" chatrooms such as subscriber
# only chatrooms or whatnot. Twitch has good documentation on
# how to find this at https://dev.twitch.tv/docs/irc/
#
# typically #chatrooms
subchan = '#SUBCHANNEL'
# you'll have to find this yourself
shenchannelid = 'ID'
# you'll have to find this yourself
shensubchat = 'STR'

# nick!ident@host
shenbot = 'BOT'

# nick!ident@host
owner = 'SELF'
# nick
ownernick = 'NICK'

# you can leave these as is
pidfile = 'run.pid'
logfile = 'logs/twircbot.log'
dbfile = 'db/twircbot.db'
