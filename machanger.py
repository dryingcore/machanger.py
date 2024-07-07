import subprocess
import argparse
import re


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")

    subprocess.run(["ifconfig", interface, "down"])

    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])

    subprocess.run(["ifconfig", interface, "up"])

    current_mac = get_current_mac(interface)
    if current_mac == new_mac:
        print(f"[+] MAC address successfully changed to {new_mac}")
    else:
        print("[-] Failed to change MAC address. Reverting changes.")
        subprocess.run(["ifconfig", interface, "hw", "ether", current_mac])
        subprocess.run(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")
        return None


def handle_args():
    parser = argparse.ArgumentParser(description="Change MAC address of a network interface")
    parser.add_argument("-i", "--interface", type=str, required=True, help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", type=str, required=True, help="New MAC address")
    args = parser.parse_args()

    change_mac(args.interface, args.mac)


if __name__ == "__main__":
    handle_args()
