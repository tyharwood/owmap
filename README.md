# Old World Mapmaker
This is an unofficial XML generator that converts 3 RGB bitmaps to a map for the game [Old World](https://en.wikipedia.org/wiki/Old_World_(video_game)) by [Mohawk Games](https://en.wikipedia.org/wiki/Mohawk_Games). I thought it was amazing the maps were all just in plain XML and wanted a lighter-weight way to make maps outside of the in-game editor, so I made this. The main use-case for this is to make a map first as a bitmap in an image editor like GIMP or Photoshop, then use this to transform your layers into XML.  

### Installation
This has been rolled into a python package and CLI application. You can install the python package for Python 3.[ ]+ with pip,

`pip install owmap`

To set up a development environment I suggest using uv. After cloning the repository sync with the all dependency groups: 

`uv sync --all-groups`

I'm not the brightest bulb, so for some reason I couldn't get `uv run pytest` to work. For some reason that uses the default python interpreter instead of your virtual environment. This does work though:

`uv run python -m pytest /tests`


### CLI Basic usage

[image](./docs/pipeline.svg)

```
owmap [-h] [--mapname MAPNAME] [--terrainmap TERRAINMAP]
             [--heightmap HEIGHTMAP] [--vegmap VEGMAP]
             [maps ...]
```

At its most basic, the cli tool can take 3 positional arguments like so: 

`owmap [heightmap] [vegmap] [terrainmap]`

Each of these maps represents a different layer of Old World's tile system. All of these maps are required to build a proper world. The tool can also be run with flags instead of positional arguments, for example:

`owmap --terrainmap docs/donut.png --heightmap docs/donut_height.png --vegmap docs/donut_veg.png --mapname docs/donut.xml`

or more succinctly:

`owmap -t docs/donut.png -e docs/donut_height.png -v docs/donut_veg.png -o docs/donut.xml`

The order doesn't matter for flags. 