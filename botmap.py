"""World map and node handling."""
import os
import sqlite3
import path

map_name = 'worldmap.txt'

_map_path = path.get_path()
_map_path = _map_path + 'data\\' + map_name 
map = open(_map_path)
map = map.read()
map_rows = map.split() #Split the map into lines
map_row = []

def node(_row, _col):
    """Get a node."""
    map_row = map_rows[_row]
    _colend = _col + 4
    map_col = map_row[_col:_colend]     #  Get a string of 4 characters long.
    return map_col

def map_scan():
    """Scan worldmap.txt and store it in botterlord.db nodes table."""
    conn = sqlite3.connect('botterlord.db')
    db = conn.cursor()
    stored_new = 0
    map_row = None
    _colend = 0
    _col = 0
    map_list = map.split()
    map_list_len = len(map_list)    #  Get number of objects in list
    for _row in range(0, map_list_len):     #  Start with the first object
        """_row and _col is the number of current row and col."""
        cur_row = map_list[_row]    #  map_list[i] the i'th object in list
        row_len = len(map_list[_row])   #  Length of current line

        for _col in range(0, row_len, 4):
            repr_node = node(_row, _col)
            _addr = '%d:%d'  %(_row, _col)
            _addrdb = (_addr,)
            _node = [_addr, repr_node, 'None']
            db.execute('SELECT * FROM NODES WHERE ADDR = ?', _addrdb)
            if db.fetchone() == None: #If there is no node with the same address
                db.execute('INSERT INTO NODES VALUES (?,?,?)', _node)
                stored_new += 1
            else:
                continue
            print node(_row, _col)
    conn.commit()
    conn.close()
    print "botmap: %d nodes added to the database." %(stored_new)

def get_node(_addr_):
    """Fetch a node from the database file."""
    conn = sqlite3.connect('botterlord.db')
    db = conn.cursor()
    _addrdb_ = (_addr_,)
    db.execute('SELECT * FROM NODES WHERE ADDR = ?', _addrdb_)
    return db.fetchone()
    conn.commit()
    conn.close()

print get_node('10:40')

def recog_node(_addr_):
    cur_node = get_node(_addr_)
    node_sign = cur_node[1]
    if node_sign == '^^^^':
        return 'a Forest'
    else: return 'Unknown'
