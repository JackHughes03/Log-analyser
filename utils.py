import os
import re
import requests
import time

def get_response_codes(logfilepath, text_label=None, scroll_area=None, set_text_callback=None, full_report=False):

    response_code_pattern = r'(?<=\s)(\d{3})(?=\s)'
    response_code_dictionary = {}

    with open(logfilepath, 'r') as file:
        for logline in file:
            found_response_codes = re.findall(response_code_pattern, logline)

            for response_code in found_response_codes:
                if response_code in response_code_dictionary:
                    response_code_dictionary[response_code] += 1
                else:
                    response_code_dictionary[response_code] = 1

    if full_report:
        return response_code_dictionary
        
    sorted_codes = sorted(response_code_dictionary.items(), key=lambda x: x[1], reverse=True)
    processed = 0
    
    for response_code, count in sorted_codes[:30]:
        processed += 1
        color = "#ffffff"
        set_text_callback(text_label, f"{response_code} - appears {count} times.", color, scroll_area)

    remaining = len(sorted_codes) - processed
    if remaining > 0:
        set_text_callback(text_label, 
                         f"\nAnd {remaining} more response codes with fewer occurrences...", 
                         "#ffffff", 
                         scroll_area)


def get_country_and_isp(ip):
    try:
        # Add delay between requests to avoid rate limiting
        time.sleep(0.1)  # 100ms delay
        
        response = requests.get(f'http://ipinfo.io/{ip}?token=4ee37a1361c69b', timeout=5)
        
        # Check if we hit rate limit
        if response.status_code == 429:  # Too Many Requests
            return "Rate limited", "Rate limited"
            
        data = response.json()
        country = data.get('country', 'Unknown')
        isp = data.get('org', 'Unknown')
        
        return country, isp
        
    except requests.exceptions.RequestException as e:
        return "Network error", "Network error"
    except Exception as e:
        return "Unknown", "Unknown"


def get_all_ip_addresses(logfilepath, text_label=None, scroll_area=None, set_text_callback=None, full_report=False):
    ip_pattern = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    ip_dictionary = {}

    with open(logfilepath, 'r') as file:
        for line in file:
            found_ips = re.findall(ip_pattern, line)
            for ip in found_ips:
                ip_dictionary[ip] = ip_dictionary.get(ip, 0) + 1

    if full_report:
        return ip_dictionary
        
    sorted_ips = sorted(ip_dictionary.items(), key=lambda item: item[1], reverse=True)
    processed = 0
    
    for ip, count in sorted_ips[:20]:
        processed += 1
        country, isp = get_country_and_isp(ip)
        message = f"IP: {ip}, Count: {count}, Country: {country}, ISP: {isp}"

        # if count >= 800:
        #     color = "#ff0000"
        # elif count >= 300:
        #     color = "#ffcc00"
        # elif count >= 50:
        #     color = "#00ff00"
        # else:
        #     color = "#ffffff"

        color = "#ffffff"
            
        set_text_callback(text_label, message, color, scroll_area)

    remaining = len(sorted_ips) - processed
    if remaining > 0:
        set_text_callback(text_label, 
                         f"\nAnd {remaining} more IPs with fewer occurrences...", 
                         "#ffffff", 
                         scroll_area)


def get_most_requested_files(logfilepath, text_label=None, scroll_area=None, set_text_callback=None, full_report=False):
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

    if full_report:
        return file_dictionary
        
    sorted_files = sorted(file_dictionary.items(), key=lambda x: x[1], reverse=True)
    processed = 0
    
    for (file, response_code), count in sorted_files[:30]:
        processed += 1
        message = f"{file} - accessed {count} times with response code {response_code}."
        color = "#ffffff"
        set_text_callback(text_label, message, color, scroll_area)

    remaining = len(sorted_files) - processed
    if remaining > 0:
        set_text_callback(text_label, 
                         f"\nAnd {remaining} more files with fewer accesses...", 
                         "#ffffff", 
                         scroll_area)


def get_tools_used(logfilepath, text_label=None, scroll_area=None, set_text_callback=None, full_report=False):
    tools_pattern = r'(?<=\()\w+'
    tools_dictionary = {}

    with open(logfilepath, 'r') as file:
        for logline in file:
            found_tools = re.findall(tools_pattern, logline)

            for tool in found_tools:
                if tool in tools_dictionary:
                    tools_dictionary[tool] += 1
                else:
                    tools_dictionary[tool] = 1

    if full_report:
        return tools_dictionary
        
    sorted_tools = sorted(tools_dictionary.items(), key=lambda x: x[1], reverse=True)
    processed = 0
    
    for tool, count in sorted_tools[:30]:
        processed += 1
        message = f"{tool} - used {count} times."
        color = "#ffffff"
        set_text_callback(text_label, message, color, scroll_area)

    remaining = len(sorted_tools) - processed
    if remaining > 0:
        set_text_callback(text_label, 
                         f"\nAnd {remaining} more tools with fewer uses...", 
                         "#ffffff", 
                         scroll_area)
        

def get_peak_traffic_times(logfilepath, text_label=None, scroll_area=None, set_text_callback=None, full_report=False):
    """Analyze peak traffic times from log files."""
    # Pattern to match timestamp in common log format
    time_pattern = r'\[(\d{2})/\w+/\d{4}:(\d{2}):(\d{2}):\d{2}'
    time_dictionary = {}
    hourly_traffic = {}
    
    with open(logfilepath, 'r') as file:
        for logline in file:
            matches = re.findall(time_pattern, logline)
            
            for day, hour, minute in matches:
                # Create hourly key
                hour_key = f"{hour}:00"
                hourly_traffic[hour_key] = hourly_traffic.get(hour_key, 0) + 1
                
                # Create 15-minute interval key
                minute_interval = int(minute) // 15 * 15
                time_key = f"{hour}:{minute_interval:02d}"
                time_dictionary[time_key] = time_dictionary.get(time_key, 0) + 1

    if full_report:
        return {"detailed": time_dictionary, "hourly": hourly_traffic}
    
    # Sort by traffic volume
    sorted_times = sorted(time_dictionary.items(), key=lambda x: x[1], reverse=True)
    sorted_hourly = sorted(hourly_traffic.items(), key=lambda x: x[1], reverse=True)
    
    # Report peak hours
    if set_text_callback:
        set_text_callback(text_label, "\nPeak Hours (24-hour format):", "#ffffff", scroll_area)
        processed = 0
        
        for hour, count in sorted_hourly[:5]:
            processed += 1
            message = f"Hour {hour} - {count} requests"
            set_text_callback(text_label, message, "#ffffff", scroll_area)
        
        # Report peak 15-minute intervals
        set_text_callback(text_label, "\nPeak 15-minute intervals:", "#ffffff", scroll_area)
        processed = 0
        
        for time_slot, count in sorted_times[:5]:
            processed += 1
            message = f"Time {time_slot} - {count} requests"
            set_text_callback(text_label, message, "#ffffff", scroll_area)
        
        # Calculate and show busiest period
        total_requests = sum(hourly_traffic.values())
        avg_requests_per_hour = total_requests / 24
        
        set_text_callback(text_label, 
                         f"\nAverage requests per hour: {avg_requests_per_hour:.2f}", 
                         "#ffffff", 
                         scroll_area)
        
        # Identify traffic patterns
        morning_traffic = sum(count for hour, count in hourly_traffic.items() 
                            if 6 <= int(hour.split(':')[0]) <= 11)
        afternoon_traffic = sum(count for hour, count in hourly_traffic.items() 
                              if 12 <= int(hour.split(':')[0]) <= 17)
        evening_traffic = sum(count for hour, count in hourly_traffic.items() 
                            if 18 <= int(hour.split(':')[0]) <= 23)
        night_traffic = sum(count for hour, count in hourly_traffic.items() 
                          if 0 <= int(hour.split(':')[0]) <= 5)
        
        # Determine busiest period
        periods = {
            "Morning (6AM-11AM)": morning_traffic,
            "Afternoon (12PM-5PM)": afternoon_traffic,
            "Evening (6PM-11PM)": evening_traffic,
            "Night (12AM-5AM)": night_traffic
        }
        
        busiest_period = max(periods.items(), key=lambda x: x[1])
        set_text_callback(text_label, 
                         f"\nBusiest period: {busiest_period[0]} with {busiest_period[1]} requests", 
                         "#ffffff", 
                         scroll_area)
        