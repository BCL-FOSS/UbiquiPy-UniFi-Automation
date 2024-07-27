from models.Utility import Utility
from models.UniFiNetAPI import UniFiNetAPI
from models.PDF import PDF
import pprint
import json
import sys
from os import system
import time

class UbiquiPy:
    def __init__(self):
        self.pdf = PDF()
        self.util_obj = Utility()
     

    def generate_pdf(self, title='', author='',output_file_name='', chapters=[]):
        chap_num = 0
        
        try:
            self.pdf.set_title(title)
            self.pdf.set_author(author)
            for chapter in chapters:
                chap_num+=1
                self.pdf.print_chapter(chap_num, chapter['name'], json.dumps(chapter))
            self.pdf.output(output_file_name)
        except Exception as e:
                print(e)
        else:
                print('PDF Report Creation Complete')
                

    def network_admin(self, hostname='', port='', username='', password=''):
        ubnt_controller = UniFiNetAPI(controller_ip=hostname, controller_port=port, username=username, password=password)
        status = ubnt_controller.authenticate()
        print(status)
        return ubnt_controller
    
    
    def email(self, email_pass='', email_recipients=[], email_sender='', body='', subject='', filename=''):
        self.util_obj.send_email(password=email_pass, recipients=email_recipients, sender=email_sender, body=body, subject=subject, file_name=filename)

    def display_menu(self, menu=None, menu_type=''):

        match menu_type:
            case 'm':

                print(
                    """
                        Welcome to UbiquiPy: UniFi CLI Administration Tool

            Manage UniFi Network, Protect & Access deployments from the command line.
                            Developed by Baugh Consulting & Lab L.L.C.
        
                    """)
            case 'n':
                print(
                    """
                            UniFi Network CLI Admin Module

        Only options 5, 6, 7, 8, 11, 33 are available for on the demo controller. 
    For full functionality, connect to your production UniFi controller with UbiquiPy. 

                    """)
      
        for k, function in menu.items():
            print(k, function.__name__)

    def done(self):
        system('clear')  # clears stdout
        print("Goodbye")
        sys.exit()

    def main(self):
         # Create a menu dictionary where the key is an integer number and the
        # value is a function name.
        functions_names = [self.network_admin, self.done]
        menu_items = dict(enumerate(functions_names, start=1))

        try:
            while True:
                system('clear')
                self.display_menu(menu=menu_items, menu_type='m')
                selection = int(input("\nPlease enter your selection number: "))  # Get function key
            
                match selection:
                    case 1:
                        system('clear')
                        print(
                            """
                                Starting the Network Administration Module...
        
                            """)
                        
                        time.sleep(0.5)   

                        host_name = str(input("\nPlease enter hostname or IP of the controller: "))

                        port = '8443'

                        user = str(input("Enter UniFi Controller admin username: "))

                        psswd = str(input("Enter UniFi Controller Admin password: "))

                        selected_value = menu_items[selection]  # Gets the function name
                        ubnt_controller = selected_value(hostname=host_name, port=port, username=user, password=psswd)  # add parentheses to call the function
                        ubnt_controller.authenticate()

                        system('clear')

                        net_functions_names = [ubnt_controller.site_dpi_data, ubnt_controller.client_dpi_data, ubnt_controller.event_data, ubnt_controller.alarm_data, 
                           ubnt_controller.controller_health_data, ubnt_controller.site_stats, ubnt_controller.sites, ubnt_controller.list_admins, 
                           ubnt_controller.udm_poweroff, ubnt_controller.udm_reboot, ubnt_controller.get_sysinfo, ubnt_controller.active_clients,
                           ubnt_controller.all_clients, ubnt_controller.device_data_basic, ubnt_controller.device_data, ubnt_controller.site_settings,
                           ubnt_controller.active_routes, ubnt_controller.firewall_rules, ubnt_controller.firewall_groups, ubnt_controller.wlans, 
                           ubnt_controller.rogue_aps, ubnt_controller.dynamic_dns_info, ubnt_controller.dynamic_dns_config, ubnt_controller.list_port_profiles,
                           ubnt_controller.rf_scan_results, ubnt_controller.radius_profiles, ubnt_controller.radius_accounts, ubnt_controller.port_forwards,
                           ubnt_controller.reports, ubnt_controller.auth_audit, ubnt_controller.mgr_clients, ubnt_controller.mgr_devices, ubnt_controller.mgr_sites, ubnt_controller.sign_out, self.main, self.done]
                        
                        net_menu_items = dict(enumerate(net_functions_names, start=1))

                        system('clear')

                        self.display_menu(menu=net_menu_items, menu_type='n')

                        net_selection = int(input("\nPlease enter your selection number: "))  # Get function key
                        
                        match net_selection:
                            
                            case 5:
                                system('clear')
                                print(
                                    """
                                            Controller Health Data
        
                                    """)
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value()  # add parentheses to call the function

                                for cell in data:
                                    pprint.pprint(cell)
                                    time.sleep(0.5)

                                time.sleep(0.5)

                                ubnt_controller.sign_out()

                            case 6:
                                system('clear')
                                print(
                                    """
                                                Sites Statistics
        
                                    """)
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value()  # add parentheses to call the function

                                for cell in data:
                                    pprint.pprint(cell)
                                    time.sleep(0.5)

                                time.sleep(0.5)

                                ubnt_controller.sign_out()

                            case 7:
                                system('clear')
                                print(
                                    """
                                                All Sites
        
                                    """)
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value()  # add parentheses to call the function

                                for cell in data:
                                    pprint.pprint(cell)
                                    time.sleep(0.5)

                                time.sleep(0.5)

                                ubnt_controller.sign_out()

                            case 8:
                                system('clear')
                                print(
                                    """
                                                All Admins
        
                                    """)
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value()  # add parentheses to call the function
                                time.sleep(0.5)

                                for cell in data:
                                    pprint.pprint(cell)
                                    time.sleep(0.5)

                                time.sleep(0.5)

                                ubnt_controller.sign_out()

                            case 11:
                                system('clear')
                                print(
                                    """
                                            System Information
        
                                    """)
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value()  # add parentheses to call the function
                                time.sleep(0.5)

                                for cell in data:
                                    pprint.pprint(cell)
                                    time.sleep(0.5)

                                time.sleep(0.5)

                                ubnt_controller.sign_out()

                            case 33:
                                system('clear')
                                print(
                                    """
                                                Site Manager
        
                                    """)
                                
                                time.sleep(0.5)   

                                name = str(input("Enter new site name: "))

                                desc = str(input("Enter new site description: "))

                                cmd = str(input("Enter command: "))
                            
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value(name=name, desc=desc, cmd=cmd)  # add parentheses to call the function

                                system('clear')

                                for cell in data:
                                    pprint.pprint(cell)
                                    time.sleep(0.5)

                                time.sleep(0.5)

                                ubnt_controller.sign_out()
                                
                            case 34:
                                system('clear')
                                net_selected_value = net_menu_items[net_selection]  # Gets the function name
                                data=net_selected_value()  # add parentheses to call the function

                            case 35:
                                system('clear')
                                self.main()
                            case 36:
                                system('clear')
                                self.done()
                            case _:
                                system('clear')
                                print('Empty input. Choose from one of the available options.')
                                system('clear')
                                self.display_menu(menu=net_menu_items, menu_type='n')
                        

                    case 2:
                        selected_value = menu_items[selection]  # Gets the function name
                        selected_value()  # add parentheses to call the function
                    case _:
                        system('clear')
                        print('Choose from one of the available options.')
                        return self.main()
                    
        except KeyboardInterrupt:
            system('clear')
            print('Operation interrupted by user. Exiting UbiquiPy. Goodbye...')
            exit()

        except ValueError as e:
            system('clear')
            print('Empty selection. Choose from one of the available options.')
            return self.main()

        except Exception as e:
            system('clear')
            print('An error has occurred: ', e)
            return self.main()
                
            

if __name__ == "__main__":
    
    ubiquipy = UbiquiPy()
    ubiquipy.main()
    
    