"""
Palo Alto Network toolset

documentation on github https://github.com/kevinsteves/pan-python/blob/master/doc/pan.xapi.rst
http://api-lab.paloaltonetworks.com/index.html
References:
https://cyruslab.net/2017/11/12/pythonworking-with-palo-alto-firewall-api-with-pan-python-module/

"""

import pan.xapi,time, sys, cmd, shlex
from bs4 import BeautifulSoup

#xpath can be navigated on PAN OS on this path https://firewall_ip/api/
deviceconfig_system_xpath = "/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system"

class Panco(cmd.Cmd):
    """Palo Alto Network toolset"""

    prompt = '(Panco) '
    intro = "Palo Alto Network toolset"
    #doc_header = 'doc_header'
    #misc_header = 'misc_header'
    #undoc_header = 'undoc_header'
    ruler = '-'
    password=''

    def do_set_pass(self, password):
        self.password=password

    def _get_pan_credentials(self, hostname, username):
        """Get credentials """
        cred = {}
        cred['api_username'] = username
        cred['api_password'] = self.password
        cred['hostname'] = hostname
        return cred

    def do_check_soft(self, arguments):
        """check_soft [hostname] [username]

        Check software on [hostname]  with [username]"""
        args = shlex.split(arguments)
        if len(args) < 2 or not self.password:
            print ("More arguments required")
            return False
        hostname, username = args[:2]
        self._set_command('<request><system><software><check></check></software></system></request>', False, hostname, username, 'version')   

    def do_download_soft(self, arguments):
        """download_soft [version] [hostname] [username]

        Download software [version] on [hostname] with [username]"""
        args = shlex.split(arguments)
        if len(args) < 3  or not self.password:
            print ("More arguments required")
            return False
        version, hostname, username= args[:3]
        self._set_command('<request><system><software><download><version>'+version+'</version></download></software></system></request>', False, hostname, username, 'line')
    
    def do_set_time(self, arguments):
        """set_time [hostname] [username]
        timezone='US/Eastern',ntp_primary='10.34.21.215',ntp_secondary='10.41.21.215'
        """
        args = shlex.split(arguments)
        if len(args) < 2  or not self.password:
            print ("More arguments required")
            return False
        timezone, ntp_primary, ntp_secondary= 'US/Eastern','10.34.21.215', '10.41.21.215'
        hostname, username = args[:2]
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
        self._set_config(config, hostname, username)        
    
    #option for cmd help
    def help_set_time(self):
        print '\n'.join([ 'set_time [hostname] [username]',
                        "timezone='US/Eastern',ntp_primary='10.34.21.215',ntp_secondary='10.41.21.215'"
                           ])

    def do_show_job(self, arguments):
        """show_job [jobid] [hostname] [username]

        Show job [jobid] on [hostname]  with [username]"""
        args = shlex.split(arguments)
        if len(args) < 3  or not self.password:
            print ("More arguments required")
            return False
        jobid, hostname, username = args[:3]
        self._set_command('show jobs id "'+jobid+'"', True, hostname, username, 'result')

    def do_show_system(self, arguments):
        """show_system [tag] [hostname] [username]

        Show system [tag] on [hostname]  with [username]
        Tags: sw-version, uptime, hostname, ip-address, multi-vsys, operational-mode, devicename,
            serial, vm-uuid, vm-cpuid, vm-license, vm-mode, threat-version, wildfire-version """
        args = shlex.split(arguments)
        if len(args) < 3 or not self.password:
            print ("More arguments required or password not set (set_pass password)")
            return False
        tag, hostname, username = args[:3]
        self._set_command('show system info', True, hostname, username, tag)        

    def do_upgrade_soft(self, arguments):
        """upgrade_soft [version] [hostname] [username]

        Upgrade software [version] on [hostname] with [username]"""
        args = shlex.split(arguments)
        if len(args) < 3  or not self.password:
            print ("More arguments required")
            return False
        version, hostname, username = args[:3]
        self._set_command('<request><system><software><install><version>'+version+'</version></install></software></system></request>', False, hostname, username, 'line') 

    def do_set_panorama(self, arguments):
        """set_panorama [panorama] [hostname] [username]
        Setup Panorama Servers on firewalls
        """
        args = shlex.split(arguments)
        if len(args) < 3  or not self.password:
            print ("More arguments required")
            return False
        panorama, hostname, username,= args[:3]
        config = """
        <panorama-server>{}</panorama-server>
        """.format(panorama)
        self._set_config(config, hostname, username)


    def _set_config(self, config, hostname, username):        
        xapi = pan.xapi.PanXapi(**self._get_pan_credentials(hostname, username))
        xapi.set(xpath=deviceconfig_system_xpath,element=config)
        time.sleep(3)
        print(xapi.status)
        time.sleep(1)
        print("Applying config on {hostname} with {username} and {password}...".format(hostname= hostname, username= username, password=self.password[:1]))
        xapi.commit(cmd="<commit></commit>",timeout=10)
        print(xapi.status)     

    def _set_command(self, command, cmd_xml, hostname, username, tag):  
        xapi = pan.xapi.PanXapi(**self._get_pan_credentials(hostname, username))
        print('Running command on {hostname} with {username} and {password}...'.format(hostname=hostname, username=username, password=self.password[:1]))
        try:
            xapi.op(cmd=command, cmd_xml=cmd_xml)
        except pan.xapi.PanXapiError as e:
            print("{error}".format(error=e))
            return False
        if xapi.status == 'success':
            soup = BeautifulSoup(xapi.xml_result(),'html.parser')
            for line in soup.find_all(tag):
                print(line.get_text())                           

    def do_EOF(self, line):
        return True

    def postloop(self):
        print    

if __name__ == '__main__':
    Panco().cmdloop()