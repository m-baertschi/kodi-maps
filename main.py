# -*- coding: utf-8 -*-
# Module: Google Maps for Kodi
# License: MIT

import os
import sys
import urllib.parse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import requests
from PIL import Image
from io import BytesIO

# Get the plugin url in plugin:// notation
_URL = sys.argv[0]
# Get the plugin handle as an integer number
_HANDLE = int(sys.argv[1])
_ADDON = xbmcaddon.Addon()
_ADDON_PATH = _ADDON.getAddonInfo('path')
_RESOURCE_PATH = os.path.join(_ADDON_PATH, 'resources')

# Get settings
API_KEY = _ADDON.getSetting('api_key')
DEFAULT_LOCATION = _ADDON.getSetting('default_location')
DEFAULT_ZOOM = int(_ADDON.getSetting('default_zoom'))

# Map type settings (from enum: 0=Roadmap, 1=Satellite, 2=Hybrid, 3=Terrain)
MAP_TYPES = ['roadmap', 'satellite', 'hybrid', 'terrain']
DEFAULT_MAP_TYPE = MAP_TYPES[int(_ADDON.getSetting('default_map_type'))]


def get_url(**kwargs):
    """Create a URL for calling the plugin recursively from the given set of keyword arguments."""
    return '{0}?{1}'.format(_URL, urllib.parse.urlencode(kwargs))


def get_map_image(location, zoom=DEFAULT_ZOOM, map_type=DEFAULT_MAP_TYPE, size='800x600'):
    """Get a map image from Google Maps Static API."""
    url = 'https://maps.googleapis.com/maps/api/staticmap'
    params = {
        'center': location,
        'zoom': zoom,
        'size': size,
        'maptype': map_type,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    else:
        xbmc.log(f'Error getting map: {response.status_code} - {response.text}', xbmc.LOGERROR)
        return None


def display_map(location=DEFAULT_LOCATION, zoom=DEFAULT_ZOOM, map_type=DEFAULT_MAP_TYPE):
    """Display the map in Kodi."""
    map_data = get_map_image(location, zoom, map_type)
    if not map_data:
        xbmcgui.Dialog().notification('Error', 'Failed to retrieve map', xbmcgui.NOTIFICATION_ERROR)
        return
    
    # Save temporary image
    temp_file = os.path.join(xbmcvfs.translatePath('special://temp'), 'google_map.jpg')
    image = Image.open(BytesIO(map_data))
    image.save(temp_file)
    
    # Show the image
    xbmc.executebuiltin(f'ShowPicture({temp_file})')


def list_map_options():
    """Create the list of map options in the Kodi interface."""
    # Add various map view options
    listing = []
    
    # Default view
    list_item = xbmcgui.ListItem(label='View Default Map')
    list_item.setInfo('image', {'title': 'Default Map View'})
    url = get_url(action='view_map', location=DEFAULT_LOCATION, zoom=DEFAULT_ZOOM, map_type=DEFAULT_MAP_TYPE)
    is_folder = False
    listing.append((url, list_item, is_folder))
    
    # Different map types
    for map_type in ['roadmap', 'satellite', 'hybrid', 'terrain']:
        list_item = xbmcgui.ListItem(label=f'View {map_type.title()} Map')
        list_item.setInfo('image', {'title': f'{map_type.title()} Map View'})
        url = get_url(action='view_map', location=DEFAULT_LOCATION, zoom=DEFAULT_ZOOM, map_type=map_type)
        is_folder = False
        listing.append((url, list_item, is_folder))
    
    # Search option
    list_item = xbmcgui.ListItem(label='Search Location')
    list_item.setInfo('image', {'title': 'Search for a location'})
    url = get_url(action='search')
    is_folder = False
    listing.append((url, list_item, is_folder))
    
    # Settings option
    list_item = xbmcgui.ListItem(label='Settings')
    list_item.setInfo('image', {'title': 'Configure addon settings'})
    url = get_url(action='settings')
    is_folder = False
    listing.append((url, list_item, is_folder))
    
    # Add our listing to Kodi
    xbmcplugin.addDirectoryItems(_HANDLE, listing, len(listing))
    xbmcplugin.setContent(_HANDLE, 'images')
    xbmcplugin.endOfDirectory(_HANDLE)


def search_location():
    """Prompt user to enter a location to search for."""
    keyboard = xbmc.Keyboard('', 'Search Location')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_term = keyboard.getText()
        
        # Geocode the location using Google Geocoding API
        url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': search_term,
            'key': API_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data['status'] == 'OK':
            location = data['results'][0]['geometry']['location']
            lat_lng = f"{location['lat']},{location['lng']}"
            display_map(lat_lng)
        else:
            xbmcgui.Dialog().notification('Error', 'Location not found', xbmcgui.NOTIFICATION_ERROR)


def router(paramstring):
    """Router function that calls other functions depending on the provided parameters."""
    # Check if API key is configured
    if not API_KEY:
        xbmcgui.Dialog().ok('API Key Required', 
                           'Please enter your Google Maps API Key in the addon settings.')
        _ADDON.openSettings()
        return
        
    params = dict(urllib.parse.parse_qsl(paramstring))
    if params:
        if params['action'] == 'view_map':
            location = params.get('location', DEFAULT_LOCATION)
            zoom = int(params.get('zoom', DEFAULT_ZOOM))
            map_type = params.get('map_type', DEFAULT_MAP_TYPE)
            display_map(location, zoom, map_type)
        elif params['action'] == 'search':
            search_location()
        elif params['action'] == 'settings':
            _ADDON.openSettings()
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called without parameters, display the list of map options
        list_map_options()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it
    router(sys.argv[2][1:])