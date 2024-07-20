import requests
import http.client
import json
import os,os.path
import pprint
import aiohttp
import asyncio


class AsyncUniFiNetwork:

    def __init__(self, controller_ip, controller_port, username, password, is_udm=False):

        self.base_url = f"https://{controller_ip}:{controller_port}"
        self.url = controller_ip
        self.port = controller_port
        self.username = username
        self.password = password
        self.token = None
        self.is_udm = is_udm
        self.auth_check = False
        self.http_session = asyncio.run(self.init_session())

    async def main(self):

        async with aiohttp.ClientSession() as session:
            async with session.get('http://python.org') as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.text()
                print("Body:", html[:15], "...")


    async def init_session(self):
        session = aiohttp.ClientSession()
        return session


    

    async def make_request(self, url='', cmd='', payload={'':''}):

        if url.strip() == '':
            print('Enter the API URL to make Restful calls against.')
            exit()
        
        if cmd.strip() == '':
            print('Enter a command to make an API call.')
            exit()

        cmds = ['g', 'p', 'e']
        if cmd not in cmds:
            print('Only select commands from given options. Try again...')
            exit()

        if len(cmd) >= 2:
            print('Command entered exceeds required length. Select a command from the given options.')
            exit()

        if not payload and self.auth_check == False:
            print('Empty payload')
            headers={'':''}

        elif payload: 
            print('Empty payload')
            headers={'Cookie':self.token} 
                
        else:
            headers={
                        'Content-Type':'application/json',
                        'Cookie':self.token
                    }

        try:

            async with self.http_session as session:
                match cmd.strip():
                    case 'g':
                        async with session.get(url=url, json=payload) as response:
                            
                           
                                print("Status:", response.status)
                               
                                return 'done'

                        
                    case 'p':
                        if self.auth_check == False:

                            async with session.post(url=url, json=payload, headers=headers) as response :
                                
                                print(await response.json())
                                print('post done')
                                
                                #pprint.pprint(await response.json())
                                    #data = response.json()
                                    #print(response.headers.get("Set-Cookie"))
                                    #header_data = response.headers.get("Set-Cookie")
                                    #unifises = str(header_data[0:41])
                                    #print(unifises)
                                    #csrf = str(header_data[69:113])
                                    #print(csrf)
                                    #session_token = csrf + unifises
                                    #print(session_token)
                                    #self.token = session_token
                                    #print(self.token)
                
                                    #print("Authentication successful!")
                                    #self.auth_check = True
                                
                                    
                
                        else:
                            async with session.post(url=url, json=payload, headers=headers) as response:
                                
                                print(await response.json())
                                print('Other post done')
                            
                                
                        
                    case 'e':
                        async with session.put(url=url, json=payload, headers=headers) as response:
                            if response.status == 200:
                                print("Status:", response.status)
                                
                                return 'done'

        except Exception as e:
            
            return(print(e))
            
        else:
            pass

    def authenticate(self):
        if self.is_udm is True:
            auth_url = f"{self.base_url}/proxy/network/api/auth/login"
        else:
            auth_url = f"{self.base_url}/api/login"

        payload = {"username": self.username, "password": self.password}

        try:
            

            asyncio.run(self.make_request(url=auth_url, cmd='p', payload=payload))
            
            if self.auth_check == True:
                print(self.token)
                
            else:
                print("Authentication failed. ")
                
        except Exception as e:
            print(e)
            
        else:
           print('End of line')
           exit()

    def sign_out(self):

        if self.is_udm is True:
            url = f"{self.base_url}/proxy/network/api/logout"
        else:
            url = f"{self.base_url}/api/logout"

        try:
            asyncio..run(self.make_request(url=url, cmd='p'))

            if self.auth_check == True:
                print(self.token)
                
            else:
                print("Authentication failed. ")
            
        except Exception as e:
            print(e)
          
        else:
            #Clean up
            print('End of line')
            exit()


    def site_dpi_data(self, app='', cat='', site='', cmd=''):

        if app.strip() == '':
            print('Enter an application to filter site dpi data by.')
            exit()
        
        if cat.strip() == '':
            print('Enter a category to filter site dpi data by.')
            exit()

        if cmd.strip() == '':
            print('Enter a command to retrieve site dpi data.')
            exit()

        cmds = ['p', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if site.strip() == '':
            print('Enter a site name to retrieve dpi stats.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/sitedpi" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/sitedpi" % site

            url = f"{self.base_url}{url_string}"
        
        try:

            payload = json.dumps({'by_app': app,
                       'by_cat': cat
                       })
             
            match cmd.strip():
                case 'p':
                    
                    response = self.make_request(url=url, cmd=cmd, payload=payload)

                case 'g':
                    response = self.make_request(url=url, cmd=cmd)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the POST request to the site dpi endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def client_dpi_data(self, app='', cat='', site='', macs=[]):

        if app.strip() == '':
            print('Enter an application to filter client dpi data by.')
            exit()
        
        if cat.strip() == '':
            print('Enter a category to filter client dpi data by.')
            exit()

        if site.strip() == '':
            print('Enter a site to retrieve client dpi data from.')
            exit()
        
        if macs:
            print('MAC list in payload.')

            payload = json.dumps({'by_app': app, 
                           'by_cat': cat,
                             'macs': macs})
        else:
            print('MAC list not in payload.')
            payload = json.dumps({'by_app': app, 
                           'by_cat': cat})
            
        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/stadpi" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/stadpi" % site

            url = f"{self.base_url}{url_string}"
            
        try:
                 
            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the POST request to the client dpi endpoint:", str(e))
            response.close()
        else:
            response.close()

    def event_data(self, site=''):

        if site.strip() == '':
            print('Enter a site to retrieve event data from.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/event" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/event" % site

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the site event data endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def alarm_data(self, site=''):

        if site.strip() == '':
            print('Enter a site to retrieve alarm data from.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/alarm" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/alarm" % site

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the site alarm data endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()


    def controller_health_data(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/stat/health"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/stat/health"

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the controller health report endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def site_stats(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/stat/sites"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/stat/sites"

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the sites statistics endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def sites(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/self/sites"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/self/sites"

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the sites endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()


    def list_admins(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/stat/admin"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/stat/admin"

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the admins list endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def udm_poweroff(self):

        
        if self.is_udm is True:

            url_string = "/proxy/network/api/system/poweroff"

            url = f"{self.base_url}{url_string}"
        else:
            print('This command does not work with self hosted controllers. Please reinitialize the object with is_udm=True and set the URL as the IP address of the UDM or hardware Cloud Gateway.')
            exit()

        payload = json.dumps({'':''})

        try:

            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the POST request to the UDM shutdown endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def udm_reboot(self):

        if self.is_udm is True:

            url_string = "/proxy/network/api/system/reboot"

            url = f"{self.base_url}{url_string}"
        else:
            print('This command does not work with self hosted controllers. Please reinitialize the object with is_udm=True and set the URL as the IP address of the UDM or hardware Cloud Gateway.')
            exit()

        payload = json.dumps({'':''})

        try:
            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            

        except Exception as e:
            print("Error occurred during the POST request to the UDM reboot endpoint:", str(e))
            response.close()

        else:
            #Clean up
            response.close()

    def get_sysinfo(self):

        if self.is_udm is True:
            url = f"{self.base_url}/proxy/network/api/s/default/stat/sysinfo"
        else:
            url = f"{self.base_url}/api/s/default/stat/sysinfo"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the GET request to the system information endpoint:", str(e))
            response.close()

        else:
            #Clean up
            response.close()

    def active_clients(self, site=''):

        if site.strip() == '':
            print('Enter a site to retrieve the active client list from.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/sta" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/sta" % site

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
           
        except Exception as e:
            print("Error occurred during the GET request to the active clients endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def all_clients(self, cmd='', site=''):

        if cmd.strip() == '':
            print('Enter a command for site client management.')
            exit()
        
        cmds = ['p', 'e', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if site.strip() == '':
            print('Enter a site for client management.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/user" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/user" % site

            url = f"{self.base_url}{url_string}"

        payload = json.dumps({'':''})

        try:

            match cmd.strip():
                case 'p':
                    response = self.make_request(url=url, cmd=cmd, payload=payload) 
                case 'e':
                    response = self.make_request(url=url, cmd=cmd, payload=payload)
                case 'g':
                    response = self.make_request(url=url, cmd=cmd, payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the request to the (all clients) endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def device_data_basic(self, site=''):

        if site.strip() == '':
            print('Enter a site for network device data retrieval.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/device-basic" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/device-basic" % site

            url = f"{self.base_url}{url_string}"

        try:
            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during the GET request to the site network device information endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def device_data(self, macs=[], site=''):

        if site.strip() == '':
            print('Enter a site for assigned network device data retrieval.')

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/device" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/device" % site

            url = f"{self.base_url}{url_string}"
            
        try:
              
            if self.is_udm is False and not macs: 
                payload = json.dumps({'macs': macs})
                    
                response = self.make_request(url=url, cmd='p', payload=payload)
            else:
                response = self.make_request(url=url, cmd='g')               

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the GET request to the detailed device data endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def site_settings(self, key='', id='', cmd='', site=''):

        if key.strip() == '':
            print('Please enter a site key')
            exit()
        
        if id.strip() == '':
            print('Please enter a site ID')
            exit()

        if cmd.strip() == '':
            print('Please enter a command')
            exit()

        cmds = ['e', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()
        
        if site.strip() == '':
            print('Please enter a site')
            exit()

        if self.is_udm is True:

            if not any ((key, id)):

                url_string = "/proxy/network/api/s/%s/rest/setting/%s/%s" % (site, key, id)
            else:

                url_string = "/proxy/network/api/s/%s/rest/setting" % site       
        else:
            if not any ((key, id)):

                url_string = "/api/s/%s/rest/setting/%s/%s" % (site, key, id)
            else:

                url_string = "/api/s/%s/rest/setting" % site 

        url = f"{self.base_url}{url_string}"

        try:

            match cmd.strip():
                case 'e':
                    payload = json.dumps({'': ''})
                    response = self.make_request(url=url, cmd=cmd, payload=payload)     
                        
                case 'g':
                    response = self.make_request(url=url, cmd=cmd)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the request to the site settings endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def active_routes(self, site=''):

        if site.strip() == '':
            print('Please enter a site')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/routing" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/routing" % site

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
            
        except Exception as e:
            print("Error occurred during GET request to active routes endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def firewall_rules(self, cmd='', site=''):

        if site.strip() == '':
            print('Enter a site')
            exit()
        
        if cmd.strip() == '':
            print('Enter a command for firewall rule management.')
            exit()
        
        cmds = ['g', 'e']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/firewallrule" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/firewallrule" % site

            url = f"{self.base_url}{url_string}"

        try:

            match cmd.strip():
                    case 'e':
                        payload = json.dumps({'': ''})
                        response = self.make_request(url=url, cmd=cmd, payload=payload)
                        
                    case 'g':
                        response = self.make_request(url=url, cmd=cmd)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()    

        except Exception as e:
            print("Error occurred during the request to the firewall rules endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def firewall_groups(self, cmd='', site=''):

        if cmd.strip() == '':
            print('Enter a command for firewall group management.')
            exit()

        cmds = ['e', 'g']
        if not cmd in cmds:
                print('Command key entered does not exist. Please choose from the available commands.')
                exit()

        if len(cmd) >= 2:
                print('Please enter only the command options provided, other inputs will not be accepted.')
                exit()
        
        if site.strip() == '':
            print('Enter a site for firewall group management')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/firewallgroup" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/firewallgroup" % site

            url = f"{self.base_url}{url_string}"

        try:

            match cmd.strip():
                case 'e':
                
                    payload = json.dumps({'': ''})

                    response = self.make_request(url=url, cmd=cmd, payload=payload)
                        
                case 'g':

                    response = self.make_request(url=url, cmd=cmd)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the request to the firewall groups endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def wlans(self, wlan_name='', psswd='', site_id='', wlan_id='', cmd='', site=''):
        
        if cmd.strip() == '':
            print('Enter a command for wlan management.')
            exit()

        cmds = ['e', 'p', 'g']
        if not cmd in cmds:
                print('Command key entered does not exist. Please choose from the available commands.')
                exit()

        if len(cmd) >= 2:
                print('Please enter only the command options provided, other inputs will not be accepted.')
                exit()

        if site.strip() == '':
            print('Enter a ite for wlan management.')
            exit()

        payload = json.dumps({
                "name": wlan_name,
                "password": psswd,
                "site_id": site_id,
                "usergroup_id": "660e8cf02260b651d2585910",
                "ap_group_ids": [
                    "660e8cf02260b651d2585914"
                ],
                "ap_group_mode": "all",
                "wpa_mode": "wpa2",
                "x_passphrase": psswd
            })

        
        try:

            if self.is_udm is True:

                match cmd.strip():

                    case 'e':

                        url_string = "/proxy/network/api/s/%s/rest/wlanconf/%s" % (site, wlan_id)

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url= url, cmd=cmd, payload=payload)

                        
                    case 'p':
                        url_string = "/proxy/network/api/s/%s/rest/wlanconfs" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url= url, cmd=cmd, payload=payload)

                    case 'g':

                        url_string = "/proxy/network/api/s/%s/rest/wlanconfs" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url= url, cmd=cmd)

            else:

                match cmd.strip():

                    case 'e':

                        url_string = "/api/s/%s/rest/wlanconf/%s" % (site, wlan_id)

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url= url, cmd=cmd, payload=payload)

                        
                    case 'p':
                        url_string = "/api/s/%s/rest/wlanconfs" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url= url, cmd=cmd, payload=payload)

                    case 'g':

                        url_string = "/api/s/%s/rest/wlanconfs" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url= url, cmd=cmd)
                

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
           

        except Exception as e:
            print("Error occurred during the request to the wlan config endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def rogue_aps(self, seen_last=0, site=''):   

        if site.strip() == '':
            print('Enter a site to initiate a rogue ap scan on.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/rogueap" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/rogueap" % site

            url = f"{self.base_url}{url_string}"

        try:

            if seen_last != 0: 
                    
                payload = json.dumps({'within': seen_last})

                response = self.make_request(url=url, cmd='p', payload=payload)

            else:

                response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
                
        except Exception as e:
            print("Error occurred during the request to the rogue APs endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def dynamic_dns_info(self, site=''):

        if site.strip() == '':
            print('Enter a site to retrieve Dynamic DNS information.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/dynamicdns" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/dynamicdns" % site

            url = f"{self.base_url}{url_string}"

        try:
            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during GET request to DynamicDNS information endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def dynamic_dns_config(self, cmd='', site=''):

        if cmd.split() == '':
            print('Enter a command for Dynamic DNS configuration management.')
            exit()

        cmds = ['e', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if site.strip() == '':
            print('Enter a site for Dynamic DNS configuration management.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/dynamicdns" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/dynamicdns" % site

            url = f"{self.base_url}{url_string}"

        try:

            match cmd.split():
                case 'e':
                    payload = json.dumps({'': ''})
                    
                    response = self.make_request(url=url, cmd=cmd, payload=payload)
                

                case 'g':
                    response = self.make_request(url=url, cmd=cmd)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the request to the Dynamic DNS configuration endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def list_port_profiles(self, site=''):

        if site.strip() == '':
            print('Enter a site name.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/portconf" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/portconf" % site

            url = f"{self.base_url}{url_string}"

        try:

            response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the GET request to port profile information endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def rf_scan_results(self, mac='', cmd='', site=''):

        if site.strip() == '':
            print('Enter a site.')
            exit()

        if mac.strip() == '':
            print('Enter an AP MAC address to start the RF Scan.')
            exit()

        if cmd.strip() == '':
            print('Select a command to start an RF Scan.')
            exit()

        cmds = ['d', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        try:

            payload = {'': ''}


            if self.is_udm is True:
                match cmd.strip():
                    case 'd':
                        url_string = "/proxy/network/api/s/%s/stat/spectrumscan/%s" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url=url, cmd='g', payload=payload)
                    case 'g':
                        url_string = "/proxy/network/api/s/%s/stat/spectrumscan/" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url=url, cmd='g')
                        
            else:
                match cmd.strip():
                    case 'd':
                        url_string = "/api/s/%s/stat/spectrumscan/%s" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url=url, cmd='g', payload=payload)
                    case 'g':
                        url_string = "/api/s/%s/stat/spectrumscan/" % site

                        url = f"{self.base_url}{url_string}"

                        response = self.make_request(url=url, cmd='g')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during GET request to rf scan results endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def radius_profiles(self, cmd='', site=''):

        if site.strip() == '':
            print('Enter a site.')
            exit()

        if cmd.strip() == '':
            print('Select a command to manage RADIUS profiles.')
            exit()

        cmds = ['e','p', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/radiusprofile" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/radiusprofile" % site

            url = f"{self.base_url}{url_string}"

        try:

            match cmd.strip():
                case 'e':
                
                    payload = json.dumps({'': ''})
                    response = self.make_request(url=url, cmd=cmd, payload=payload)
                       
                case 'p':
                    payload = json.dumps({'': ''})
                    response = self.make_request(url=url, cmd=cmd, payload=payload)
                       
                case 'g':
                    response = self.make_request(url=url, cmd=cmd)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
                        
        except Exception as e:
            print("Error occurred during request to radius profiles endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def radius_accounts(self, cmd='', site=''):

        if site.strip() == '':
            print('Enter a site.')
            exit()

        if cmd.strip() == '':
            print('Select a command to manage RADIUS accounts.')
            exit()

        cmds = ['e','p', 'g']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/account" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/account" % site

            url = f"{self.base_url}{url_string}"

        try:

            match cmd.strip():
                    case 'e':

                        payload = json.dumps({'': ''})
                        response = self.make_request(url=url, cmd=cmd, payload=payload)
                
                    case 'p':
                        payload = json.dumps({'': ''})
                        response = self.make_request(url=url, cmd=cmd, payload=payload)
                        
                    case 'g':
                        
                        response = self.make_request(url=url, cmd=cmd)
                        
            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during request to radius accounts endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def port_forwards(self, site=''):

        if site.strip() == '':
            print('Enter a site.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/rest/portforward" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/rest/portforward" % site

            url = f"{self.base_url}{url_string}"

        try:

           response = self.make_request(url=url, cmd='g')

           if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during GET request to the port forward config information endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def reports(self, interval='5', type='site', returned_data='bytes', macs=[], site='' ):

        if site.strip() == '':
            print('Enter a site.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/report/%s.%s" % (site, interval, type)

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/report/%s.%s" % (site, interval, type)

            url = f"{self.base_url}{url_string}"
       
        try:
            if not macs:
                payload = json.dumps({'macs': macs})
                response = self.make_request(url=url, cmd='p', payload=payload)

            else:

                response = self.make_request(url=url, cmd='p')

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()
                    
            
        except Exception as e:
            print("Error occurred during POST request to the reports endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()    
        
    def auth_audit(self, start='', end='', site=''):

        if site.strip() == '':
            print('Enter a site.')
            exit()

        if start.strip() == '':
            print('Enter a start time for auth audit search.')
            exit()

        if end.strip() == '':
            print('Enter an end time for auth audit search.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/%s/stat/authorization/" % site

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/%s/stat/authorization/" % site

            url = f"{self.base_url}{url_string}"

        try:

            payload = json.dumps({'start': start, 'end': end})

            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during POST request to the authorization audit endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def mgr_sites(self, name='', desc='', mac='', site_id='', cmd=''):
        try:

            if name.strip() == '':
                print('Please enter a name for the site.')
                exit()
                

            if desc.strip() == '':
                print('Please enter a description for the site.')
                exit()

            if cmd.strip() == '':
                print('Please enter a command for site management.')
                exit()

            cmds = ['g', 'a', 'u', 'm', 'd']
            if not cmd in cmds:
                print('Command key entered does not exist. Please choose from the available commands.')
                exit()

            if len(cmd) >= 2:
                print('Please enter only the command options provided, other inputs will not be accepted.')
                exit()

            if self.is_udm is True:

                url_string = "/proxy/network/api/s/default/cmd/sitemgr/"

                url = f"{self.base_url}{url_string}"
            else:
                url_string = "/api/s/default/cmd/sitemgr/" 

                url = f"{self.base_url}{url_string}"

            match cmd.strip():
                case 'g':
                    payload = json.dumps({'cmd': 'get-admins'})

                case 'a':
                    payload = json.dumps({'cmd': 'add-site',
                                        'name': name,
                                        'desc': desc})
                
                case 'u':
                    payload = json.dumps({'cmd': 'update-site',
                                      'name': name,
                                      'desc': desc})
                    
                case 'r':
                    payload = json.dumps({'cmd': 'delete-site',
                                      'name': name})
                    
                case 'm':
                    payload = json.dumps({'cmd': 'move-device',
                                      'mac': mac,
                                      'site_id': site_id})
                    
                case 'd':
                    payload = json.dumps({'cmd': 'delete-device',
                                      'mac': mac})

            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the POST request to the site manager endpoint:", str(e))
            response.close()
            exit()

        else:
            #Clean up
            response.close()

    def mgr_clients(self, mac='',site='', cmd=''):

        if mac.strip() == '':
            print('Please enter the MAC address of the client you would like to manage for this site.')
            exit()

        if site.strip() == '':
            print('Please enter a site name.')
            exit()

        if cmd.strip() == '':
            print('Please enter a command for site management.')
            exit()

        cmds = ['b', 'k', 'u', 'f', 'r']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/cmd/stamgr/"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/cmd/stamgr/" 

            url = f"{self.base_url}{url_string}"

        try:
            
            match cmd:
                case 'b':
                    payload = json.dumps({'cmd': 'block-sta',
                                      'mac': mac})
                    
                case 'k':
                    payload = json.dumps({'cmd': 'kick-sta',
                                      'mac': mac})
                    
                case 'u':
                    payload = json.dumps({'cmd': 'unblock-sta',
                                      'mac': mac})
                    
                case 'f':
                    payload = json.dumps({'cmd': 'forget-sta',
                                      'mac': mac})
                    
                case 'r':
                    payload = json.dumps({'cmd': 'unauthorize-guest',
                                      'mac': mac})
                
            
            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the POST request to the client manager endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()

    def mgr_devices(self, cmd='', mac='', port_idx='', url='', inform_url=''):

        if mac.strip() == '':
            print('Please enter the MAC address of the client you would like to manage.')
            exit()

        if cmd.strip() == '':
            print('Please enter a command for site management.')
            exit()

        cmds = ['a', 'r', 'f', 'p', 's', 'S', 'l', 'L', 'u', 'U', 'm', 'M', 'w']
        if not cmd in cmds:
            print('Command key entered does not exist. Please choose from the available commands.')
            exit()

        if len(cmd) >= 2:
            print('Please enter only the command options provided, other inputs will not be accepted.')
            exit()

        if self.is_udm is True:

            url_string = "/proxy/network/api/s/default/cmd/stamgr/"

            url = f"{self.base_url}{url_string}"
        else:
            url_string = "/api/s/default/cmd/stamgr/" 

            url = f"{self.base_url}{url_string}"

        try:
            
            match cmd:
                case 'a':
                    payload = json.dumps({'cmd': 'adopt',
                                      'mac': mac})
                    
                case 'r':
                    payload = json.dumps({'cmd': 'restart',
                                      'mac': mac})
                    
                case 'f':
                    payload = json.dumps({'cmd': 'force-provision',
                                      'mac': mac})
                    
                case 'p':
                    payload = json.dumps({'cmd': 'power-cycle',
                                      'mac': mac,
                                      'port_idx': port_idx})
                    
                case 's':
                    payload = json.dumps({'cmd': 'speedtest',
                                      'mac': mac})
                case 'S':
                    payload = json.dumps({'cmd': 'speedtest-status',
                                      'mac': mac})
                case 'l':
                    payload = json.dumps({'cmd': 'set-locate',
                                      'mac': mac})
                case 'L':
                    payload = json.dumps({'cmd': 'unset-locate',
                                      'mac': mac})
                case 'u':
                    payload = json.dumps({'cmd': 'upgrade',
                                      'mac': mac})
                case 'U':
                    if url.strip() == '':
                        print('Enter the URL for the firmware to update to.')
                    else:
                        print('Updating...')
                        payload = json.dumps({'cmd': 'upgrade-external',
                                        'mac': mac,
                                        'url': url})
                case 'm':
                    if inform_url.strip() == '':
                        print('Enter the new inform URL to migrate the device: %s to.' % mac)
                    else:
                        ('Migrating...')
                        payload = json.dumps({'cmd': 'migrate',
                                        'mac': mac,
                                        'inform_url': inform_url})
                case 'M':
                    payload = json.dumps({'cmd': 'cancel-migrate',
                                      'mac': mac})
                case 'w':
                    payload = json.dumps({'cmd': 'spectrum-scan',
                                      'mac': mac})
           
            response = self.make_request(url=url, cmd='p', payload=payload)

            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                response.close()

        except Exception as e:
            print("Error occurred during the POST request to the device manager endpoint:", str(e))
            response.close()
        else:
            #Clean up
            response.close()


if __name__ == "__main__":
    ubnt = Utility("ubntdemo.netifidash.io", "8443", "ubnt_mon", "!RyuGin45!@")
    ubnt.authenticate()
    #ubnt.get_sysinfo()
    #ubnt.alarm_data()
    #ubnt.event_data()
    #ubnt.list_admins()
    #ubnt.sites() 
    #ubnt.mgr_sites(cmd='a', name='evaboys', desc='sewersluts')   
    #ubnt.mgr_sites_test(name='MainTest', desc='4th Test Site')
    ubnt.sign_out()

        