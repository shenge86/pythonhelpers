# Notes about ffpmeg

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
