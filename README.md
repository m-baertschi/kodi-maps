# Google Maps for Kodi

A Kodi addon to view Google Maps within Kodi.

## Features
- View Google Maps in roadmap, satellite, hybrid, and terrain modes
- Search for locations
- Default view of New York City

## Installation
1. Download the zip file from the releases page
2. In Kodi, go to Settings > Add-ons > Install from zip file
3. Navigate to the downloaded zip file and select it
4. The addon will be installed

## Configuration
You need to add your own Google Maps API key in the main.py file:

```python
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
```

To get an API key:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Maps Static API and Geocoding API
4. Create credentials (API key)
5. Restrict the API key to only these two APIs

## Usage
- Open the addon
- Select a map type to view
- Use the search option to find specific locations

## Requirements
- Kodi 21 (Omega) or higher
- Internet connection
- Google Maps API Key

## License
MIT License