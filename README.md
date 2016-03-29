# Rigol MSO2000 LA-Sample Downloader
This tool downloads LA-Samples from Rigol MSO2000s and stores them for further usage. 

### Supported viewers
 - Sigrok's Pulse View (https://sigrok.org/wiki/PulseView)
 - OLS (http://ols.lxtreme.nl)

### Usage
`python download.py ip filename format`

### Note
 * ***This tool is in a very early stage***
 * Python 2.7 and PyVISA 1.5+ is required (https://pyvisa.readthedocs.org/en/stable/)
 * Firmware 3.01.00.04+ is required (earlier versions have a bug that limits the VISA interface to 1400 samples)
 * The tool assumes the sample rate of analog and digital channels to be identical. If they are different the samplerate should be defined using `--sample-rate`.
