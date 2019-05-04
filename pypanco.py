"""
Palo Alto Network toolset

documentation on github https://github.com/kevinsteves/pan-python/blob/master/doc/pan.xapi.rst
http://api-lab.paloaltonetworks.com/index.html
used https://cyruslab.net/2017/11/12/pythonworking-with-palo-alto-firewall-api-with-pan-python-module/

"""

import pan.xapi,time, sys, cmd, shlex

#xpath can be navigated on PAN OS on this path https://firewall_ip/api/
deviceconfig_system_xpath = "/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system"
 
#define the timezone, can read from a list and enumerate in dictionary
tz = {}
tz['US'] = 'US/Eastern'

class Panco(cmd.Cmd):
    """Palo Alto credential, can be modified by using an external encrypted list"""
    def _get_pan_credentials(self, hostname, username,password):
        """Get credentials"""
        cred = {}
        cred['api_username'] = username
        cred['api_password'] = password
        cred['hostname'] = hostname
        return cred

    def do_check_soft(self, arguments):
        """check_soft [hostname] [username] [password]

        Check software on [hostname]  with [username] and [password]"""
        args = shlex.split(arguments)
        if len(args) < 3:
            print ("More arguments required")
            return False
        hostname, username, password = args[:3]
        xapi = pan.xapi.PanXapi(**self._get_pan_credentials(hostname, username, password))
        print('Checking software on {hostname} with: {username} and {password}...'.format(hostname=hostname, username=username, password=password[:2]))
        try:
            xapi.op(cmd='<request><system><software><check></check></software></system></request>', cmd_xml=False)
        except pan.xapi.PanXapiError as e:
            print("{error}".format(error=e))
            return False
        if len(args) > 3:
            print(xapi.xml_result())
    
    #device configuration setting only time
    def do_set_time(timezone,ntp_primary,ntp_secondary):
        """Set time"""
        deviceconfig = """
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
        return deviceconfig
    
    def do_EOF(self, line):
        return True

                
#config = set_time(tz['US'],'10.34.21.215','10.41.21.215')
 
#shoud use try and except, if status code is error then break exit with error code.
#this is a demo hence not as good on error handling.
    #xapi = pan.xapi.PanXapi(**get_pan_credentials(sys.argv[2],sys.argv[3]))
#xapi.set(xpath=deviceconfig_system_xpath,element=config)
#time.sleep(3)
#print(xapi.status)
#time.sleep(3)
#xapi.commit(cmd="<commit></commit>",timeout=10)
#print(xapi.status)

#xapi.op(cmd='show system info', cmd_xml=True)
#print(xapi.xml_result())
#xapi.op(cmd='request restart system', cmd_xml=True)
#xapi.op(cmd='<request><system><software><check></check></software></system></request>', cmd_xml=False)
#print(xapi.xml_result())
#xapi.op(cmd='<request><system><software><download><version>9.0.0</version></download></software></system></request>', cmd_xml=False)
#print(xapi.status)

if __name__ == '__main__':
    Panco().cmdloop()