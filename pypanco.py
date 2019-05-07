"""
Palo Alto Network toolset

documentation on github https://github.com/kevinsteves/pan-python/blob/master/doc/pan.xapi.rst
http://api-lab.paloaltonetworks.com/index.html
References:
https://cyruslab.net/2017/11/12/pythonworking-with-palo-alto-firewall-api-with-pan-python-module/

"""

import pan.xapi,time, sys, cmd, shlex, re
from pandevice.base import PanDevice, pandevice
from bs4 import BeautifulSoup
import requests, urllib3
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry

class Panco(cmd.Cmd):
    """Palo Alto Network toolset"""

    prompt = '(Panco) '
    intro = "Palo Alto Network toolset, remember to setup credentails (cred [user] [pass])\n\n"
    #doc_header = 'doc_header'
    #misc_header = 'misc_header'
    #undoc_header = 'undoc_header'
    ruler = '-'

    username, password, hostname, jobid = '', '', '', ''
       
    """
    def __init__(self, *args, **kwargs):
        super(Panco, self).__init__(*args, **kwargs)
        self.username = ''
        self.password = ''
    """    

    def _get_pan_credentials(self, hostname):
        """Get credentials """
        cred = {}
        cred['api_username'] = self.username
        cred['api_password'] = self.password
        cred['hostname'] = hostname
        return cred

    def do_cred(self, arguments):
        """Setup credentials cred  [username] [password]""" 
        args = shlex.split(arguments)       
        if len(args) < 2:
            print ("More arguments required")
            return False   
        username, password = args[:2]    
        self.username = username   
        self.password = password
        print("Credentials for {username} setup".format(username = username))
        
    def do_check_soft(self, arguments):
        """check_soft [hostname]

        Check software on [hostname]"""
        args = shlex.split(arguments)
        if len(args) < 1 or not self.password or not self.username:
            print ("More arguments required  or credentials not set (cred [user] [pass])")
            return False
        hostname = args[0]
        self._set_command('<request><system><software><check></check></software></system></request>', False, hostname, 'version', False)   

    def do_download_soft(self, arguments):
        """download_soft [version] [hostname]

        Download software [version] on [hostname]"""
        args = shlex.split(arguments)
        if len(args) < 2  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        version, hostname= args[:2]
        jobid = self._set_command('<request><system><software><download><version>'+version+'</version></download></software></system></request>', 
                                        False, hostname, 'line', 'jobid ([0-9]+)')
        self.jobid, self.hostname = str(jobid.group(1)), hostname                         
    
    def do_set_time(self, arguments):
        """set_time [hostname]
        timezone='US/Eastern',ntp_primary='10.34.21.215',ntp_secondary='10.41.21.215'
        """
        args = shlex.split(arguments)
        if len(args) < 1  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        timezone, ntp_primary, ntp_secondary= 'US/Eastern','10.34.21.215', '10.41.21.215'
        hostname = args[0]
        xpath = "/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system"
        config = """
        <timezone>{}</timezone>
        <ntp-servers>
            <primary-ntp-server>
                <ntp-server-address>{}</ntp-server-address>
            </primary-ntp-server>
            <secondary-ntp-server>
                <ntp-server-address>{}</ntp-server-address>
            </secondary-ntp-server>
        </ntp-servers>
        """.format(timezone,ntp_primary,ntp_secondary)
        self._set_config(config, hostname, xpath)        
    
    #option for cmd help
    def help_set_time(self):
        print '\n'.join([ 'set_time [hostname]',
                        "timezone='US/Eastern',ntp_primary='10.34.21.215',ntp_secondary='10.41.21.215'"
                           ])

    def do_show_job(self, arguments):
        """show_job [jobid] [hostname]

        Show job [jobid] on [hostname]"""
        args = shlex.split(arguments)
        if len(args) == 0:
            jobid, hostname= self.jobid, self.hostname
        elif len(args) < 2  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        else:
            jobid, hostname = args[:2]   
        while True:
            status = self._set_command('show jobs id "'+jobid+'"', True, hostname, 'result', False)
            if status == 'OK' or len(args) == 2:
                break
            time.sleep(5)    
        self.jobid, self.hostname = jobid, hostname
        
    def do_show_system(self, arguments):
        """show_system [tag] [hostname] 

        Show system [tag] on [hostname]
        Tags: sw-version, uptime, hostname, ip-address, multi-vsys, operational-mode, devicename,
            serial, vm-uuid, vm-cpuid, vm-license, vm-mode, threat-version, wildfire-version """   
        args = shlex.split(arguments)   
        if len(args) == 1:
            hostname = args[0]
            tag = 'sw-version'
        elif len(args) < 1 or not self.password or not self.username:
            print ("More arguments required (.i.e. tag: sw-version) or credentials not set (cred [user] [pass])")
            return False
        else:
            tag, hostname= args[:2]
            
        self._set_command('show system info', True, hostname, tag, False)        

    def do_upgrade_soft(self, arguments):
        """upgrade_soft [version] [hostname]

        Upgrade software [version] using pan-python on [hostname]"""
        args = shlex.split(arguments)
        if len(args) < 2  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        version, hostname = args[:2]
        jobid = self._set_command('<request><system><software><install><version>'+version+'</version></install></software></system></request>', 
                                        False, hostname, 'line', 'jobid ([0-9]+)') 
        self.jobid, self.hostname = str(jobid.group(1)), hostname

    def do_upgrade_soft_pandevice(self, arguments):
        """upgrade_soft_pandevice [version] [hostname] [dryrun]

        Upgrade software [version] using pandevice on [hostname]
        When dryrun is 'store_true', print what would happen, but don't perform upgrades"""
        args = shlex.split(arguments)
        if len(args) < 2  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        dryrun =  'store_true'
        version, hostname = args[:2]
        device = PanDevice.create_from_device(hostname, self.username, self.password,)
        try:
            device.software.upgrade_to_version(version, dryrun)
        #.PanDeviceError, .PanURLError
        except (pandevice.errors.PanDeviceError, pandevice.errors.PanURLError) as e:
            print("{error}".format(error=e))
            return False   

    def do_set_panorama(self, arguments):
        """set_panorama [panorama] [hostname]
        Setup Panorama Servers on firewalls
        """
        args = shlex.split(arguments)
        if len(args) < 2  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        panorama, hostname= args[:2]
        xpath = "/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system"
        config = """
        <panorama-server>{}</panorama-server>
        """.format(panorama)
        self._set_config(config, hostname, xpath)

    def do_set_admin(self, arguments):
        """set_admin [hash] [hostname]
        Change admin password
        """
        args = shlex.split(arguments)
        if len(args) < 2  or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        hash, hostname= args[:2]
        xpath="/config/mgt-config/users/entry[@name='admin']"
        config = """
        <phash>{}</phash>
        """.format(hash)
        self._set_config(config, hostname, xpath)    

    def do_restart(self, arguments):
        """restart [hostname] 

        Restart [hostname]"""   
        args = shlex.split(arguments)
        
        if len(args) < 1 or not self.password or not self.username:
            print ("More arguments required (.i.e. tag: sw-version) or credentials not set (cred [user] [pass])")
            return False
        hostname= args[0]    
        self._set_command('request restart system', True, hostname, 'line', False) 

    def do_waitfor_url(self, arguments):
        """waitfor_portal [hostname] [sleep] [timeout]

        Wait [timeout] until portal on [hostname] available and verify login every [sleep]"""   
        args = shlex.split(arguments)
        
        if len(args) == 1:
            hostname = args[0]
            sleep, timeout = 3, 1
        elif len(args) <= 2 or not self.password or not self.username:
            print ("More arguments required or credentials not set (cred [user] [pass])")
            return False
        elif len(args) > 2:
            hostname, sleep, timeout = args[:3] 

        url ='https://'+hostname
        sess = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        sess.mount('http://', adapter)
        response = self._get_url(url, int(sleep), int(timeout)) # try url, sleep 3s, timeout is 1min
        if response == False:
            print("No Response from {url}".format(url=url))
        elif response.status_code == 200:   
            print("Portal {url} is up and running".format(url=url))
        else:     
            print("Response from {url} is: {response}".format(url=url, response=response.status_code ))
           

    def _get_url(self, url, sleep, timeout):
        timeout = time.time() + 60*timeout
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        #https://www.reddit.com/r/learnpython/comments/2hpgja/requests_error_max_retries_i_wish_to_wait_and_try/
        response = False
        while True:
            if time.time() > timeout:
                break
            try:
                response = requests.get(url, verify=False, auth=(self.username, self.password))  
                if response.status_code == 200:
                    return response
            except requests.exceptions:
                print("Sleeping for {sleep}s...Remaining {remained}s".format(sleep=sleep, remained=int(timeout-time.time())))
                time.sleep(sleep)
            except requests.exceptions.RequestException as e:
                #print("{error}".format(error=e))
                print("No Response: Sleeping for {sleep}s...Remaining {remained}s".format(sleep=sleep, remained=int(timeout-time.time())))
                time.sleep(sleep) 
            if  response != False:  #and response.status_code != 200:   
                print("Up but not auth, sleeping for {sleep}s...Remaining {remained}s".format(sleep=sleep, remained=int(timeout-time.time())))
                time.sleep(sleep)   
        return response    

    def _set_config(self, config, hostname, xpath):        
        xapi = pan.xapi.PanXapi(**self._get_pan_credentials(hostname))
        try:
            xapi.set(xpath=xpath,element=config)
        except pan.xapi.PanXapiError as e:
            print("{error}".format(error=e))
            return False  
        time.sleep(3)
        print(xapi.status)
        time.sleep(1)
        print("Applying config on {hostname} with user {username} and password {password}...".format(hostname=hostname, username=self.username, password=self.password[:1]))
        try:
            xapi.commit(cmd="<commit></commit>",timeout=10)
        except pan.xapi.PanXapiError as e:
            print("{error}".format(error=e))
            return False    
        print(xapi.status)    

    def _set_command(self, command, cmd_xml, hostname, tag, pattern):  
        result = False
        xapi = pan.xapi.PanXapi(**self._get_pan_credentials(hostname))
        print('Running command on {hostname} with user {username} and password {password}...'.format(hostname=hostname, username=self.username, password=self.password[:1]))
        try:
            xapi.op(cmd=command, cmd_xml=cmd_xml)
        except pan.xapi.PanXapiError as e:
            print("{error}".format(error=e))
            return False
        if xapi.status == 'success':
            soup = BeautifulSoup(xapi.xml_result(),'html.parser')
            for line in soup.find_all(tag):
                result = line.get_text()  
                print(result) 
                if pattern:
                    result= self._parso(pattern, result)                   
        return result            


    
    def _parso(self, pattern, output):
        """Example usage:
        result= self._parso('jobid ([0-9]+)','Download job enqueued with jobid 248')
        if result:
            print result.group(1)"""
        try:
            return re.search(pattern, output)
        except (TypeError, AttributeError, IndexError):
            return False
        
    def do_EOF(self, line):
        return True

    def postloop(self):
        print    

if __name__ == '__main__':
    Panco().cmdloop()