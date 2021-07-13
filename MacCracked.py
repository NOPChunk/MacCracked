#!/usr/bin/env python
import re
import subprocess
import optparse
import itertools
import threading
import time
import sys


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change Its MAC address. ")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address. ")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("\n""\033[1;31;40m[-] Please specify an interface. \033[1;37;40m\n[!] Use --help for more info. "
                     "\n""\033[1;37;40m[Hint] -i wlanX -m ff:ff:ff:ff:ff:ff")
    elif not options.new_mac:
        parser.error("\n""\033[1;31;40m[-] Please specify a new MAC address. \033[1;37;40m"
                     "\n[!] Use --help for more info. ""\n""\033[1;37;40m[Hint] -i wlanX -m ff:ff:ff:ff:ff:ff")
    return options


def change_mac(interface, new_mac):

    current_mac_result = get_current_mac(options.interface)
    if not current_mac_result == options.new_mac:
        print("\033[1;33;40m[~] Current MAC => " + str(current_mac_result))
    elif current_mac_result == options.new_mac:
        print("\033[1;33;40m[~] Current MAC => Same as before ")

    print("\033[1;32;40m[~] Change MAC address for\033[1;35;40m " + interface + " \033[1;32;40m=> \033[1;37;40m"
          + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

    done = False

    def animate():
        for c in itertools.cycle(['\033[1;30;47m.', '..', '...', '....', '.....',
                                  ':', '::', ':::', '::::', 'Loaded!\n']):
            if done:
                break
            sys.stdout.write('\r' + c)
            sys.stdout.flush()
            time.sleep(0.1)

    t = threading.Thread(target=animate)
    t.start()

    time.sleep(1)
    done = True

    new_current_mac_result = get_current_mac(options.interface)
    if new_current_mac_result == options.new_mac:
        print("\033[1;32;40m[+] MAC address was successfully changed \033[1;37;40m=> " + new_current_mac_result)
    else:
        print("\033[1;31;40m[-] MAC address did not get changed. ")


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address. ")


options = get_arguments()

change_mac(options.interface, options.new_mac)
