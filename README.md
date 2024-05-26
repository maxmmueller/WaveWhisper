<h1 align="center">
audio-steganography
</h1>

<p align="center">
<a href="https://github.com/maxmmueller/audio-steganography/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-blue"/></a>
</p>


<h2 align="center">!! Work in process - New version is currently undocumented !!</h2>

<p align="center">A Python library for steganographic encryption of text within the spectrogram of an audio file.</p>


<p align="center">
<img src="images/screenshot.jpg">
</p>

---
## Installation
To use this library, download the latest [release](https://github.com/maxmmueller/audio-steganography/releases/latest) (source code zip) and unzip it.

Then install the necessary python libraries `pydub` and `scipy`.

---
## Usage 

## `audio_steganography(text, audio_path, destination_path)`

- Parameters:
  - `text (str)`: the text to be encrypted
  - `audio_path (str)`: a path to a .wav audio file
  - `param destination_path (str)`: path where the modified .wav will be saved


- Returns: None
### Example:

```python
audio_steganography(text="SECRET", audio_path="song.wav", destination_path="encrypted.wav")
```

---
## Contributing
Contributions to this project are welcome!

If you encounter any problems, find a bug or have feature requests, please open an [issue](https://github.com/maxmmueller/audio-steganography/issues/new).

---
## Licence
Maximilian Müller 2023 [Apache License 2.0](LICENSE)
