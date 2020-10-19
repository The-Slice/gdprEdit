from tkinter import *
from tkinter import ttk 
import getpass
import requests
import json


# search jamf pro users
def search_user(api_url, api_auth, search_username):
    jss_users_api = api_url + '/users/name/' + search_username
    jss_users_response = requests.get(jss_users_api, auth=api_auth, headers={'Accept': 'application/json'})

    if jss_users_response.status_code == 200:
        jss_user = jss_users_response.json()
        print('User found')
        return jss_user['user']


# search jamf pro accounts
def search_account(api_url, api_auth, search_username):
    jss_account_api = api_url + '/accounts/username/' + search_username
    jss_account_response = requests.get(jss_account_api, auth=api_auth, headers={'Accept': 'application/json'})

    if jss_account_response.status_code == 200:
        jss_account = jss_account_response.json()
        print('Account found')
        return jss_account['account']


# search ldap user accounts
def search_ldap_account(api_url, api_auth, search_username):
    ldap_servers_url = api_url + '/ldapservers'
    ldap_servers_response = requests.get(ldap_servers_url, auth=api_auth, headers={'Accept': 'application/json'})

    if ldap_servers_response.status_code == 200:
        ldap_servers = ldap_servers_response.json()
        servers = ldap_servers['ldap_servers']

        ldap_results = []
        for server in servers:
            ldap_server_id = str(server['id'])
            ldap_server_search_url = api_url + '/ldapservers/id/' + ldap_server_id + '/user/' + search_username
            ldap_server_search_response = requests.get(ldap_server_search_url, auth=api_auth, headers={'Accept': 'application/json'})

            if ldap_server_search_response.status_code == 200:
                ldap_server_search_response_json = ldap_server_search_response.json()
                ldap_results.append({server['name']: ldap_server_search_response_json['ldap_users']})
                print('LDAP account found on: ' + server['name'])

        if len(ldap_results) > 0:
            return ldap_results


# get user's mobile devices
def get_mobile_devices(api_url, api_auth, devices):
    mobile_devices = []
    for device in devices:
        device_api_url = api_url + '/mobiledevices/id/' + str(device['id'])
        device_response = requests.get(device_api_url, auth=api_auth, headers={'Accept': 'application/json'})
        device_response_json = device_response.json()
        mobile_devices.append(device_response_json['mobile_device'])

    if len(mobile_devices) > 0:
        print(str(len(mobile_devices)) + ' mobile devices found')
        return mobile_devices


# get user's computers
def get_computers(api_url, api_auth, devices):
    computers = []
    for device in devices:
        device_api_url = api_url + '/computers/id/' + str(device['id'])
        device_response = requests.get(device_api_url, auth=api_auth, headers={'Accept': 'application/json'})
        device_response_json = device_response.json()
        computers.append(device_response_json['computer'])

    if len(computers) > 0:
        print(str(len(computers)) + ' computers found')
        return computers

# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)
        
        #reference to the master widget, which is the tk window
        self.master = master
        
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
    
    #Creation of init_window
    def init_window(self):

        self.s=ttk.Style()
        self.s.theme_use('aqua')
        self.master.title("GDPR Application")
        
        
        self.id1 = StringVar()
        self.id2 = StringVar()
        self.id3 = StringVar()
        self.usr = StringVar()
        self.err = StringVar()
        self.but = StringVar()
        
        self.space2 = ttk.Label(self.master)
        self.l1 = ttk.Label(self.master, text="Jamf Pro URL:")
        self.e1 = ttk.Entry(self.master, textvariable=self.id1)
        self.l2 = ttk.Label(self.master, text="Jamf Pro Username:")
        self.e2 = ttk.Entry(self.master, textvariable=self.id2)
        self.l3 = ttk.Label(self.master, text="Jamf Pro Password:")
        self.e3 = ttk.Entry(self.master, textvariable=self.id3, show="*")
        self.l4 = ttk.Label(self.master, text="Search Username:")
        self.e4 = ttk.Entry(self.master, textvariable=self.usr)
        self.space4 = ttk.Label(self.master)
        self.mess = ttk.Label(self.master, textvariable=self.err, style="BW.TLabel")
        self.space3 = ttk.Label(self.master)
        self.b1 = ttk.Button(self.master,textvariable=self.but, command=self.buttonClick)
        self.space = ttk.Label(self.master)
        self.b2 = ttk.Button(self.master,text="Exit", command=self.buttonExit)
        
        
        self.master.columnconfigure(2, weight=50)
       
        
        self.space2.grid(row=0, column=2)
        self.space2.grid(row=0, column=2)
        self.l1.grid(row=1, column=1)
        self.e1.grid(row=1, column=2)
        self.l2.grid(row=2, column=1)
        self.e2.grid(row=2, column=2)
        self.l3.grid(row=3, column=1)
        self.e3.grid(row=3, column=2)
        self.l4.grid(row=4, column=1)
        self.e4.grid(row=4, column=2)
        self.space4.grid(row=5, column=2)
        self.mess.grid(row=6, column=2)
        self.space3.grid(row=7, column=2)
        self.b1.grid(row=8, column = 2)
        self.space.grid(row=9, column=2)
        self.b2.grid(row=10, column = 2)
        
        self.but.set("Search")
    
    

    def buttonClick(self):
        self.s.configure("BW.TLabel", foreground="red")
        self.err.set("")
    
        if not self.id1.get() or not self.id2.get() or not self.id3.get() or not self.usr.get():

            self.err.set("Please fill out all text fields")
    
        else:
           
            instance = self.id1.get()
            username = self.id2.get()
            password = self.id3.get()
            

            api_url = 'https://' + instance + '/JSSResource'
            api_auth = (username, password)

            loop = True
            
            user_data = {}

            search_username = self.usr.get()

            account_result = search_account(api_url, api_auth, search_username)
            if account_result is not None:
                user_data['account'] = account_result

            ldap_result = search_ldap_account(api_url, api_auth, search_username)
            if ldap_result is not None:
                user_data['ldap'] = ldap_result

            user_result = search_user(api_url, api_auth, search_username)
            if user_result is not None:
                user_data['user'] = user_result

                mobile_devices = user_data['user']['links']['mobile_devices']
                mobile_devices_result = get_mobile_devices(api_url, api_auth, mobile_devices)
                if mobile_devices_result is not None:
                    user_data['devices'] = mobile_devices_result

                computers = user_data['user']['links']['computers']
                computers_result = get_computers(api_url, api_auth, computers)
                if computers_result is not None:
                    user_data['computers'] = computers_result

            # only write to file if data exists
            if user_data:
                file_name = search_username + '.json'
                file = open(file_name, 'w')
                file_contents = json.dumps(user_data)
                file.write(file_contents)
                file.close()
                self.s.configure("BW.TLabel", foreground="green")
                self.err.set("Succesfully saved to: " + file_name)
                self.but.set("Search Again")
                self.usr.set("")
                
            else:
                self.err.set("User not found")
                
            


    def buttonExit(self):
        quit()





def main():


   
# root window created. Here, that would be the only window, but
# you can later have windows within windows.
    root = Tk()
    bgColor = '#EBEBEB'
    root.configure(background=bgColor)
    
    root.geometry("400x275")
    
    #creation of an instance
    app = Window(root)
    
    #mainloop
    root.mainloop()

if __name__ == '__main__':
    main()
