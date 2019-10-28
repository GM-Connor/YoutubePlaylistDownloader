# Core imports
import os
import shutil
import time
import datetime

# Import pytube
try:
	from pytube import YouTube
	from pytube import Playlist
except ImportError:
	print ('Failed to import pytube. Install with "pip install pytube"')
	raise


# Akagami main channel
# https://www.youtube.com/playlist?list=UUEIMvzf3R9d3_2A3IAajvHg

# Akagami food channel
# https://www.youtube.com/playlist?list=UUhFqyZDekCMt_z7sVO3JjBQ

# michael ilectureonline
# https://www.youtube.com/playlist?list=UUiGxYawhEp4QyFcX0R60YdQ


# Constants
FAILURE = 25


# Funtions

# Get video
def get_video(video_url):
	fails = 0
	while True:
		try:
			return YouTube(video_url)
		except:
			fails = fails + 1
			print ('Failed attempt ' + str(fails) + '/' + str(FAILURE))

			if fails == FAILURE:
				raise

# Select a stream
def get_stream(yt):
	# Preferences
	pref1 = yt.streams.filter(progressive=True, mime_type='video/webm', res='360p').first()
	pref2 = yt.streams.filter(progressive=True, mime_type='video/webm', res='480p').first()
	pref3 = yt.streams.filter(progressive=True, mime_type='video/webm', res='720p').first()
	pref4 = yt.streams.filter(progressive=True, res='360p').first()
	pref5 = yt.streams.filter(progressive=True, res='480p').first()
	pref6 = yt.streams.filter(progressive=True, res='720p').first()
	pref7 = yt.streams.filter(progressive=True).first()
	pref8 = yt.streams.filter().first()

	if pref1:
		return pref1
	if pref2:
		return pref2
	if pref3:
		return pref3
	if pref4:
		return pref4
	if pref5:
		return pref5
	if pref6:
		return pref6
	if pref7:
		return pref7
	if pref8:
		return pref8

	print('No available stream')
	return false

# Download video
def download_video(stream):
	fails = 0
	while True:
		try:
			return stream.download(tmpdownloads_dir)
		except:
			fails = fails + 1
			print ('Failed attempt ' + str(fails) + '/' + str(FAILURE))

			if fails == FAILURE:
				raise


# Script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Downloads directory
downloads_dir = script_dir + '/downloads'

# Downloads directory
tmpdownloads_dir = downloads_dir + '/tmp'

# Data directory
data_dir = script_dir + '/data'

# Blacklist file
blacklist_file = data_dir + '/blacklist'


# Create Downloads directory if doesn't exist
if not os.path.isdir(downloads_dir):
	try:
		os.makedirs(downloads_dir)
		print ('Initialized Downloads directory')
	except:
		print ('Could not make Downloads directoy')
		raise

# Create Tmp Downloads directory if doesn't exist
if not os.path.isdir(tmpdownloads_dir):
	try:
		os.makedirs(tmpdownloads_dir)
		print ('Initialized Tmp Downloads directory')
	except:
		print ('Could not make Tmp Downloads directoy')
		raise

# Create Data directory if doesn't exist
if not os.path.isdir(data_dir):
	try:
		os.makedirs(data_dir)
		print ('Initialized Date directory')
	except:
		print ('Could not make Data directoy')
		raise

# Create Blacklist file if doesn't exist
if not os.path.exists(blacklist_file):
	try:
		f = open(blacklist_file,"w+")
		f.close()
		print ('Initialized Blacklist file')
	except:
		print ('Could not make Blacklist file')
		raise


# Prompt user for playlist url
playlist = raw_input("Enter YouTube playlist url: ")
# playlist = "https://www.youtube.com/playlist?list=PLC4EWNG6GsuZpxgiXSpL1yoDlNFXfrh3Y"

# Prompt user for reverse playlist check
usereverse = True if raw_input("Reverse playlist? (y/n): ") == 'y' else False

# Prompt user for limit
videolimit = int( raw_input("Video limit? (-1 for unlimited): ") )

# Create playlist object
pl = Playlist(playlist)

# Load playlist video urls
print ('\nLoading video urls...')
pl.populate_video_urls()

# Reverse order if demanded
if usereverse:
	pl.video_urls.reverse()

# for video in pl.video_urls:
# 	print video

# Video count
video_count = len(pl.video_urls)

# Counter
counter = 0

# Loop through urls
for video in pl.video_urls:

	# Check limit
	if counter == videolimit:
		continue
		

	# Incremet counter
	counter = counter + 1

	print video


	# Check blacklist
	blacklist = open(blacklist_file).read().splitlines()
	if video in blacklist:
		print ('Skipping ' + str(video))
		continue


	# Create youtube object
	print ('\nStarting ' + video + '... [' + str(counter) + '/' + str(video_count) + ']')
	yt = get_video(video)

	# Print video title
	print ('Title: ' + str(yt.title))

	# Load audio stream
	print ('Loading stream...')
	stream = get_stream(yt)
	if not stream:
		continue
	print ('Stream: ' + str(stream))

	# Download stream
	print ('Downloading...')
	dl = download_video(stream)
	print dl

	# Move out of tmp folder
	for f in os.listdir(tmpdownloads_dir):
		if os.path.isfile(os.path.join(tmpdownloads_dir, f)):
			if f in dl:
				print ('Moving file from tmp...')
				shutil.move(dl, downloads_dir + '/' + f)

	# Blacklist
	print ('Blacklisting...')
	blacklist = open(blacklist_file,'a')
	blacklist.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '\n')
	blacklist.write(yt.title + '\n')
	blacklist.write(video + '\n\n')
	blacklist.close()


