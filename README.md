# JeopardyInteractive
Play Jeopardy with friends and keep score automatically! The software is based on [howardchung/watchparty](https://github.com/howardchung/watchparty). 

## How it works / How to use it

1. Find an MP4 of an episode of Jeopardy. I use an HDHomeRun and Plex to DVR my own recordings. I also use [MCEBuddy](http://www.mcebuddy2x.com/) to remove commercials
2. The script uses [WhisperX](https://github.com/m-bain/whisperX) combined with [Jeopardy Archive](https://j-archive.com/) to match the correct clues to the time in the video
3. The modified Watchparty code pauses during the clue and gives players time to find the correct answer (not implemented yet, uses a second webpage for demo purposes)
4. Score is deduced from J! Archive and tallied up using Watchparty's chat feature (not implemented yet)

(proof of concept also uses [zolomohan/speech-recognition-in-javascript-starter](https://github.com/zolomohan/speech-recognition-in-javascript-starter))

## Demo



https://github.com/ayancey/JeopardyInteractive/assets/10055792/df3bdd8c-45dd-4485-b759-3f71ad8964b7

