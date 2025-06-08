<h1 align="center">
WaveWhisper
</h1>

<p align="center">
<a href="https://pypi.org/project/WaveWhisper/"><img src="https://img.shields.io/pypi/dm/wavewhisper?label=PyPi%20downloads"/></a>

  
<a href="https://github.com/maxmmueller/WaveWhisper/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-blue"/></a>
</p>

<p align="center" style="font-size: 18px;">WaveWhisper is a lightweight Python library for steganographic encryption of text within the spectrogram of audio files.</p>


<p align="center">
<img src="https://raw.githubusercontent.com/maxmmueller/WaveWhisper/main/images/screenshot.png">
</p>


## Note
This project was originally created for the German competition [*Explore Science Mannheim 2022*](https://www.explore-science.info/downloads/esma2022datensicherheit.pdf) in the category *data security* where it was ranked 2nd. I then made some small changes to turn it into this open source library.

In my attempt to make this library as lightweight as possible, it can currently operate without any external dependencies.


## Installation
To access this library in Python, install the latest release from PyPi:
```
pip install wavewhisper
```

## Usage
Only capital letters of the english alphabet and spaces are supported.

#### Code example:
```python
from wavewhisper import Message

# Create a Message object with the desired text
message = Message("My secret text")

# Encrypt the message into an audio file by specifying the carrier path and output path
message.encrypt("song.wav", "encrypted.wav")
```

See the [documentation](https://github.com/maxmmueller/WaveWhisper/blob/main/docs.md) for more detailed usage instructions.


## Contributing
Contributions to this project are welcome!

If you encounter any problems, find a bug or have feature requests, please open an [issue](https://github.com/maxmmueller/wavewhisper/issues/new).


## Support
If you find this project helpful, consider supporting its development by making a donation:

<a href="https://www.buymeacoffee.com/maxmmueller" target="_blank">
  <img src="https://raw.githubusercontent.com/maxmmueller/WaveWhisper/main/images/bmac.png" alt="Buy Me A Coffee" style="width: 140px;">
</a>
