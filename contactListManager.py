"""
Basic python app for managing a list of contacs.
Allows the user to add new, edit and remove contacts, as well as import or export the list as a JSON file.

Made by David Santos - https://github.com/odavidsons/contact-list-manager-GUI
"""
#File imports
import dbconnection #File containing database class/functions
import filehandling
#Module imports
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as msg
import json
from os import getcwdb,path
from configparser import ConfigParser

class App(tk.Frame):

    contactsDataJSON = [] #Contact data is stored in a temporary list while the app is running, which is then used to export
    db = "" #database connection variable
    databaseStatus = False

    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.config(width=300,height=400)
        self.pack(expand=True)

    #Select and import a JSON file
    def importContactsJSON(self):
        if self.databaseStatus == True:
                msg.showinfo(title="Import to database",message="This will import the contacts from the selected file to the database.")
        filetypes = (('JSON files', '*.json'),('All files', '*.*'))
        filename = fd.askopenfilename(title='Open a file',initialdir=getcwdb(),filetypes=filetypes)
        try:
            file = open(filename)
            data = json.load(file)
            for contact in data:
                #If database connection is set
                if self.databaseStatus == True:
                    self.db.insertContact(contact["name"],contact["phone_number"],contact["email"],contact["address"],contact["gender"])
                    contactList.insert(tk.END,contact["name"])
                #Import to local data
                else:
                    contactList.insert(tk.END,contact["name"])
                    self.contactsDataJSON.append(contact)
            if self.filehandling.logger != '': self.filehandling.logger.info(f'Imported contacts list from ({filename})')
        except: pass

    #Export the current dictionary as a JSON file
    def exportContactsJSON(self):
        try:
            #If database connecton is set
            if self.databaseStatus == True:
                contacts = self.db.getContacts()
            else: contacts = self.contactsDataJSON
            if len(contacts) > 0:
                json_object = json.dumps(contacts, indent=4)
                filetypes = (('JSON files', '*.json'),('All files', '*.*'))
                filename = fd.asksaveasfilename(title="Save file",initialdir=getcwdb(),filetypes=filetypes)
                with open(filename, "w") as outfile:
                    outfile.write(json_object)
                msg.showinfo(title="Success",message="Your contacts were exported. ("+filename+")")
                if self.filehandling.logger != '': self.filehandling.logger.info(f'Exported contacts list to ({filename})')
            else: msg.showerror(title="Failed",message="You have no data to export!")
        except: msg.showerror(title="Error",message="There was an error while exporting your contacts")

    #Create a window with a contact form
    def addContactWindow(self):
        window = tk.Toplevel(self)
        window.title("Add a contact")
        window.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty()}')
        body = tk.Frame(window,padx=20,pady=20)
        body.grid()
        name = tk.Label(body,text="Name:",pady=5)
        name.grid(row=0,column=0)
        inputName = tk.Entry(body)
        inputName.grid(row=0,column=1)
        phone = tk.Label(body,text="Phone number:",pady=5)
        phone.grid(row=1,column=0)
        inputPhone = tk.Entry(body)
        inputPhone.grid(row=1,column=1)
        email = tk.Label(body,text="Email:",pady=5)
        email.grid(row=2,column=0)
        inputEmail = tk.Entry(body)
        inputEmail.grid(row=2,column=1)
        address = tk.Label(body,text="Address:",pady=5)
        address.grid(row=3,column=0)
        inputAddress = tk.Entry(body)
        inputAddress.grid(row=3,column=1)
        gender = tk.Label(body,text="Gender:",pady=5)
        gender.grid(row=4,column=0)
        gender_value = tk.StringVar(body,"Select a gender")
        inputGender = tk.OptionMenu(body,gender_value,"Male","Female","Other")
        inputGender.grid(row=4,column=1)
        addBtn = tk.Button(body,text="OK",command=lambda: [self.addContact(window,inputName.get(),inputPhone.get(),inputEmail.get(),inputAddress.get(),gender_value.get())])
        addBtn.grid(columnspan=2)
        self.make_dynamic(window)

    #Execute the operations for adding a new contact
    def addContact(self,window,name,phone,email,address,gender):
        if name != "":
            #If database connection is set
            if self.databaseStatus == True:
                self.db.insertContact(name,phone,email,address,gender)
                contactList.insert(tk.END,name)
            else:
                #Add a local data entry
                self.contactsDataJSON.append({"name": name, "phone_number": phone, "email": email, "address": address, "gender": gender})
                contactList.insert(tk.END,name)
            window.destroy()
        else: msg.showwarning(title="Missing field",message="Please enter at least the contact name")

    #Create a window with the contact details
    def viewContact(self):
        try:
            selected = contactList.get(contactList.curselection())
            #If database connection is set
            if self.databaseStatus == True:
                contact = self.db.getContactByName(selected)
                view_name = contact[0]["name"]
                view_phone = contact[0]["phone_number"]
                view_email = contact[0]["email"]
                view_address = contact[0]["address"]
                view_gender = contact[0]["gender"]
            else:
                #For local data
                for contact in self.contactsDataJSON:
                    if contact["name"] == selected:
                        view_name = contact["name"]
                        view_phone = contact["phone_number"]
                        view_email = contact["email"]
                        view_address = contact["address"]
                        view_gender = contact["gender"]
            #Open view window
            window = tk.Toplevel(self)
            window.title("View contact")
            window.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty()}')
            body = tk.Frame(window,padx=20,pady=20)
            body.grid()
            name = tk.Label(body,text="Name:",pady=5)
            name.grid(row=0,column=0)
            inputName = tk.Label(body,text=view_name)
            inputName.grid(row=0,column=1)
            phone = tk.Label(body,text="Phone number:",pady=5)
            phone.grid(row=1,column=0)
            inputPhone = tk.Label(body,text=view_phone)
            inputPhone.grid(row=1,column=1)
            email = tk.Label(body,text="Email:",pady=5)
            email.grid(row=2,column=0)
            inputEmail = tk.Label(body,text=view_email)
            inputEmail.grid(row=2,column=1)
            address = tk.Label(body,text="Address:",pady=5)
            address.grid(row=3,column=0)
            inputAddress = tk.Label(body,text=view_address)
            inputAddress.grid(row=3,column=1)
            gender = tk.Label(body,text="Gender:",pady=5)
            gender.grid(row=4,column=0)
            inputGender = tk.Label(body,text=view_gender)
            inputGender.grid(row=4,column=1)
            addBtn = tk.Button(body,text="Close",command=window.destroy)
            addBtn.grid(columnspan=2)
            self.make_dynamic(window)
        except: pass
            
    #Create a window with the contact edit form
    def editContactWindow(self):
        try:
            selected = contactList.get(contactList.curselection())
            selected_index = contactList.curselection()
            #If database connection is set
            if self.databaseStatus == True:
                contact = self.db.getContactByName(selected)
                edit_name = contact[0]["name"]
                edit_phone = contact[0]["phone_number"]
                edit_email = contact[0]["email"]
                edit_address = contact[0]["address"]
                edit_gender = contact[0]["gender"]
            else:
                #For local data
                for contact in self.contactsDataJSON:
                    if contact["name"] == selected:
                        edit_name = contact["name"]
                        edit_phone = contact["phone_number"]
                        edit_email = contact["email"]
                        edit_address = contact["address"]
                        edit_gender = contact["gender"]
            #Open edit window
            window = tk.Toplevel(self)
            window.title("Edit contact")
            window.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty()}')
            body = tk.Frame(window,padx=20,pady=20)
            body.grid()
            name = tk.Label(body,text="Name:",pady=5)
            name.grid(row=0,column=0)
            inputName = tk.Entry(body,text=edit_name)
            inputName.grid(row=0,column=1)
            inputName.delete(0,tk.END)
            inputName.insert(tk.END,edit_name)
            phone = tk.Label(body,text="Phone number:",pady=5)
            phone.grid(row=1,column=0)
            inputPhone = tk.Entry(body,text=edit_phone)
            inputPhone.grid(row=1,column=1)
            inputPhone.delete(0,tk.END)
            inputPhone.insert(tk.END,edit_phone)
            email = tk.Label(body,text="Email:",pady=5)
            email.grid(row=2,column=0)
            inputEmail = tk.Entry(body,text=edit_email)
            inputEmail.grid(row=2,column=1)
            inputEmail.delete(0,tk.END)
            inputEmail.insert(tk.END,edit_email)
            address = tk.Label(body,text="Address:",pady=5)
            address.grid(row=3,column=0)
            inputAddress = tk.Entry(body,text=edit_address)
            inputAddress.grid(row=3,column=1)
            inputAddress.delete(0,tk.END)
            inputAddress.insert(tk.END,edit_address)
            gender = tk.Label(body,text="Gender:",pady=5)
            gender.grid(row=4,column=0)
            gender_value = tk.StringVar(body,edit_gender)
            inputGender = tk.OptionMenu(body,gender_value,"Male","Female","Other")
            inputGender.grid(row=4,column=1)
            addBtn = tk.Button(body,text="OK",command=lambda: [self.editContact(window,selected_index,inputName.get(),inputPhone.get(),inputEmail.get(),inputAddress.get(),gender_value.get())])
            addBtn.grid(columnspan=2)
            self.make_dynamic(window)
        except: pass

    #Execute the operations for editing a contact
    def editContact(self,window,selected_index,name,phone,email,address,gender):
        try:
            old_name = contactList.get(selected_index)
            if self.databaseStatus == True:
                self.db.editContact(old_name,name,phone,email,address,gender)
                #Update the listbox entry with the new name
                contactList.delete(selected_index,selected_index)
                contactList.insert(selected_index,name)
            else:
                for contact in self.contactsDataJSON:
                    if contact["name"] == old_name:
                        contact["name"] = name
                        contact["phone_number"] = phone
                        contact["email"] = email
                        contact["address"] = address
                        contact["gender"] = gender
            msg.showinfo(title="Success",message="Contact updated")
            window.destroy()
        except: msg.showerror(title="Failed",message="There was en error updating your contact.")

    #Execute the operations for removing a contact
    def removeContact(self):
        try: 
            selected_index = contactList.curselection()
            selected = contactList.get(contactList.curselection())
            confirm = msg.askyesno(title="Remove contact",message="Do you want to remove this contact? ("+selected+")")
            if confirm == True:
                #If database connection is set
                if self.databaseStatus == True:
                    self.db.removeContact(selected)
                    contactList.delete(selected_index,selected_index)
                else:
                    #Delete the local list entry
                    for contact in self.contactsDataJSON:
                        if contact["name"] == selected:
                            self.contactsDataJSON.pop(self.contactsDataJSON.index(contact))
                    contactList.delete(selected_index,selected_index)
        except: pass

    #Create a Window for inputing the database details
    def connectDBWindow(self):
        database_details = self.filehandling.loadDatabaseConfig() #Load the server details from the configuration file
        window = tk.Toplevel(self)
        window.title("Database details")
        window.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty()}')
        body = tk.Frame(window,padx=20,pady=20)
        body.grid()
        DBhost = tk.Label(body,text="Host:",pady=5)
        DBhost.grid(row=0,column=0)
        inputDBhost = tk.Entry(body)
        inputDBhost.grid(row=0,column=1)
        inputDBhost.insert(0,database_details[0])
        DBuser = tk.Label(body,text="User:",pady=5)
        DBuser.grid(row=1,column=0)
        inputDBuser = tk.Entry(body)
        inputDBuser.grid(row=1,column=1)
        inputDBuser.insert(0,database_details[1])
        DBpassword = tk.Label(body,text="Password:",pady=5)
        DBpassword.grid(row=2,column=0)
        inputDBpassword = tk.Entry(body)
        inputDBpassword.grid(row=2,column=1)
        inputDBpassword.insert(0,database_details[2])
        DBname = tk.Label(body,text="Database name:",pady=5)
        DBname.grid(row=3,column=0)
        inputDBname = tk.Entry(body)
        inputDBname.grid(row=3,column=1)
        inputDBname.insert(0,database_details[3])
        addBtn = tk.Button(body,text="OK",command=lambda: [self.connectDB(window,inputDBhost.get(),inputDBuser.get(),inputDBpassword.get(),inputDBname.get())])
        addBtn.grid(columnspan=2)
        self.make_dynamic(window)

    #Update the contact list counter
    def contactCounter(self):
        n_contacts = contactList.size()
        contactCounter.config(text=f"Total contacts: {n_contacts}")
        self.after(1000,self.contactCounter)

    #Create a window for changing the application settings
    def settingsWindow(self):
        global_settings = self.filehandling.loadGlobalConfig()
        autoConnect = tk.StringVar()
        autoConnect.set(global_settings[0])
        keepLogs = tk.StringVar()
        keepLogs.set(global_settings[1])
        
        window = tk.Toplevel(self)
        window.title("Settings")
        window.geometry(f'+{self.winfo_rootx()}+{self.winfo_rooty()}')
        body = tk.Frame(window, padx=20,pady=20)
        body.grid()
        label1 = tk.Label(window,text="Auto connect on open:",pady=5)
        label1.grid(row=0,column=0)
        chk_autoConn = tk.Checkbutton(window,variable=autoConnect,onvalue=1,offvalue=0)
        chk_autoConn.grid(row=0,column=1)
        label2 = tk.Label(window, text="Keep logs:",pady=5)
        label2.grid(row=1,column=0)
        chk_keepLogs = tk.Checkbutton(window,variable=keepLogs,onvalue=1,offvalue=0)
        chk_keepLogs.grid(row=1,column=1)
        label3 = tk.Label(window,text="Delete saved connection details")
        label3.grid(row=2,column=0)
        delDBBtn = tk.Button(window,text="Delete", command=self.filehandling.resetDatabaseConfig)
        delDBBtn.grid(row=2,column=1)
        database_details = self.filehandling.loadDatabaseConfig()
        if database_details[0] == '': delDBBtn.config(state="disabled")
        saveBtn = tk.Button(window, text="Save", command=lambda: self.filehandling.saveGlobalConfig(window,autoConnect.get(),keepLogs.get()))
        saveBtn.grid(row=3,column=0,columnspan=2,pady=5,padx=5)
        self.make_dynamic(window)

    #Make a window's widgets dynamic when resizing
    def make_dynamic(self,window):
        col_count,row_count = window.grid_size()
        
        for i in range(row_count):
            window.grid_rowconfigure(i, weight=1)

        for i in range(col_count):
            window.grid_columnconfigure(i, weight=1)

        for child in window.children.values():
            child.grid_configure(sticky="nsew")
            self.make_dynamic(child)

    """ *---------------------------------------------------------------*
        |         Functions for config and logs file handling           |
        *---------------------------------------------------------------* """

    #Create the filehandling constructor
    def initializeFiles(self):
        self.configFile = ConfigParser()
        self.filehandling = filehandling.filehandling(self.configFile)
        if not path.exists('config.ini'):
            self.configFile['DATABASE_DETAILS'] = {'dbhost': '', 'dbuser': '', 'dbpwd': '', 'dbname': ''}
            self.configFile['GLOBAL_SETTINGS'] = {'auto_connect': 0, 'keep_logs': 0}
            with open('config.ini', 'w') as configfile:
                self.configFile.write(configfile)
        else: 
            self.configFile.read('config.ini')
            #Check if the auto connect setting is on
            auto_connect = self.configFile.get('GLOBAL_SETTINGS','auto_connect')
            if auto_connect == '1':
                database_details = self.filehandling.loadDatabaseConfig()
                #If the connection details are missing, throw a warning saying that this settings is not working properly
                if database_details[0] != '':
                    self.connectDB(tk.Frame(),database_details[0],database_details[1],database_details[2],database_details[3])
                else: msg.showwarning(title="Auto connect error",message="You have turned on 'Auto connect' in the settings, but you don't have a saved database connection!")
            #Check if the keep logs setting is on
            keep_logs = self.configFile.get('GLOBAL_SETTINGS','keep_logs')
            if keep_logs == '1':
                self.filehandling.configLog()
                #If auto_connect was on, pass the newly created logger object
                if self.db:
                    self.db.logger = self.filehandling.logger
                    print(self.db.logger)

    """ *---------------------------------------------------------------*
        |                Functions for database handling                |
        *---------------------------------------------------------------* """

    #Call dbconnection constructor and set variables
    def connectDB(self,window,dbhost,dbuser,dbpassword,dbname):
        try:
            self.db = dbconnection.dbconnection(dbhost,dbuser,dbpassword,dbname)
            self.db.logger = self.filehandling.logger #Pass the logger object to the dbconnection object
            self.filehandling.saveDatabaseConfig(dbhost,dbuser,dbpassword,dbname)
            self.databaseStatus = True
            self.setDatabaseStatus()
            msg.showinfo(title="Connected",message="Connected to database")
            window.destroy()
            self.importContactsDB()
            databaseMenu.entryconfig("Connect",state="disabled")
            databaseMenu.entryconfig("Disconnect",state="normal")
        except: msg.showerror(title="Connection failed",message="There was an error connecting to the database")

    def disconnectDB(self):
        try:
            self.db.cursor.close()
            self.db.conn.close()
            self.databaseStatus = False
            contactList.delete(0,tk.END)
            self.setDatabaseStatus()
            databaseMenu.entryconfig("Connect",state="normal")
            databaseMenu.entryconfig("Disconnect",state="disabled")
        except: msg.showerror(title="Disconnection failed",message="There was an error disconnecting the database")

    #Set the displayed stats of the database connection
    def setDatabaseStatus(self):
        if self.databaseStatus == True:
            statusLabel.config(text="Database Connected")
        else: statusLabel.config(text="Database Disconnected")

    def importContactsDB(self):
        dbContacts = self.db.getContacts()
        contactList.delete(0,tk.END)
        for contact in dbContacts:
            contactList.insert(tk.END,contact["name"])

#---------------------------- Run application ----------------------------
app = App()
menubar = tk.Menu(app)
menubar = tk.Menu(app)
contactsMenu = tk.Menu(menubar, tearoff=0)
contactsMenu.add_command(label="Import contacts",command=app.importContactsJSON)
contactsMenu.add_command(label="Export contacts",command=app.exportContactsJSON)
databaseMenu = tk.Menu(menubar, tearoff=0)
databaseMenu.add_command(label="Connect",command=app.connectDBWindow)
databaseMenu.add_command(label="Disconnect",command=app.disconnectDB,state="disabled")
menubar.add_cascade(label="Contacts", menu=contactsMenu)
menubar.add_cascade(label="Database", menu=databaseMenu)
menubar.add_command(label="Settings",command=app.settingsWindow)
menubar.add_command(label="Exit", command=app.quit)

app.master.config(menu=menubar)
app.master.title("Contact Manager")
app.master.resizable(True, True)
optionsFrame = tk.Frame(app,padx=20,pady=10,bg="#2b7287")
optionsFrame.pack()

viewBtn = tk.Button(optionsFrame,text="View",bg="teal",fg="white",highlightthickness=0,command=app.viewContact)
viewBtn.pack(side="left",padx=5)
addBtn = tk.Button(optionsFrame,text="Add",bg="teal",fg="white",highlightthickness=0,command=app.addContactWindow)
addBtn.pack(side="left",padx=5)
editBtn = tk.Button(optionsFrame,text="Edit",bg="teal",fg="white",highlightthickness=0,command=app.editContactWindow)
editBtn.pack(side="left",padx=5)
removeBtn = tk.Button(optionsFrame,text="Remove",bg="teal",fg="white",highlightthickness=0,command=app.removeContact)
removeBtn.pack(side="left",padx=5)

contactsFrame = tk.Frame(app,pady=10,bg="#b0b0b0")
contactsFrame.pack(fill="x")
contactList = tk.Listbox(contactsFrame,width=30)
contactList.pack(side="left",padx=10)
scrollbar_y = tk.Scrollbar(contactsFrame)
scrollbar_y.pack(side="left", fill="y")
contactList.config(yscrollcommand=scrollbar_y.set)
scrollbar_y.config(command = contactList.yview)

statusFrame = tk.Frame(app)
statusFrame.pack(fill="x")
contactCounter = tk.Label(statusFrame,text="Total contacts: 0",bg="#b0b0b0")
contactCounter.pack(fill="x")
statusLabel = tk.Label(statusFrame,text="Database Disconnected",fg="white",bg="#2b7287")
statusLabel.pack(fill="x")
app.contactCounter()
app.initializeFiles() #Check for the existance of a config file
app.mainloop()
