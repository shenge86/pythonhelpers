# Notes about ffmpeg

I use ffmpeg frequently for basic video editing! Here are some tips for myself and for others.

## Downloading
Easiest way in Windows is to use winget

`winget install ffmpeg`

## Examples of cutting videos
Cut a video from 0 to 11 seconds and call it output.mp4

`ffmpeg -i .\12655570-720p.mp4 -ss 00:00:00 -to 00:00:11 -c copy output.mp4`

## Examples of combining videos

Create a text file listing videos called `list.txt`

file 'video1.webm' \
file 'video2.webm'

Then just do as such:

`ffmpeg -f concat -safe 0 -i list.txt -c copy output.webm`

If not the same resolution, codec and frame rate, drop the `-c copy` and ffmpeg will re-encode to normalize them.

## Example of cropping videos

This will crop the video from its original resolution to 1280x720 pixels starting at pixel coordinates (150, 100).

`ffmpeg -i .\input.mp4 -vf "crop=1280:720:150:100" cropped1.mp4`