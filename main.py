#!/usr/bin/env python
import feedparser
import requests
import multiprocessing

base_folder = 'downloads'

podcasts = {
        'HowToDoEverything': 'feed://www.npr.org/rss/podcast.php?id=510303',
        'OnTheMedia': 'http://feeds.wnyc.org/onthemedia'
}

def downloadPodcast(name, podcast):
    index = 0
    for line in feedparser.parse(podcast)['entries']:
        print "line", line
        url = filter(lambda x: '.mp3' in x['href'], line['links'])[0]['href']
        print "url", url
        file_name = base_folder + '/' + name + '_' + str(index) + '.mp3'
        with open(file_name, 'wb') as f:
            f.write(requests.get(url).content)
        index += 1

processes = []
for podcast_name in podcasts:
    processes.append(multiprocessing.Process(target=downloadPodcast, args=(podcast_name, podcasts[podcast_name],)))

for process in processes:
    process.start()

print "Downloading all podcasts"

for process in processes:
    process.join()

print "All downloads completed"
