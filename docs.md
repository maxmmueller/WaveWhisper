# WaveWhisper

## Classes
### Message
Represents a message to be encrypted into an audio file.

#### Attributes
- `message_text` (str): The text of the message to be encrypted.

#### Methods
- `encrypt(carrier_audio_path: str, output_path: str)`: Encrypts the message steganographically into an audio file.
  - `carrier_audio_path` (str): File path to the carrier audio waveform (.wav) file.
  - `output_path` (str): File path used to save the original audio with the hidden message.

---
### Code example:
```python
from wavewhisper import Message

message = Message("My secret text")
message.encrypt("song.wav", "encrypted.wav")
```