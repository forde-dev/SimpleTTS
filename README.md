# SimpleTTS
This is a simple Text-To-Speech that I have quickly pulled together for use on my main linux computer

# How to use
To use this program you must first have 'xsel' installed.

> ArchLinux: `sudo pacman -S xsel`

> Ubuntu: `sudo apt-get install xsel`

Then install the required imports for python,

> `sudo pip3 install -r requirements.txt`

Finally, to use it you just have to highlight text you want read to you and
run the following command.

> `python3 tts.py`

I recommend to bind that command to a key-shortcut
