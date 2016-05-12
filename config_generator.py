# -*- coding: utf-8 -*-
"""
Desription:

Warning: this script will modify ~/.kkauto.cfg

After execute this script
You need to edit ~/.account.cfg to append more account for deviecs

Athor: Can Yu
"""


import subprocess
import logging
import os.path as path
from ConfigParser import RawConfigParser

logger = logging.getLogger(__name__)

class ConfigWriter():

    def __init__(self):
        # Location of kkauto.cfg file
        # store basic device information to connect appium
        self.config_dir = path.expanduser('~/')
        self.config_file_name = '.kkauto.cfg'
        self.config_location = path.join(self.config_dir,
                                         self.config_file_name)
        self.config = RawConfigParser()
        self.requests = ['platform', 'platform.version', 'name']
        self.appium_connect = ['remote.port', 'remote.host']
        self.appium_port = 4723
        self.port_idx = 0
        self.config_start()

    def config_start(self):
        self.config_file = open(self.config_location, 'w')

    def set_local_apk(self, platform, file_path):
        self.config.add_section('kkbox')
        if platform == 'android':
            self.config.set('kkbox', 'android.app-path', file_path)
        elif platform == 'ios':
            self.config.set('kkbox', 'ios.app-path', file_path)

    def set_default_serialno(self, platform ,device_id):
        if platform == 'android':
            # [android]
            # default-serialno=<ANDROID_SERIALNO>
            if not self.config.has_section('android'):
                self.config.add_section('android')
                print 'android-default add'
                self.config.set('android', 'default-serialno', device_id)
            else:
                #self.config.remove_section('android')
                print 'section = [android] already existeds'
        elif platform == 'ios':
            # [ios]
            # default-udid=<IOS_UDID>
            if not self.config.has_section('ios'):
                self.config.add_section('ios')
                print 'ios-default add'
                self.config.set('ios', 'default-udid', device_id)
            else:
                #self.config.remove_section('ios')
                print 'section = [ios] already existed'
        elif platform == 'device':
            # [device]
            # default-serialno=<ANDROID_SERIALNO>
            if not self.config.has_section('device'):
                self.config.add_section('device')
                print 'android-default add'
                self.config.set('device', 'default-serialno', device_id)
            else:
                #self.config.remove_section('device')
                print 'section = [device] already existed'

    def set_default_udid(self, udid):
        device_sect = self.id_format(udid)
        if not self.config.has_section(udid):
            self.config.add_section(device_sect)

    def get_devices_id(self):
        "Return andoid devices id with list"
        command = 'adb devices'
        ids = subprocess.check_output(command, shell=True)
        ids = ids.strip('\n').replace('\tdevice',"").split('\n')
        ids.pop(0)
        return ids

    def get_property(self, device_id, prop):
        """ Get device property by device_id
    ​
        Properties Example:
        [net.bt.name]: [Android]
        [ro.product.brand]: [Android]
        [dhcp.wlan0.gateway]: [192.168.0.1]
        [ro.build.version.release]: [5.0.2]
        [ro.build.version.sdk]: [21]
        [ro.product.brand]: [InFocus]
        [ro.product.model]: [InFocus M810]
        [ro.product.manufacturer]: [InFocus]
        """
        property_dic = {'platform.version': 'ro.build.version.release',
                        'platform': 'net.bt.name',
                        'name': 'ro.product.model'}

        command = 'adb -s ' + device_id + ' shell getprop ' + property_dic[prop]
        #print 'command: ', command
        result = subprocess.check_output(command, shell=True).strip('\n').strip('\r')
        #print 'value: ', result
        return result

    def id_format(self, device_id):
        return 'device-%s' % device_id

    def _option_process(self, device_id, option_list):
        device_sect = self.id_format(device_id)
        if not self.config.has_section(device_sect):
            self.config.add_section(device_sect)
            for option in option_list:
                self.config.set(device_sect, option, self.get_property(device_id, option))
        else:
            print 'section = [%s] already existed' % device_sect
            #self.config.remove_section(device_sect)

    def set_device_config_ios(self, device_id='<IOS_UDID>'):
        self._option_process(device_id, self.requests)

    def set_device_config(self, device_id=''):
        self._option_process(device_id, self.requests)

    def set_appium_config(self, device_id):
        device_sect = self.id_format(device_id)
        if not self.config.has_section(device_sect):
            self.config.add_section(device_sect)
        self.config.set(device_sect, self.appium_connect[0], self.appium_port + self.port_idx)
        self.port_idx += 2

    def _set_status(self, device_id, status):
        device_sect = self.id_format(device_id)
        self.config.set(device_sect, 'status', status)

    def set_device_available(self, device_id):
        self._set_status(device_id, 'available')

    def set_device_busy(self, device_id):
        self._set_status(device_id, 'busy')

    def config_close(self):
        self.config.write(self.config_file)
        self.config_file.close()
        # remove swp in vim
        command = 'rm ' + '~/.kkauto.cfg.swp'
        if path.exists(path.join(self.config_location, '.swp')):
            subprocess.check_output(command, shell=True)

    def get_sections(self):
        return self.config.sections()

    def get_options(self, section):
        return self.config.options(section)

    def get_option(self, section, option):
        return self.config.get(section, option)

    def get_port(self, section):
        return self.get_option(section, 'remote.port')

    def remove_all_sections(self):
        for section in self.get_sections():
            self.config.remove_section(section)

    def set_account_config(self, device_id, product, information, value):
        device_sect = self.id_format(device_id)
        opt = "%s_%s" % (product, information)
        self.config.set(device_sect, opt, value)

class AccountWriter():

    def __init__(self):
        # Location of account.cfg file
        # Store account information
        self.account_dir = path.expanduser('~/')
        self.account_file_name = '.account.cfg'
        self.account_config_location = path.join(self.account_dir,
                                                 self.account_file_name)
        self.account_config = RawConfigParser()
        if path.exists(self.account_config_location):
            self.account_config.read(self.account_config_location)


    def set_example(self):
        if not path.exists(self.account_config_location):
            self.account_config_file = open(self.account_config_location, 'w+')
            self.account_config.add_section('product-account-0')
            self.account_config.set('product-account-0', ";= This is a example", "")
            self.account_config.set('product-account-0', 'account', 'account')
            self.account_config.set('product-account-0', 'password', 'password')
            self.account_config.write(self.account_config_file)
            self.account_config_file.close()
            assert False, "No Accouts information file.\n" + \
                          "Example of configuration added\n" + \
                          "Please add account to this file: %s\n" % \
                          self.account_config_location + \
                          "You can add more account for KKBOX like this: \n[KKBOX-account-1]\n" + \
                          "account = account@kkbox.com\n" + \
                          "password = password"
        else:
            print "sample existed in Account file"

    def get_account_sections(self):
        if len(self.account_config.sections()) <= 1:
            self.set_example()
            return 0 # for no account config
        else:
            result = self.account_config.sections()
            result.pop(0) # remove example
            return result

    def get_account_option(self, section, option):
        return self.account_config.get(section, option)

class AppiumControler():

    def __init__(self):
        self.port = 4723
        self.bootstrap_port = self.port + 1
        self.command = 'appium --command-timeout 9999 \
                               --session-override \
                               --port %d  \
                               --bootstrap %d' % (self.port, self.bootstrap_port)

if __name__ == '__main__':
    c = ConfigWriter()
    a = AccountWriter()
    appium = AppiumControler()
    idx = 0

    accounts = a.get_account_sections()
    device_ids = c.get_devices_id()


    if len(device_ids) == 0:
        c.remove_all_sections()
        assert False, "No devices existed. Please plugin devices"
    elif len(device_ids) > len(accounts):
        assert False, "Not enought account for devices"
    else:
        c.remove_all_sections()

        # For robot framework default variable
        c.set_default_serialno('ios', '<uuid>')
        c.set_default_serialno('android', device_ids[0])
        print 'Set android default-serialno with %s' % device_ids[0]

        # Add config to device
        for device in device_ids:
            c.set_device_config(device)
            c.set_appium_config(device)
            uid =  a.get_account_option(accounts[idx], 'account')
            pwd =  a.get_account_option(accounts[idx], 'password')
            c.set_account_config(device, 'kkbox', 'account', uid)
            c.set_account_config(device, 'kkbox', 'password', pwd)
            idx += 1

    # Writing and saving to kkauto.cfg
    c.config_close()

    # Read kkauto.cfg to get device option
    all_devices = c.get_sections()[2:]
    print 'You got %d devices' % len(all_devices)
    print 'device list:', all_devices

    #for device in all_devices:
    #    print c.get_options(device)
    #    print c.get_port(device)

# No devices + No account
# One devices with No account
#
