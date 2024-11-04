import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from flask import Flask, request, send_file
import io

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="fin")
    c = _conn.cursor()

    return c, _conn




def owner_reg(username,password,email,mobile,address):
    try:
        c, conn = db_connect()
        print(username,password,email,address)
        id="0"
        status = "pending"
        j = c.execute("insert into user (id,username,password,email,mobile,address,status) values ('"+id +
                      "','"+username+"','"+password+"','"+email+"','"+mobile+"','"+address+"','"+status+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    

def te_act(username,income,expenses,dt):
    try:
        c, conn = db_connect()
        print(username,income,expenses,dt)
        id="0"
        status = "pending"
        i = int(income)
        e = int(expenses)
        s = i-e
        print(s)
        j = c.execute("insert into track (id,username,income,expenses,savings,dt) values ('"+id +
                      "','"+username+"','"+income+"','"+expenses+"','"+str(s)+"','"+dt+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    

def g_act(username,gname,tamount,camount):
    try:
        c, conn = db_connect()
        print(username,gname,tamount,camount)
        id="0"
        status = "pending"
        j = c.execute("insert into goal (id,username,gname,tamount,camount) values ('"+id +
                      "','"+username+"','"+gname+"','"+tamount+"','"+camount+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    


def g1_act(username,gname,tamount,fa):
    try:
        c, conn = db_connect()
        print(username,gname,tamount,fa)
        id="0"
        status = "pending"
        j = c.execute("update goal set camount='"+str(fa)+"' where username = '"+username+"' and gname='"+gname+"'  ")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
    


def owner_login(username, password):
    try:
        c, conn = db_connect()
        
        j = c.execute("select * from user where username='" +
                      username+"' and password='"+password+"'   "  )
        c.fetchall()
        
        conn.close()
        return j
    except Exception as e:
        return(str(e))
    


def vtrack(username):
    c, conn = db_connect()
    c.execute("select * from track where username = '"+username+"'  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

def vgoal(username):
    c, conn = db_connect()
    c.execute("select * from goal where username = '"+username+"'  ")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


# -------------------------------Registration-----------------------------------------------------------------
