#error handling karni hai bhaiya ji 

import cryptography.fernet as fernet
import mysql.connector as m
import time as t
from mysql.connector import cursor

def generate_key():
    key = fernet.Fernet.generate_key()
    with open("C:\\Users\\Public\\Documents\\sqlkey.txt", "wb") as key_file:
        key_file.write(key)
    print("=>generating encryption key.....\n")
    t.sleep(3)

def database():
    conn = m.connect(
        host = 'localhost',
        user = 'root',
        password = 'root'
    )
    create = """create database passmanagerschool;"""
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute(create)
        conn.commit()

        print("=>Creating Database in MYSQL DBMS.............\n")
        t.sleep(4)
    except m.errors as error:
        print('there was an error:', error, "please restart the program")
        print("please start the setup again")

def tables():
    conn = m.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'passmanagerschool'
    )
    count = 1
    use, create_table, create_master = """use passmanagerschool;""","""create table userpass ( user varchar(50), password varchar (256), appname varchar(30)); ""","""create table masterpass ( masterpassword varchar(30));"""

    cursor = conn.cursor(buffered=True)
    cursor.execute(use)
    print('creating table 1')
    conn.commit()
    t.sleep(2)
    cursor.execute(create_table)
    print('creating table 2')
    conn.commit()
    t.sleep(2)
    cursor.execute(create_master)
    print('creating table 3')
    conn.commit()
    t.sleep(2)
    print("=>Table Creation Completed!\n")

def masterpass():
    print("YOU ARE ABOUT TO ENTER THE MASTERPASSWORD, THIS IS THE ONLY PASSWORD YOU HAVE TO REMEMBER WHILST USING THIS MANAGER. REMEMBER IT OR WRITE IT DOWN! \n YOU CAN CHANGE THIS PASSWORD IN THE FUTURE.\n")
    masterpassword = input("\nEnter A MasterPassword For The Manager: ")

    conn = m.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'passmanagerschool'
    )
    cursor = conn.cursor(buffered=True)

    cursor.execute(("insert into masterpass values ('{masterpass}');").format(masterpass=masterpassword))
    conn.commit()
    print("=>establishing masterpassword in the database.......\n")
    t.sleep(3)

if __name__ == "__main__":
    generate_key()
    database()
    tables()
    masterpass()


print("\n CONGRATULATIONS, THE SETUP IS COMPLETE, YOU CAN NOW POWER UP THE PASSMANAGER AND USE! \n")
print("DEV - MadhavBhatnagar/Lu3if4r")

t.sleep(60)