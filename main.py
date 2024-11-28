import os
import re
import requests
from utils import get_response_codes

RED = '\033[31m'
ORANGE = '\033[33m'
GREEN = '\033[32m'
RESET = '\033[97m'

def get_most_requested_files(logfilepath):
    file_pattern = r'GET\s(.*?)\sHTTP.*"\s(\d{3})'
    file_dictionary = {}

    with open(logfilepath, 'r') as file:
        for logline in file:
            found_files = re.findall(file_pattern, logline)

            for file_path, response_code in found_files:
                key = (file_path, response_code)
                if key in file_dictionary:
                    file_dictionary[key] += 1
                else:
                    file_dictionary[key] = 1

    for (file, response_code), count in file_dictionary.items():
        if count > 100:
            color = RED if count >= 800 else ORANGE if count >= 300 else GREEN
            print(color + f"{file} - accessed {count} times with response code {response_code}." + RESET)


def get_country_and_isp(ip):
    try:
        response = requests.get(f'http://ipinfo.io/{ip}?token=4ee37a1361c69b')
        data = response.json()

        country = data.get('country', 'Unknown')
        isp = data.get('org', 'Unknown')

        return country, isp
    except Exception as e:
        print("No network connection")
        exit()


def get_all_ip_addresses(logfilepath):
    ip_pattern = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    ip_dictionary = {}

    # Open the log file and search for IP addresses
    with open(logfilepath, 'r') as file:
        for line in file:
            found_ips = re.findall(ip_pattern, line)

            for ip in found_ips:
                if ip in ip_dictionary:
                    ip_dictionary[ip] += 1
                else:
                    ip_dictionary[ip] = 1

    sorted_ips = sorted(ip_dictionary.items(), key=lambda item: item[1], reverse=True)
    amountofips = 0

    # Print IP with country and ISP info
    for ip, count in sorted_ips:
        amountofips += 1
        country, isp = get_country_and_isp(ip)
        # print(f"IP: {ip}, Count: {count}, Country: {country}, ISP: {isp}")

        if count >= 800:
            print(RED + f"IP: {ip}, Count: {count}, Country: {country}, ISP: {isp}" + RESET)
        elif count >= 300:
            print(ORANGE + f"IP: {ip}, Count: {count}, Country: {country}, ISP: {isp}" + RESET)
        elif count >= 50:
            print(GREEN + f"IP: {ip}, Count: {count}, Country: {country}, ISP: {isp}" + RESET)

        if amountofips == 70:
            print("Finished. Please wait...")
            break

    return sorted_ips


def get_tools_used(logfilepath):
    tools_pattern = r'(?<=\()\w+'
    tools_dictionary = {}

    with open(logfilepath, 'r') as file:
        for logfilepath in file:
            found_tools = re.findall(tools_pattern, logfilepath)

            for tool in found_tools:
                if tool in tools_dictionary:
                    tools_dictionary[tool] += 1
                else:
                    tools_dictionary[tool] = 1

    for tool, count in tools_dictionary.items():
        color = RED if count >= 800 else ORANGE if count >= 300 else GREEN if count >= 50 else RESET
        print(color + f"{tool} - used {count} times." + RESET)


def choose_options(logfilepath):
    while True:
        print("\nChoose an option:"
              "\n1. See IP addresses found"
              "\n2. See requested assets"
              "\n3. See response codes"
              "\n4. See tools used"
              "\n5. Choose another log file"
              "\n6. Exit")

        option = input("Enter: ")

        if option == '1':
            get_all_ip_addresses(logfilepath)
        elif option == '2':
            get_most_requested_files(logfilepath)
        elif option == '3':
            get_response_codes(logfilepath)
        elif option == '4':
            get_tools_used(logfilepath)
        elif option == '5':
            get_log_file()
        elif option == '6':
            exit()
        else:
            print("Invalid option")


def read_log_file(logfilepath):
    try:
        with open(logfilepath, 'r') as file:
            choose_options(logfilepath)
    except FileNotFoundError:
        print("File not found")
        return
    except PermissionError:
        print("Permission denied")
        return
    except Exception as e:
        print("An error occurred: " + str(e))
    return


def get_log_file():
    logfiledirectory = 'LogFiles'
    for file in os.listdir(logfiledirectory):
        print(" - "+ file)

    logfilename = input("Enter: ")
    logfilepath = os.path.join(logfiledirectory, logfilename)

    print("You choose " + logfilepath)

    read_log_file(logfilepath)

if __name__ == "__main__":
    get_log_file()