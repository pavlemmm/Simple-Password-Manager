#!/usr/bin/python3
from colorama import init as colorama, Fore, Style, Back
from pynput.keyboard import Listener
from sys import exit, platform
from math import floor, ceil
import sqlite3 as sql
import pyperclip
import argparse
import random
import time
import os

if platform == 'win32':
    isWin = True
else:
    isWin = False

colorama()
bckst = Back.GREEN+Fore.BLACK
bcked = Back.RESET+Fore.RESET

cnn = sql.connect('database.db')
c = cnn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS t (
    info text,
    email text,
    password text
)''')

def main():
    if isWin:
        os.system('cls')
    else:
        os.system('clear')

    print(Fore.LIGHTGREEN_EX + 'PavleM\'s PW Manager\n\n' + Fore.RESET + '1) Sql console\n2) Find details from info\n3) Find details from email\n4) Input and pw creator\n')
    
    br = input(bckst+"main$"+bcked+" ")

    if br == '1':
        console()
    elif br == '2':
        byinfo()
    elif br == '3':
        byemail()
    elif br == '4':
        simpleinput()
    elif br == 'qq':
        print()
        exit()
    else:
        main()

temp = ""
def on_press(key):
    global temp
    if isWin:
        if str(key) == r"""'\x16'""":
            return False
    else:
        if temp == "Key.ctrl" and str(key) == """'v'""":
            return False
        temp = str(key)

def fetch():
    br = 0
    out = c.fetchall()

    max = [4, 5, 8]
    for item in out:
        for i, it in enumerate(item):
            if len(it) > max[i]:
                max[i] = len(it)

    b = Fore.LIGHTGREEN_EX
    r = Fore.RESET

    header = "| "+" "*floor(max[0]/2-2)+b+"INFO"+r+" "*ceil(max[0]/2-2)+" | "+" "*floor(max[1]/2-2.5)+b+"EMAIL"+r+" "*ceil(max[1]/2-2.5)+" | "+" "*floor(max[2]/2-4)+b+"PASSWORD"+r+" "*ceil(max[2]/2-4)+" |"
    border = " "*3+"+"+"-"*(max[0]+2) + "+" + "-"*(max[1]+2) + "+" + "-"*(max[2]+2) + "+"
    
    print("\n"+border)
    print(" "*3+header)
    print(border)

    b = Style.DIM
    r = Style.RESET_ALL

    for item in out:
        br+=1
        if br%2 == 0:
            print(b+str(br)+r+"."+" | "+b+item[0]+r+" "*(max[0]-len(item[0]))+" | "+b+item[1]+r+" "*(max[1]-len(item[1]))+" | "+b+item[2]+r+" "*(max[2]-len(item[2]))+" | ")
        else:
            print(str(br)+"."+" | "+item[0]+" "*(max[0]-len(item[0]))+" | "+item[1]+" "*(max[1]-len(item[1]))+" | "+item[2]+" "*(max[2]-len(item[2]))+" | ")

    print(border+"\n")


    index = 0
    if len(out) > 1:
        try:
            index = int(input(bckst+"Type row number to copy details or any letter to skip:"+bcked+" "))
        except:
            print()
            return
        pyperclip.copy(out[index-1][1])
        print("email copied to clipboard")
        with Listener(on_press=on_press) as l:
            l.join()
        time.sleep(0.4)
        pyperclip.copy(out[index-1][2])
        print("password copied to clipboard\n")
    elif len(out) == 1:
        pyperclip.copy(out[0][1])
        print("email copied to clipboard")
        with Listener(on_press=on_press) as l:
            l.join()
        time.sleep(0.4)
        pyperclip.copy(out[0][2])
        print("password copied to clipboard\n")

def console():
    print(Fore.LIGHTGREEN_EX+'\nSql console\n'+Fore.RESET+'q to return to main function\nt(info, email, password)', end='\n\n')
    i=""
    while True:
        i = input(bckst+"main/console$"+bcked+" ")

        if i == "q":
            main()
        elif i == "*":
            c.execute("select * from t")
            fetch()
            continue

        try:
            c.execute(i)
            fetch()
            cnn.commit()
        except:
            print("Bad sql command", end='\n\n')

def byinfo():
    print(Fore.LIGHTGREEN_EX+'\nFind by info\n'+Fore.RESET+'q to return to main function\nInput app info', end='\n\n')
    i=""
    while True:
        i = input(bckst+"main/byinfo$"+bcked+" ")

        if i == "q":
            main()
        
        try:
            c.execute(f"""select * from t where info like '%{i}%'""")
            fetch()
        except:
            print("Bad sql command", end='\n\n')

def byemail():
    print(Fore.LIGHTGREEN_EX+'\nFind by email\n'+Fore.RESET+'q to return to main function\nInput email', end='\n\n')
    i=""
    while True:
        i = input(bckst+"main/byemail$"+bcked+" ")

        if i == "q":
            main()
        
        try:
            c.execute(f"""select * from t where email like '%{i}%'""")
            fetch()
        except:
            print("Bad sql command", end='\n\n')

def simpleinput():
    print(Fore.LIGHTGREEN_EX+'\nInput and pw creator\n'+Fore.RESET+'q to return to main function\nInput in this form: info email', end='\n\n')
    
    while True:
        i = input(bckst+"main/simpleinput$"+bcked+" ")

        if i == "q":
            main()

        i = i.split(" ")
        createpass(i)

def createpass(i):
    allchars = ('abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTYVWXYZ', '0123456789', ',._-*~"<>/|!@#$%^&()+=')
    pw=""
    for j in allchars:
        for _ in range(6):
            pw += j[random.randint(0, len(j)-1)]

    pw = list(pw)
    random.shuffle(pw)
    pw = ''.join(pw)
    
    i.append(pw)

    try:
        c.execute(f"""insert into t values("{i[0]}", "{i[1]}", "{i[2]}")""")
        cnn.commit()
        print("Successfully inserted")
        print(pw + " copied to clipboard\n")
        pyperclip.copy(pw)
    except:
        print("Bad sql command", end='\n\n')


parser = argparse.ArgumentParser(description='PavleM\'s Password Manager')
parser.add_argument('-c', '--console', help='sql console', required=False)
parser.add_argument('-s', '--search', help='search login credentials by info', required=False)
parser.add_argument('-e', '--email', help='search login credentials by email', required=False)
parser.add_argument('-a', '--add', help='''add new login credentials\nInput in form: info,email or "info email"''',required=False)
args = parser.parse_args()

if args.console:
    if args.console == "*":
        c.execute("select * from t")
    else:
        c.execute(args.console)
    fetch()
    exit()
elif args.search:
    c.execute(f"""select * from t where info like '%{args.search}%'""")
    fetch()
    exit()
elif args.email:
    c.execute(f"""select * from t where email like '%{args.email}%'""")
    fetch()
    exit()
elif args.add:
    l =[]
    l = str(args.add).split(' ')
    if len(l) == 1:
        l = str(args.add).split(',')
    createpass(l)
    exit()


main()
