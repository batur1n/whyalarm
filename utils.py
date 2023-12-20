"""Utils module"""
import sys
import time
import requests
import shutil

class Utils:
    """Class for various utils"""

    def get_alert_info(self, endpoint):
        """Get alert info for Kyiv area"""
        sys.stdout.write("\nSending GET request to alerts API... ")
        response = requests.get(endpoint, timeout=10)
        if response.status_code != 200:
            sys.stdout.write(f"\nGET request failed: {response.status_code}, {response.reason}")
        else:
            sys.stdout.write(f'{response.status_code} OK')
            return response.json()['states']['м. Київ']
        return None
    
    def get_map_image(self, endpoint):
        """Get map image and store it locally for later upload"""
        r = requests.get(endpoint + "?map=true", stream=True)
        if r.status_code == 200:
            with open('./map.png', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)     

    @staticmethod
    def wait(seconds, message="Waiting for updates"):
        """Display dots in stdout while waiting"""
        sys.stdout.write('\n'+message)
        for _ in range(seconds*2):
            time.sleep(.5)
            sys.stdout.write('.')
            sys.stdout.flush()
