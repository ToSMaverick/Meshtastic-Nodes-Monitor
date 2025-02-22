from datetime import datetime
import time
from geopy.distance import geodesic
from config import Config

def calculate_distance(coord1, coord2=None):
    if coord2 is None:
        c = Config()
        my_lat = c.get('location.latitude', None)
        my_long = c.get('location.longitude', None)
        coord2 = (my_lat, my_long)

    if not any([coord1[0], coord1[1], coord2[0], coord2[1]]):
        return -1

    return geodesic(coord1, coord2).km

def get_datestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_seconds(seconds):
    hms = time.strftime('%H:%M:%S', time.gmtime(seconds))
    days = int(seconds / (60 * 60 * 24))
    if days > 0:
        hms = f"{days} days, {hms}"
    return hms
