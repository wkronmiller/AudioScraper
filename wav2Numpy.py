#!/usr/bin/env python
import os
import numpy
import scipy.io.wavfile
from scipy.fftpack import fft
import multiprocessing
#import matplotlib.pyplot as plt

ROOT_FOLDER = 'downloads'

wavs = mp3s = [os.path.join(ROOT_FOLDER, x) for x in  os.listdir(ROOT_FOLDER) if x.endswith('.wav')]

wav_queue = multiprocessing.Queue()
for wav in wavs:
	wav_queue.put(wav)

def loadWav(pid):
	print "Starting %d" % pid
	while True:
		try:
			path = wav_queue.get()
			print "Processing %s" % (path)
			(sample_rate, array) = scipy.io.wavfile.read(path)
			full_fft = fft(array.T[0])
			real_fft = abs(full_fft[:(len(full_fft) / 2 - 1)])
			numpy.savetxt(path + '.csv', real_fft)
			# Force delete vars (bugfix OOM)
			real_fft = full_fft = array = None
		except:
			print "Worker %d failed" % pid

NUM_WORKERS = 8
pool = multiprocessing.Pool(NUM_WORKERS)
pool.map(loadWav, list(range(NUM_WORKERS)))

#TODO: output csvs
print "Done"
