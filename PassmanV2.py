# to retrieve creds of more than 2 services at the same time if there are multiple accounts on the same service. ----Important---- 
# we will create a google form with password habits, which will then be converted into csv data and visualised using matplotlib. it will be a secondary feature of the password manager.c
from logging import error
from colorama.initialise import init, reset_all
import mysql.connector as m
import time as t
from mysql.connector import cursor
import pyperclip
from colorama import Fore,Back,Style
import pandas as pd
from nltk import flatten
import matplotlib.pyplot as p
from getpass import getpass

init(convert=True) #colorama

def copy(thing_to_copy):                        
    pyperclip.copy(thing_to_copy)

a = pd.read_csv("C:\\Users\\Madhav Bhatnagar\\Downloads\\Password Habits pakka final.csv\\Password Habits.csv", skiprows=[0], header=None)  # change the location of the CSV file here, note: add the double \\
a.columns = ["age", "accounts", "reuse", "change", "2FA", "store", "better", "misc"]

a = pd.DataFrame(a, index = None)

age = a["age"]
accounts = a["accounts"]
reuse = a["reuse"]
fa = a["2FA"]
store = a["store"]
better = a["better"]
misc = a["misc"]
change = a["change"]

def plt(elem):
    if elem == "accounts":
        p.hist(accounts)
        p.title("number of accounts")
        p.ylabel("number of people")
        p.show()
    elif elem == "reuse":
        p.hist(reuse)
        p.title("do you reuse passwords?")
        p.ylabel("number of people")
        p.show()
    elif elem == "fa":
        p.hist(fa)
        p.title("do you enable 2 factor authentication?")
        p.ylabel("number of people")
        p.show()
    elif elem == "store":
        p.hist(store
        )
        p.xlabel("medium")
        p.title("how do you store your passwords?")
        p.ylabel("number of people")
        p.show()
    elif elem == "change":
        p.hist(change)
        p.title("How often do you change your passwords?")
        p.ylabel("number of people")
        p.show()


def change_masterpass():
    try:
        conn = m.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'passmanagerschool'
        )
        masterpass = input("enter the new masterpassword: ")

        cursor = conn.cursor()
        cursor.execute("update masterpass set masterpass = '{}'".format(masterpass))
        conn.commit()
        print("updating masterpassword....")
        t.sleep(1)
    except m.Error as error:
        print("error ho gaya bhaiya: ", error, " Developer ko report kardo pls")

def update_password():
    try:
        conn = m.connect(
                host = 'localhost',
                user = 'root',
                password = 'root',
                database = 'passmanagerschool'
            )
        user = input("enter the username used: ")
        service = input("enter the name of the service: ")
        new_password = input('enter the new password: ')
        cursor = conn.cursor()    
        cursor.execute("update userpass set password = '{passw}' where user = '{usern}' and appname = '{serv}';".format(passw = new_password, usern = user, serv = service))
        conn.commit()
        print("updating password.....")
        t.sleep(1)
        print('done!')
        t.sleep(3)
    except m.Error as error:
        print("an error occurred ", error, "please report to the developer")

def show_all():                                 # can be used but is not used bevause does not print whole dataframes which is required by the projet parameters
    conn = m.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'passmanagerschool'
    )
    total = []  
    sql = '''select appname from userpass;'''
    cursor = conn.cursor(buffered=True)
    cursor.execute(sql)
    conn.commit()
    result = list(cursor.fetchall())

    for i in result:
        i = ''.join(i)
        total.append(i)
    creds(total)
    t.sleep(3)

def show_all2():
    conn = m.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'passmanagerschool'
    )

    everything = pd.read_sql("""select * from userpass;""", conn)
    print("loading results.....")
    t.sleep(2)
    print(Back.GREEN)
    print(Fore.BLACK)
    print(everything)
    print(Style.RESET_ALL)
    t.sleep(3)

def creds(the_list):
    for i in the_list:
        display_username_with_pass(i)
        print('+'*50)

def find_password_with_appname():
        conn = m.connect(
                host = 'localhost',
                user = 'root',
                password = 'root',
                database = 'passmanagerschool'
                )
        appname = str(input("enter the name of the app: "))
        try:
            df = pd.read_sql("""select password from userpass where appname = '{appname}';""".format(appname = appname), conn)

            display_username_with_pass(appname)
        except m.Error as error:
            print("there was an error: ", error)
            t.sleep(2)

def display_username_with_pass(service):
    try:
        conn = m.connect(
                host = 'localhost',
                user = 'root',
                password = 'root',
                database = 'passmanagerschool'
                )
        user = pd.read_sql(""" select user from userpass where appname = '{appname}';""".format(appname = service), conn)
        print(Fore.YELLOW)
        print("Username ==> \n",user)
        print(Style.RESET_ALL)
        listuser = user.values.tolist()
        flattenedlistuser = flatten(listuser)
        user = flattenedlistuser[0]
        display_pass(user)
    except m.errors as error:
        print("there was an error: ", error)

def display_pass(user):
    try:
        conn = m.connect(
                host = 'localhost',
                user = 'root',
                password = 'root',
                database = 'passmanagerschool'
                )
        password = pd.read_sql(""" select password from userpass where user = '{}';""".format(user), conn)
        print(Fore.GREEN)
        print("password ==> \n",password)
        print(Style.RESET_ALL)
        display_service(user)
    except m.errors as error:
        print("there was an error: ", error)

def display_service(user):
    try:
        conn = m.connect(
            host = 'localhost',
            user = 'root',
            password = 'root',
            database = 'passmanagerschool'
        )
        service = pd.read_sql("""select appname from userpass where user = '{}'""".format(user), conn)
        print(Fore.CYAN)
        print("Appname ==> ", service)
        print(Style.RESET_ALL)
        t.sleep(3)
    except m.Error as error:
        print("error ho gaya bhai: ", error)

def store_password(app_user, app_pass, app_name):           #backend
    try:
        conn = m.connect( 
            host = 'localhost',
            user =  'root',
            password = 'root',
            database = 'passmanagerschool')

        cursor = conn.cursor(buffered=True)
        sql_query = ("""insert into userpass values ( %s , %s , %s)""")
        Data_Insertions = (app_user, app_pass, app_name)
        cursor.execute(sql_query,Data_Insertions)
        conn.commit()

        print('-'*100)
        print("\n ===>  ", app_pass)
        print('-'*100)
        pyperclip.copy(app_pass)
        print(Fore.GREEN+" \n The password has been added and copied to your clipboard!")
        print(Style.RESET_ALL)
        t.sleep(3)

    except m.Error as error:    
        print("something went wrong:", error, "please restart the program")

def copy(thing_to_copy):
    pyperclip.copy(thing_to_copy)

def AddPassword():
        print(Fore.GREEN)                                         #frontend
        app_user = input("Enter the username or email used in this app: ")
        app_pass = input("Suggest a password to use in this app: ")
        app_name = input("Enter the name of the app: ") 
        print(Style.RESET_ALL)
        store_password(app_user, app_pass, app_name)

def connect_auth():
    try:
        connn = m.connect(
            host = 'localhost',
            user = 'root',                  # function to authorize the person, the first step.
            password = 'root',
            database = 'passmanagerschool')

        secretkey = getpass("enter the master password: ")

        sqlquery = """select * from masterpass;"""          
        cursor = connn.cursor(buffered=True)
        cursor.execute(sqlquery)
        connn.commit()
        
        result = list(cursor.fetchone())
        str = ''.join(result)
        if secretkey == str:
            print("You're In!")
            t.sleep(1)
            while True:
                menu()
        else:
            print('better luck next time. quitting......')
            t.sleep(1)
            quit()

    except m.Error as error:
        print('something went wrong: ', error, "please restart the program")

def datavisualmenu():
    while True:
        print(Fore.LIGHTWHITE_EX + '''
            
  _____        _         __      ___                 _ _           _   _             
 |  __ \      | |        \ \    / (_)               | (_)         | | (_)            
 | |  | | __ _| |_ __ _   \ \  / / _ ___ _   _  __ _| |_ ___  __ _| |_ _  ___  _ __  
 | |  | |/ _` | __/ _` |   \ \/ / | / __| | | |/ _` | | / __|/ _` | __| |/ _ \| '_ \ 
 | |__| | (_| | || (_| |    \  /  | \__ \ |_| | (_| | | \__ \ (_| | |_| | (_) | | | |
 |_____/ \__,_|\__\__,_|     \/   |_|___/\__,_|\__,_|_|_|___/\__,_|\__|_|\___/|_| |_|
                                                                                     
                                                                                     

        ''')
        print(Fore.GREEN + '1. data for number of password protected accounts\n')
        print(Fore.RED + '2. Data for password reuse\n')
        print(Fore.BLUE + '3. Data for enabling 2 factor authentication\n')
        print(Fore.CYAN + '4. Data for Password storage mediums\n')
        print(Fore.YELLOW + '5. Data for password change frequency\n')
        print(Style.RESET_ALL)
        print('q : to back to the password manager\n')

        nav = str(input("=> "))
        if nav == '1':
            plt("accounts")
        elif nav == '2':
            plt("reuse")
        elif nav == '3':
            plt("fa")
        elif nav == '4':
            plt("store")
        elif nav == '5':
            plt("change")
        elif nav == 'q':
            break
        else:
            print("enter a valid command")
            t.sleep(2)

def menu():                                                 #frontend   
    print(Fore.RED + '''
    ____                                          __            __  ___                                 
   / __ \____ ____________      ______  _________/ /           /  |/  /___ _____  ____ _____ ____  _____
  / /_/ / __ `/ ___/ ___| | /| / / __ \/ ___/ __  /  ______   / /|_/ / __ `/ __ \/ __ `/ __ `/ _ \/ ___/
 / ____/ /_/ (__  (__  )| |/ |/ / /_/ / /  / /_/ /  /_____/  / /  / / /_/ / / / / /_/ / /_/ /  __/ /    
/_/    \__,_/____/____/ |__/|__/\____/_/   \__,_/           /_/  /_/\__,_/_/ /_/\__,_/\__, /\___/_/     
                                                                                     /____/  

    MySQL Database Integration!                                                                     ver.1.19.1                 
''')
    print(Style.RESET_ALL)
    print(Fore.GREEN+' 1. Add new password for a website/App.\n')
    print(Fore.YELLOW+' 2. Find a password used within an app.\n')
    print(Fore.LIGHTMAGENTA_EX+' 3. Show All Passwords\n')
    print(Fore.LIGHTYELLOW_EX+" 4. Update Passwords\n")      
    print(Fore.CYAN+' 5. Change MasterPassword.\n')
    print(Fore.LIGHTMAGENTA_EX + ' 6. Data visualisation menu\n')
    print(Style.RESET_ALL)  
    print(' q : quit')

    nav = str(input("=> ")) 
    if nav == '1':
        AddPassword()
    elif nav == '2':
        find_password_with_appname()
    elif nav == '3':
         show_all2()    
    elif nav == '4':
        update_password()
    elif nav == '5':
        change_masterpass()  
    elif nav == '6':
        datavisualmenu() 
    elif nav == 'q':
        quit()
    else:
        print("enter a valid command")
        
if __name__ == "__main__":
    connect_auth()
