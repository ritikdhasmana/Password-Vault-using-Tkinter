from os import curdir, popen
import sqlite3, hashlib
from sqlite3.dbapi2 import Cursor

from tkinter import *

from tkinter import simpledialog
from functools import partial
################## Database #########################


with sqlite3.connect('pass_vault.db') as db:
    Cursor = db.cursor()

Cursor.execute('''
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL);

''')

Cursor.execute('''
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
userapp TEXT NOT NULL,
password TEXT NOT NULL);

''')


####################  HASH ###########################

def Hashpasswords(userp):
    hash = hashlib.md5(userp)
    hash = hash.hexdigest()

    return hash



#################### Pop up ###########################

def Popup(text):
    ans = simpledialog.askstring('Add', text)
    return ans



################# Window gui ########################
window = Tk()

window.title('Password vault')
window.config(bg='BLACK')


def InitialScreen():
    window.geometry('650x400')
    passw_var1= StringVar()
    passw_var2= StringVar()
    label1 = Label(window, text='Create master password',font=("Arial", 15), bg='BLACK',fg='WHITE').place(x=240,y = 115)
    entry1 = Entry(window,width = 30,textvariable=passw_var1,show='*').place(x = 243,  y = 160)

    label2 = Label(window, text='Re-enter master password',font=("Arial", 15), bg='BLACK',fg='WHITE').place(x=240,y = 215)
    entry2 = Entry(window,width = 30,textvariable=passw_var2,show='*').place(x = 243,  y = 260)
    
    label3 = Label(window,text='',bg='BLACK',fg='BLACK')
    label3.pack()

    def _savepassword():
        if passw_var1.get() == passw_var2.get():
            hashed_pass = Hashpasswords(passw_var2.get().encode('utf-8'))


            insert_pass = '''INSERT INTO masterpassword(password)
            values(?)'''
            Cursor.execute(insert_pass, [(hashed_pass)])

            db.commit()
            print(hashed_pass)
            PasswordVault()
        else :
            label3.config( text='Passwords do not match!',font=("Arial", 15), bg='BLACK',fg='RED')


    button1 = Button(window,text='Submit',command= _savepassword).place(x = 310,
                                                   y = 300)


def LoginScreen():
    window.geometry('650x400')
    passw_var= StringVar()
    label1 = Label(window, text='Enter master password',font=("Arial", 15), bg='BLACK',fg='WHITE').place(x=230,y = 155)
    entry1 = Entry(window,width = 30,textvariable=passw_var,show='*').place(x = 242,  y = 200)

    label2 = Label(window,text='',bg='BLACK',fg='BLACK')
    label2.pack()
    # print(Hashpasswords(passw_var.get().encode('utf-8')))
    
    def _getmasterpass():
        checkhashedpass = Hashpasswords(passw_var.get().encode('utf-8'))
        Cursor.execute('SELECT * FROM masterpassword WHERE id= 1 and password = ? ',[(checkhashedpass)])
        return Cursor.fetchall()

    def _checkpassword():
        # user_pass = 'fake'
        matched = _getmasterpass()
        print(matched)
        if matched:
            PasswordVault()
            # label2.config( text='',font=("Arial", 15),bg='BLACK',fg='BLACK')
        else:
            label2.config( text='wrong password!',font=("Arial", 15), bg='BLACK',fg='RED')
    
    button1 = Button(window,text='Submit',command= _checkpassword).place(x = 300,
                                                   y = 240)
    # label1.config(anchor=CENTER)
    # label1.pack()


def PasswordVault():
    for widget in window.winfo_children():
        widget.destroy()



    def _addentry():
        e1= 'username'
        e2= 'app/website'
        e3= 'password'

        username = Popup(e1)
        userapp = Popup(e2)
        password = Popup(e3)

        insert_field = '''INSERT INTO vault(username, userapp, password)
        values(?, ?, ?)
        '''
        Cursor.execute(insert_field,(username, userapp, password))
        db.commit()
        print('added ')

        PasswordVault()

    def _removeEntry(input):
        Cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        PasswordVault()



    window.geometry('650x400')
    label1 = Label(window, text= 'My Vault',font=("Arial", 15), bg='BLACK',fg='WHITE')
    label1.grid(column= 0)

    b1 = Button(window, text='Add Item', command=_addentry)
    b1.grid(column=3,pady=10)


    header1 = Label(window, text= 'Username',font=("Arial", 15), bg='BLACK',fg='WHITE')
    header1.grid(row=2,column= 0 ,padx=30)
    header2 = Label(window, text= 'App/Website',font=("Arial", 15), bg='BLACK',fg='WHITE')
    header2.grid(row=2,column= 1 ,padx=50)
    header3 = Label(window, text= 'Password',font=("Arial", 15), bg='BLACK',fg='WHITE')
    header3.grid(row=2,column= 2 ,padx=50)


    Cursor.execute('SELECT * FROM vault')
    if (Cursor.fetchall() != None) :
        i=0
        while TRUE :
            Cursor.execute('SELECT * FROM vault')
            items = Cursor.fetchall()
            print(len(items))
            if(len(items) <= 0):
                break
            print(len(items[i]))
            lbl1 = Label(window, text= items[i][1], font=('Helvetica', 12), bg='BLACK',fg='WHITE')
            lbl1.grid(column= 0, row= i+3)
            lbl2 = Label(window, text= items[i][2], font=('Helvetica', 12), bg='BLACK',fg='WHITE')
            lbl2.grid(column= 1, row= i+3)
            lbl3 = Label(window, text= items[i][3], font=('Helvetica', 12), bg='BLACK',fg='WHITE')
            lbl3.grid(column= 2, row= i+3)

            btn = Button(window, text='Delete', command= partial(_removeEntry,items[i][0]))
            btn.grid(column=3, row=i+3,pady=5)

            i=i+1
            Cursor.execute('SELECT * FROM vault')
            if i >= len(Cursor.fetchall()):
                 break

Cursor.execute('SELECT * FROM masterpassword')
if Cursor.fetchall():
    LoginScreen()
else :
    InitialScreen()
window.mainloop()