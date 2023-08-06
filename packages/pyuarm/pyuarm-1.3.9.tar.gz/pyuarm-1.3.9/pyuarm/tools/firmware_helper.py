#!/usr/bin/env python
#
# This is a module that help user to manage the uArm firmware.
# Please use -h to list all parameters of this script

# This file is part of pyuarm. https://github.com/uArm-Developer/pyuarm
# (C) 2016 UFACTORY <developer@ufactory.cc>

import pyuarm
from pyuarm.tools.list_uarms import uarm_ports
import pycurl, certifi
import json
from io import BytesIO
from progressbar import ProgressBar, Percentage, FileTransferSpeed, Bar, ETA
import requests
import os, sys, platform, subprocess
from itertools import izip

from distutils.version import LooseVersion
import argparse

github_release_url = "https://api.github.com/repos/uArm-Developer/FirmwareHelper/releases/latest"


class FirmwareHelper():
    firmware_defaul_filename = 'firmware.hex'
    application_path = ""
    firmware_path = ""
    web_firmware_version = ""
    uarm_firmware_version = ""
    uarm_port = ""

    # def update_firmware_path(path):
    #     global firmware_path
    #     firmware_path = path
    #
    # def update_uarm_port(port):
    #     global uarm_port
    #     uarm_port = port
    #
    # def update_firmware_url(url):
    #     global firmware_url
    #     firmware_url = url
    #
    # def update_firmware_size(size):
    #     global firmware_size
    #     firmware_size = size

    def __init__(self):
        self.web_firmware_version = "0.0.0"
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        elif __file__:
            self.application_path = os.path.dirname(__file__)
        self.firmware_path = os.path.join(os.getcwd(), self.firmware_defaul_filename)
        self.get_uarm_port()

    def get_uarm_port(self):
        uarm_list = uarm_ports()
        if len(uarm_list) > 0:
            self.uarm_port = uarm_list[0]
        else:
            print "No uArm is connected."

    def flash_firmware(self, firmware_path='firmware.hex'):
        global conf_name, avrdude_path, description
        if platform.system() == 'Darwin':
            avrdude_path = 'avrdude'
            conf_name = 'avrdude.conf'
            description = "avrdude is required, Please try `brew install avrdude`"
        elif platform.system() == 'Windows':
            avrdude_path = os.path.join(self.application_path, 'avrdude', 'avrdude.exe')
            conf_name = 'avrdude_win.conf'
        elif platform.system() == 'Linux':
            avrdude_path = 'avrdude'
            conf_name = 'avrdude.conf'
            description = "avrdude is required, Please try `apt-get install avrdude`"

        avrdude_conf = os.path.join(self.application_path, 'avrdude', conf_name)
        port = '-P' + self.uarm_port
        cmd = [avrdude_path, '-C' + avrdude_conf, '-v', '-patmega328p', '-carduino', port, '-b115200', '-D',
               '-Uflash:w:{0}:i'.format(firmware_path)]
        print ' '.join(cmd)
        try:
            subprocess.call(cmd)
        except OSError as e:
            print description

    def get_download_url(self, release_url=github_release_url):
        url = release_url
        c = pycurl.Curl()
        data = BytesIO()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(c.URL, url)
        c.setopt(c.WRITEFUNCTION, data.write)
        c.perform()
        dict = json.loads(data.getvalue())
        firmware_url = dict['assets'][0]['browser_download_url']
        firmware_size = dict['assets'][0]['size']
        self.firmware_url = firmware_url
        self.firmware_size = firmware_size
        print ("Firmware URL: {0}".format(firmware_url))
        print ("Firmware Size: {0}".format(firmware_size))

    def download_firmware(self):
        print ("Downloading firmware.hex...")
        self.get_download_url()
        try:
            response = requests.get(self.firmware_url, stream=True)
            with open(self.firmware_path, "wb") as handle:
                widgets = ['Downloading: ', Percentage(), ' ',
                           Bar(marker='#', left='[', right=']'),
                           ' ', ETA(), ' ', FileTransferSpeed()]
                pbar = ProgressBar(widgets=widgets, maxval=self.firmware_size)
                pbar.start()
                for i, data in izip(range(self.firmware_size), response.iter_content()):
                    handle.write(data)
                    pbar.update(i)
                pbar.finish()
        except requests.exceptions.ConnectionError:
            raise NetworkError("NetWork Error, Please retry...")

    def get_latest_version(self, release_url=github_release_url):
        c = pycurl.Curl()
        data = BytesIO()
        c.setopt(pycurl.CAINFO, certifi.where())
        c.setopt(c.URL, release_url)
        c.setopt(c.WRITEFUNCTION, data.write)
        c.perform()
        dict = json.loads(data.getvalue())
        self.web_firmware_version = dict['tag_name']

    def get_uarm_version(self):
        if self.uarm_port is not None or self.uarm_port != "":
            print "Reading Firmware version from uArm..."
            try:
                uarm = pyuarm.uArm(port=self.uarm_port)
                self.uarm_firmware_version = uarm.firmware_version
                uarm.disconnect()
            except pyuarm.UnkwonFirmwareException:
                print "Unknown Firmware version."
            except pyuarm.NoUArmPortException:
                print "No uArm is connected."

    def comapre_version(self):
        self.get_latest_version()
        self.get_uarm_version()
        if LooseVersion(self.web_firmware_version) > LooseVersion(self.uarm_firmware_version):
            return True


def main():
    """


    ::

        $ python -m pyuarm.tools.firmware_helper -h

        usage: firmware_helper.py [-h] [-d] [-f [FORCE]] [-c [CHECK]]

        optional arguments:
          -h, --help            show this help message and exit
          -d, --download        download firmware into firmware.hex
          -f [FORCE], --force [FORCE]
                                without firmware path, flash default firmware.hex, if
                                not existed, download automatically, with firmware
                                path, flash the firmware, eg. -f Blink.ino.hex
          -c [CHECK], --check [CHECK]
                                remote - lateset firmware release version, local -
                                read uArm firmware version
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download", help="download firmware into firmware.hex", action="store_true")
    parser.add_argument("-f", "--force", nargs='?', const='download',
                        help="without firmware path, flash default firmware.hex, if not existed, download automatically, with firmware path, flash the firmware, eg. -f Blink.ino.hex")
    parser.add_argument("-c", "--check", nargs='?', const='local',
                        help="remote - lateset firmware release version, local - read uArm firmware version")
    args = parser.parse_args()
    helper = FirmwareHelper()
    # download
    if args.download:
        helper.download_firmware()
        sys.exit(0)
    # flash
    if args.force == "download":
        if not os.path.exists(helper.firmware_path):
            print "firmware not existed, Downloading..."
            helper.download_firmware()
        helper.flash_firmware()
        sys.exit(0)
    elif args.force is not None and args.force != "":
        if not os.path.exists(args.force):
            print args.force + " not existed."
        else:
            helper.flash_firmware(firmware_path=args.force)
            sys.exit(0)
    # check
    if args.check == "local":
        if helper.uarm_port is None or helper.uarm_port == "":
            sys.exit(0)
        helper.get_uarm_version()
        sys.exit(0)
    elif args.check == "remote":
        print "Fetching the remote version..."
        helper.get_download_url()
        helper.get_latest_version()
        print "Latest firmware release version is: {0}".format(helper.web_firmware_version)
        sys.exit(0)

    if helper.uarm_port is None or helper.uarm_port == "":
        sys.exit(0)
    # No Argument#####
    try:
        version_compare = helper.comapre_version()
        print "Latest Firmware version: {0}".format(helper.web_firmware_version)
        print "Your uArm Firmware version: {0}".format(helper.uarm_firmware_version)
        if version_compare:
            print ("Would you want to upgrade your uArm with {0}{1}".format(helper.web_firmware_version, "?"))
            user_choice = raw_input("Please Enter Y if yes. ")
            if user_choice == "Y" or user_choice == "y":
                helper.download_firmware()
                helper.flash_firmware()
            else:
                print "exit"
    except Exception:
        print "Latest Firmware version: {0} ".format(helper.web_firmware_version)
        print ("Unknown uArm Firmware version, Would you want to upgrade your uArm with {0}{1}".format(helper.web_firmware_version, "?"))
        user_choice = raw_input("Please Enter Y if yes. ")
        if user_choice == "Y" or user_choice == "y":
            helper.download_firmware()
            helper.flash_firmware()
        else:
            print "exit"


class NetworkError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


if __name__ == '__main__':
    main()
