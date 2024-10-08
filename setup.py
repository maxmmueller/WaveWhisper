from setuptools import setup

setup(
    name='WaveWhisper',
    version='1.0.2',
    description='Steganographic encryption within audio spectrograms',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maxmmueller/wavewhisper',
    author='Maximilian Müller',
    license='Apache License 2.0',
    keywords=['audio', 'python', 'encryption', 'waveform', 'wav', 'steganography'],
    packages=['wavewhisper'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)