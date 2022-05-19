# Video textures

- [original paper](https://www.cc.gatech.edu/gvu/perception/projects/videotexture/)
- inspired by [VirtualVirtuoso](https://github.com/VirtualVirtuoso/VideoTextures) and [pviolette3](https://github.com/pviolette3/video-texture) repositories
- [more information about project](https://metaviz.netlify.app/post/video_textures/)
- [online version of video texture player](https://vt-player.netlify.app)
   - [code](https://github.com/hoskra/vt-player)
- this code is not yet working on Windows OS 

## Abstract overview

- input
   - input frames
   - parameters (`config.py`)
- output
   - transitions list (.txt)
   - transition matrix (.png)
   - partial transitions (.txt and .png)
      - visual aid to help set up `config.py` parameters
   - config.js 
      - gets included in index.html

## Install requirements

To install python3 dependencies, run command below.

```pip3 install -r requirements.txt```

## Video Textures player usage

Repository is a bit harder to use from user perspective. It requires to set up video frames and type config manually.

1. Place video in this project's root directory
   - only works on Linux OS with `ffmpeg` utility installed
   - video can be in many formats (mp4, avi, mpeg, etc.)
   - video name has to be valid python variable name (can't start with number, can't contain spaces)
   - keep in mind that large and long videos will take a lot of memory and programm may crash
2. Run `/generate_frames.sh VIDEO_NAME.mp4`
   - VIDEO_NAME.mp4 is just an example
   - this will generate frames in `VIDEO_NAME/`
3. Edit config.py
   - input_folder has to be "VIDEO_NAME"
   - set up other parameters now, or after seeing results
4. Run `python3 main.py`
   - outputs will be generated in 'out/' folder
5. To view the player, you have to start server of your choice
   - for example: `python3 -m http.server`
   - or `php -S localhost:8000`
   - or fo javascript server install and run Parcel, Snowpack, etc.
6. Open browser and type server location http://localhost:8000/
   - opened page should look like [this](https://vt-player.netlify.app/clock.html)

## Play already generated transitions

Previsously generated transitions are stored in `src/saved_config.js` file.

To preview already generated transitions, edit `src/config.js` file by replacing *config* object with object generated in `src/saved_config.js`.

*Variable name has to stay `config`.*

### Example previous
```js
const config = {"filename": "out/clock_2_0.999_2_0.5", "folder": "clock", "extension": "png", "from": 1, "to": 37, "slice": false};

```
### Example Edit

```js
const config = {"filename": "out/grass_7_0.999_2_0.6", "folder": "grass", "extension": "png", "from": 1, "to": 250, "slice": false};
```