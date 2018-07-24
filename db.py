import sqlite3, config

class db:
    __con = 0
    __c = 0

    def __init__(self):
        self.connect()
        self.__c.execute('CREATE table IF NOT EXISTS settings (id INTEGER PRIMARY KEY AUTOINCREMENT, arg TEXT UNIQUE, val TEXT)')
        self.__c.execute('CREATE table IF NOT EXISTS output (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp REAL, channel TEXT, message TEXT)')
        self.__c.execute('CREATE table IF NOT EXISTS heistscore (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp REAL, points INTEGER)')
        self.__con.commit()
        self.disconnect()

    def connect(self):
        dbfile = config.dbfile
        self.__con = sqlite3.connect(dbfile)
        self.__c = self.__con.cursor()

    def disconnect(self):
        self.__c.close()

    def set_raffle_status(self, value):
        if value != 'on' and value != 'off':
            value = 'off'
        self.connect()
        self.__c.execute('SELECT id FROM settings WHERE arg = ?', ('raffle_status',))
        row = self.__c.fetchone()
        if row == None:
            self.__c.execute('INSERT INTO settings (arg, val) VALUES (?, ?)', ('raffle_status', value))
        else:
            self.__c.execute('UPDATE settings SET val = ? WHERE arg = ?', (value, 'raffle_status'))
        self.__con.commit()
        self.disconnect()
        return True

    def get_raffle_status(self):
        self.connect()
        self.__c.execute('SELECT val FROM settings WHERE arg = ?', ('raffle_status',))
        row = self.__c.fetchone()
        if row == None:
            self.__c.execute('INSERT INTO settings (arg, val) VALUES (?, ?)', ('raffle_status', 'off'))
            self.__con.commit()
            self.disconnect()
            return False
        else:
            self.disconnect()
            if row[0] == 'off':
                return 'off'
            elif row[0] == 'on':
                return 'on'
            else:
                return 'off'

    def write_output(self, ts, chan, msg):
        self.connect()
        self.__c.execute('INSERT INTO output (timestamp, channel, message) VALUES (?, ?, ?)', (ts, chan, msg))
        self.__con.commit()
        self.disconnect()
        return True

    def delete_output(self, oid):
        self.connect()
        self.__c.execute('DELETE FROM output WHERE id = ?', (oid,))
        self.__con.commit()
        self.disconnect()
        return True

    def get_next_output(self, ts):
        self.connect()
        self.__c.execute('SELECT id, channel, message FROM output WHERE timestamp < ? ORDER BY timestamp ASC LIMIT 1', (ts,))
        row = self.__c.fetchone()
        if row == None:
            self.disconnect()
            return False
        else:
            self.disconnect()
            return row
        return False
    
    def new_heist(self, ts, points):
        self.connect()
        self.__c.execute('INSERT INTO heistscore (timestamp, points) VALUES (?, ?)', (ts, points))
        self.__con.commit()
        insert_id = self.__c.lastrowid
        self.__c.execute('SELECT id FROM settings WHERE arg = ?', ('lastheist_id',))
        row = self.__c.fetchone()
        if row == None:
            self.__c.execute('INSERT INTO settings (arg, val) VALUES (?, ?)', ('lastheist_id', insert_id))
        else:
            self.__c.execute('UPDATE settings SET val = ? WHERE arg = ?', (insert_id, 'lastheist_id'))
        self.__con.commit()
        self.disconnect()
        return True
    
    def update_heist(self, points):
        self.connect()
        self.__c.execute('SELECT val FROM settings WHERE arg = ?', ('lastheist_id',))
        row = self.__c.fetchone()
        if row == None:
            self.disconnect()
            return False
        else:
            self.__c.execute('UPDATE heistscore SET points = points + ? WHERE id = ?', (points, row[0]))
            self.__con.commit()
            self.disconnect()
            return True
        return False
    
    def get_last_heist_score(self):
        self.connect()
        self.__c.execute('SELECT val FROM settings WHERE arg = ?', ('lastheist_id',))
        row = self.__c.fetchone()
        if row == None:
            self.disconnect()
            return False
        else:
            lastheist_id = row[0]
            self.__c.execute('SELECT points FROM heistscore WHERE id = ?', (lastheist_id,))
            row = self.__c.fetchone()
            if row == None:
                self.disconnect()
                return False
            else:
                points = row[0]
                self.disconnect()
                return points
        return False