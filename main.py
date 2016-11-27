#!/usr/bin/env python
from pydub import AudioSegment
from scipy.io import wavfile
import feedparser
import requests
import multiprocessing
import os

ROOT_FOLDER = 'downloads'

podcasts = {
        'HowToDoEverything': 'feed://www.npr.org/rss/podcast.php?id=510303',
        'OnTheMedia': 'http://feeds.wnyc.org/onthemedia'
}

def convertSong(path):
    name = path.split('/')[-1].split('.')[0]
    print "Converting %s" % (name)
    song = AudioSegment.from_mp3(path)
    song.export(os.path.join(ROOT_FOLDER, name + '.wav'), format='wav')
    os.remove(path)
    print "Finished conversion of %s" % (name)

def loadEpisodes(name):
    podcast = podcasts[name]
    def lineToURLAndPath((index, line)):
        url = filter(lambda x: '.mp3' in x['href'], line['links'])[0]['href']
        file_name = ROOT_FOLDER + '/' + name + '_' + str(index) + '.mp3'
        return (url, file_name)
    lines = feedparser.parse(podcast)['entries']
    return map(lineToURLAndPath, enumerate(lines))

episodes = [tup for sublist in map(loadEpisodes, podcasts) for tup in sublist]

episode_queue = multiprocessing.Queue(maxsize=len(episodes))
for episode in episodes:
    episode_queue.put(episode)


print "Ep queue", episode_queue

def downloadPodcast((url, file_name)):
        with open(file_name, 'wb') as f:
            f.write(requests.get(url).content)
        convertSong(file_name)

def processQueue():
    print "Processing"
    while True:
        try:
            episode = episode_queue.get(True)
            print "Got episode", episode
            downloadPodcast(episode)
        except Queue.Empty:
            print "Queue empty"
            return
    print "Processing failed"

processes = []
for i in range(20):
    p = multiprocessing.Process(target=processQueue)
    p.start()
    processes.append(p)

print "All started"

for process in processes:
    process.join()

print "All downloads completed"
