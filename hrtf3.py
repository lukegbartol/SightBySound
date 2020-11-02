'''hrtf.py - spatialize a sound in azimuth on the horizontal plane

Uses the "compact" format hrtf's available from 
http://sound.media.mit.edu/resources/KEMAR/compact.tar.Z

uses sox for format conversion. I'm converting to mp3 and ogg format for use with jsonic.

Adapted from Gary Bishop Jan 2011, free for any use.
by Luke Bartol Oct 2020
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile
from scipy.signal import lfilter
from subprocess import check_call
import sys
import os
import sox

def readHRTF(name):
    '''Read the hrtf data from compact format files'''
    r = np.fromfile(open(name, 'rb'), np.dtype('>i2'), 256)
    r.shape = (128,2)
    # half the rate to 22050 and scale to 0 -> 1
    r = r.astype(float)
    # should use a better filter here, this is a box lowering the sample rate from 44100 to 22050
    r = (r[0::2,:] + r[1::2,:]) / 65536
    return r

# run as python hrtf.py infile outdir
if len(sys.argv) < 4:
    print ('usage: python3 hrtf3.py inputfile azimuth elevation')
    sys.exit(1)

inputfile = sys.argv[1]
inputname = inputfile[:-4]
az = sys.argv[2]
azimuth = int(az)

elevation = sys.argv[3]
outputdir = "output"
if not os.path.exists(outputdir):
    os.mkdir(outputdir)

# recode the sound to mono and 22050
check_call(['sox', inputfile, '-r', '22050', '-c1', '-b', '16', 'input.wav'])

# read the input
rate, mono_sound = wavfile.read(open('input.wav', 'rb'))

# remove that tmp file
os.remove('input.wav')

hrtf = readHRTF(os.path.join('compact', 'elev0', 'H0e%03da.dat' % azimuth))
# apply the filter
left = lfilter(hrtf[:,0], 1.0, mono_sound)
right = lfilter(hrtf[:,1], 1.0, mono_sound)
# combine the channels
result = np.array([left, right]).T.astype(np.int16)
# save as a wav
wavfile.write('out.wav', rate, result)

check_call(['play', 'out.wav']) 

oname = os.path.join(outputdir, inputname + "-" + 'a%d' % azimuth + 'e' + elevation)
# encode to ogg and mp3
check_call(['sox', 'out.wav', oname + '.mp3'])
# swap the left and right channels for the negative angle

os.remove('out.wav')



'''
result = result[:,(1,0)]
# save a wav
wavfile.write('out.wav', rate, result)
oname = os.path.join(outputdir, 'a%d' % -azimuth)
# encode to ogg and mp3
check_call(['sox', 'out.wav', oname + '.ogg'])
check_call(['sox', 'out.wav', oname + '.mp3'])
'''




# remove the output tmp file


