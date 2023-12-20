"""Utils module"""
import sys
import time
import requests

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

    @staticmethod
    def wait(seconds, message="Waiting for updates"):
        """Display dots in stdout while waiting"""
        sys.stdout.write('\n'+message)
        for _ in range(seconds*2):
            time.sleep(.5)
            sys.stdout.write('.')
            sys.stdout.flush()
