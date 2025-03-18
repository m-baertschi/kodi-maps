# Google Maps for Kodi

A Kodi addon to view Google Maps within Kodi.

## Features
- View Google Maps in roadmap, satellite, hybrid, and terrain modes
- Search for locations
- Default view of New York City

## Installation
1. Download the zip file from the [Releases page](https://github.com/m-baertschi/kodi-maps/releases/latest)
2. In Kodi, go to Settings > Add-ons > Install from zip file
3. Navigate to the downloaded zip file and select it
4. The addon will be installed

## Development
This repository uses GitHub Actions to automatically create a release zip file whenever changes are pushed to the main branch. The workflow:

1. Extracts the addon ID and version from addon.xml
2. Creates a clean zip file with the proper Kodi addon structure
3. Creates a new GitHub release with the version number
4. Attaches the zip file to the release

To update the addon:
1. Make your changes to the code
2. Update the version number using the provided script:
   ```
   python bump_version.py [major|minor|patch]
   ```
   This will automatically update the version in addon.xml and add an entry to changelog.txt
3. Push to the main branch
4. GitHub Actions will automatically create a new release with the installable zip file

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
- script.module.requests addon (should be installed by default with Kodi)

## License
MIT License