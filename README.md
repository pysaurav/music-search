# Spotify Search

## Description
Spotify Search provides a way to search details about a track or a playlist. 

This focuses on finding the availability of preview_url of a track.

This allows user to : 

* search details of a track
* search playlists
* search tracks in a playlist 


## Get Started

### Clone the repositiory
```
git clone https://gitlab.com/ting-ting/technology/mvp/utilities/spotify-search.git
```

### Switch into the repository directory
```
cd spotify-search
```

### Build the docker image
```
docker build -t spotify-search .
```

### Run the docker container
```
docker run -dit -p 5000:5000 --name spotify-search spotify-search
```

### Access the web application  [here](http://127.0.0.1:5000/)
