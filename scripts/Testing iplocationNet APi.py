import requests

def get_ip_location(ip_address):
    
    url = f"https://api.iplocation.net/?ip={ip_address}"

    try:
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()            
            return data
        else:
            return f"Error: Cant retrieve data (Status code: {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"

#### MAIN
ip_address = "111.68.97.29"
location_info = get_ip_location(ip_address)
print(location_info)