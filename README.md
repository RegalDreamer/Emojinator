# janky-emojification
A python script to turn any image into a series of emoji hex color codes for slack. 

## Pre-Requisites

Python 3 
Pillow package installed - `pip3 install pillow`

## Usage

To use this simply:
1. Open `Pixelify.py` and change the `inputPath` variable value to your chosen image that's saved on disk.
2. Open terminal at the root of this repo and run `python3 Pixelify.py`

It will put the slack output in the `SlackOutput.txt` and also copy the output into your clipboard for easy pasting

## How it works

1. The script takes your image, resizes it to the max value for width or height, whichever is higher while respecting the aspect ratio
2. It checks each pixel against all the hex colors in `colorList.txt` and finds the closest RGB color
3. It builds the output string one by one until finished. 

Currently it will spit out the values as `:ffffff:` format, so your emojis should be supplied like this
There's a legacy mode where the names would be supplied as `:pixel-color-ffffff:` but that was way too many characters for each pixel and would hit the max character limit real fast for a single message. 

One thing to note, from testing I could detect that a message currently has around 12k characters as the upper limit, so be wary of that when selecting larger max sizes in the script. (You can modify maxHeight or maxWidth, sometimes for tall or wide pictures you can get away with more resolution :) )
