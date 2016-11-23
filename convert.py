#!/usr/bin/env python
import os
from pydub import AudioSegment
from scipy.io import wavfile
import multiprocessing

ROOT_FOLDER = 'downloads'

mp3s = [os.path.join(ROOT_FOLDER, x) for x in  os.listdir(ROOT_FOLDER) if x.endswith('.mp3')]

def convertSong(path):
    name = path.split('/')[-1].split('.')[0]
    print "Converting %s" % (name)
    song = AudioSegment.from_mp3(path)
    song.export(os.path.join(ROOT_FOLDER, name + '.wav'), format='wav')
    os.remove(path)
    print "Finished conversion of %s" % (name)

pool = multiprocessing.Pool(processes=8)
results = pool.map(convertSong, mp3s)

print "All conversions completed"
