from pytube import Playlist			# get playlist
from pytube import YouTube			# main file getter
import pytube						# needed?  Couldn't get exceptions working
import re							# to clean up file names
import time							# to time our requests
import os							# for clear screen detection
from os import system, name 		# for os detection, maybe "system"
import sys							# sys.exit and a few things

from colorama import init			# for colors
init()

version = '1.2'


'''
OVERVIEW
	Download youtube streams as video or audio in batch or single
	Example:   Entire playlists, Movies, Single videos
	You can choose to save video or audio only to save space

	Bad/Unreliable Internet:
		Travelling but no wifi or bad wifi?  Load up a bunch of stuff ahead of time
		Want to save offline bandwidth and manually transfer files around for some reason?
		Good internet one place, bad internet another (or expensive/limited on phone?)
		Share content via usb or other means to someone that doesn't have internet
		no wifi on phone or portable music device?

	Privacy/Ads:
		Don't like google tracking what you do, watch or download?
		Sick of ads? Sick of ads?  SIck of ads?  SICK OF ADS?!?!?

	Save Time:
		Example: COMPLETED 200 FILES: 944.7422 seconds (jim rohn audios)
		Want to automate the process of learning without youtube's controls?
		Just queue it up, download, then listen/watch to ONLY what you want without distractions

	Control of Content:
		Need video/audio  content for something you are editing?
		Don't need video stream and only want audio?
		Don't like "related videos" disrupting your study/flow etc?
		Need to hide the "internet catz" that all videos lead to?
		Want to learn a language/topic and need a custom playlist?
		Distracted easily when building your list of content?
		Need Archive of content that may not be available later?
		tag files with a name prefix so you can easily find/watch them again offline


PRE-REQUISITES
	You need git, linux should be easy, but on windows that is:
	https://git-scm.com/download/win
	I chose bash style, as admin and accepted other defaults

INSTALL (git not pypi):
	pip uninstall pytube
	pip uninstall pytube3
	python -m pip install git+https://github.com/nficano/pytube

SOME DOCS:
	https://python-pytube.readthedocs.io/en/latest/user/quickstart.html
	https://python-pytube.readthedocs.io/en/latest/_modules/pytube/exceptions.html
	https://python-pytube.readthedocs.io/en/latest/api.html
	https://github.com/nficano/pytube/blob/master/tests/test_exceptions.py
	https://readthedocs.org/projects/python-pytube/downloads/pdf/stable/

CODE INSPIRATION:
	https://simply-python.com/2019/01/02/downloading-youtube-videos-and-converting-to-mp3/
	https://www.geeksforgeeks.org/create-gui-for-downloading-youtube-video-using-python/
	https://askubuntu.com/questions/486297/how-to-select-video-quality-from-youtube-dl
	https://www.programcreek.com/python/example/92182/pytube.YouTube
	https://stackoverflow.com/questions/54028675/pytube-library-receiving-pytube-exceptions-regexmatcherror-regex-pattern-er


USAGE:
	C:\>python youtube-dl.py
	YOUTUBE RIP V 1.1 based on pytube module
	 GOOGLE LIST: try google dorking for a list:
	 Example: 'some thing' inurl:playlist site:youtube.com
	 TOP HITS LISTS: https://music.youtube.com/
		 playlist or single? -> p
			 video or audio? -> a
						 URL -> https://www.youtube.com/playlist?list=PLbIe5yv16PncyNbUNNLkHdR_iVwytFf9o
	file prefix (ie: acoustic guitar) -> self discipline 2
	 Number of videos in playlist: 8
	 https://www.youtube.com/watch?v=ft_DXwgUXB0    ####################    SAVED: 3.4 seconds a_self_discipline_2_self_discipline_best_motivational_speech_video_featuring_will_smith
	 https://www.youtube.com/watch?v=CJEsIR6EcIY    ####################    SAVED: 3.5 seconds a_self_discipline_2_monday_motivation_start_your_day_right_powerful_motivation
	 https://www.youtube.com/watch?v=kak8PEl_v1I    ####################    SAVED: 3.3 seconds a_self_discipline_2_6_minutes_to_start_your_day_right_morning_motivation_motivational_video_for_success
	 https://www.youtube.com/watch?v=ni_HDRKPnJk    ####################    SAVED: 3.8 seconds a_self_discipline_2_you_need_to_do_this_in_the_morning_it_will_change_your_entire_day_morning_motivation
	 https://www.youtube.com/watch?v=ItDjjHPegGU    ####################    SAVED: 3.3 seconds a_self_discipline_2_the_psychology_of_the_1_best_motivational_video
	 https://www.youtube.com/watch?v=yZ3hc3fiuxU    ####################    SAVED: 3.7 seconds a_self_discipline_2_remember_your_dream_motivational_workout_speech_2020
	 https://www.youtube.com/watch?v=hFWGWl10vuQ    ####################    SAVED: 3.5 seconds a_self_discipline_2_2020_go_hard_mindset_high_performance_lessons_from_billionaire_dan_pena
	 https://www.youtube.com/watch?v=vPMQdVdR0gw     FAILED: Video/Account Private, Deleted or other issue? https://www.youtube.com/watch?v=vPMQdVdR0gw

	COMPLETED 8 FILES: 24.7598 seconds
		USER TERMINATED SESSION

HISTORY
	Dec 17 2020 1.0 
		- sent out to some friends after about 20 hours total code time
	
	Dec 19 2020 1.1 
		- reduced typing requirements on input fields, now accepts p, s, a, v
		- added a version tracker
		- more pythonic
		- error checking on private/deleted videos
		- fixed time display to show per loop instead of start/finish runs
		- Slightly better UI that explains/helps
		- error checking on inputs
		- added google dorks example to help find playlists
		- updated normalize() to allow numbers in file names
		- added more documentation/code explanation
	
	Dec 20 2020 1.2
		- Added short pause at the end in case run by double click
		



'''


previousprogress = 0

# class ripped from geeks for geeks colorama tutorial
class colors: 
	reset='\033[0m'
	bold='\033[01m'
	disable='\033[02m'
	underline='\033[04m'
	reverse='\033[07m'
	strikethrough='\033[09m'
	invisible='\033[08m'
	class fg: 
		black='\033[30m'
		red='\033[31m'
		green='\033[32m'
		orange='\033[33m'
		blue='\033[34m'
		purple='\033[35m'
		cyan='\033[36m'
		lightgrey='\033[37m'
		darkgrey='\033[90m'
		lightred='\033[91m'
		lightgreen='\033[92m'
		yellow='\033[93m'
		lightblue='\033[94m'
		pink='\033[95m'
		lightcyan='\033[96m'
		white='\033[37m'
	class bg: 
		black='\033[40m'
		red='\033[41m'
		green='\033[42m'
		orange='\033[43m'
		blue='\033[44m'
		purple='\033[45m'
		cyan='\033[46m'
		lightgrey='\033[47m'

# for screen clears independent of OS
def clear(): 
	# for windows 
	if name == 'nt': 
		_ = system('cls') 
  
	# for mac and linux(here, os.name is 'posix') 
	else: 
		_ = system('clear')


# given an playist, feed each URL into the downloadStream function
def downloadPlaylist(category,vid_url,stream_type):
	# get playlist urls first
	# google dork it:   motivational speech inurl:playlist site:youtube.com
	# playlist must be public
	# all videos must be public and not deleted
	# https://www.youtube.com/view_all_playlists (make/manage your own)
	# https://music.youtube.com/explore (others, audio only) 
	# google for "topic" playist youtube (find premade playlists)
	# watch any video, and if it's part of a playlist copy that playlist id manually

	vid_url = vid_url.strip()
	category = normalize(category)
	playlist = Playlist(vid_url)
	print(colors.fg.green,'Number of videos in playlist: %s' % len(playlist.video_urls))
	for url in playlist.video_urls:
		print(colors.fg.white,url,end="\t")
		global previousprogress
		previousprogress = 0
		downloadStream(category,url,stream_type)
	return len(playlist.video_urls)


# I want my file names a certain way
def normalize(data):
	dirty = str(data)			#fixme: might not be required to typecast to string
	dirty = dirty.strip()		# remove text from front/back
	dirty = dirty.lower()
	dirty = re.sub('[^a-zA-Z0-9 ]+', '', dirty)
	dirty = re.sub(' +', ' ', dirty)
	dirty = re.sub(' ', '_', dirty)
	return dirty

# a stupid progress meter because I didn't want to do my actual work
def progress(stream, chunk, bytes_remaining):
	global previousprogress
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining 

	liveprogress = (int)(bytes_downloaded / total_size * 100)
	if liveprogress > previousprogress:
		previousprogress = liveprogress
		if (liveprogress % 5 == 0):
			if liveprogress  < 20:
				print(colors.fg.pink,end="")
				print('#',end="")
			elif liveprogress  < 40:
				print(colors.fg.red,end="")
				print('#',end="")
			elif liveprogress  < 60:
				print(colors.fg.orange,end="")
				print('#',end="")
			elif liveprogress  < 80:
				print(colors.fg.yellow,end="")
				print('#',end="")
			else:
				print(colors.fg.green,end="")
				print('#',end="")

# this is the actual "work" of the script
def downloadStream(category,vid_url,stream_type):
	vid_url = vid_url.strip()

	# start our timer
	tic = time.perf_counter()

	# fixme: update other exceptions
	try:
		#yt = YouTube(vid_url).check_availability()
		#yt = YouTube(vid_url)
		yt = YouTube(vid_url, on_progress_callback=progress)
		#https://www.youtube.com/playlist?list=PLfC8rK3hcHf3XOzFgz4Kq4tbGL-2Ql67F
	except: #pytube.exceptions.PytubeError:
	
		#end our timer on a fail
		toc = time.perf_counter()
	
		print(colors.fg.red,"FAILED: Video/Account Private, Deleted or other issue?", vid_url)
		return 0

	# it passed the try, so ... do the work
	yt = YouTube(vid_url, on_progress_callback=progress)
	if stream_type == 'v':
		file_name = 'v_' + category + '_' + normalize(yt.title)
		try:
			yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(filename=file_name)
		except:
			print(colors.fg.red,"FAILED: Maybe Deleted Video/Account?", vid_url)
			return 0

	elif stream_type == 'a':
		file_name = 'a_' + category + '_' + normalize(yt.title)
		try:
			yt.streams.filter(only_audio=True).first().download(filename=file_name)
		except:
			print(colors.fg.red,"FAILED: Unknown Error", vid_url)
			return 0

	else:
		print(colors.fg.red,"FAILED: Unknown stream type: ", stream_type)
		return 0

	# end our timer
	toc = time.perf_counter()
	print(f"\tSAVED: {toc - tic:0.1f} seconds", file_name)
	return 1



# fixme:  put the questions into a while for error checking
def main():

	err = 1
	while err:

		print(colors.fg.green,"YOUTUBE RIP V " + version + " based on pytube module")
		print(colors.fg.green,"GOOGLE LIST: try google dorking for a list:")
		print(colors.fg.yellow,"Example: 'some thing' inurl:playlist site:youtube.com")
		print(colors.fg.green,"TOP HITS LISTS: https://music.youtube.com/")

		#fixme: do you even know what pythonic means? Clean this up!
		print(colors.fg.lightblue,end="")
		pls = 	input('     playlist or single? -> ')
		pl = ['playlist','p','single','s']
		if pls in pl:
			pass
		else:
			print(colors.fg.red,"PLAYLSIT ERROR: enter either 'playlist' or 'p' or 'single' or 's'")
			continue

		print(colors.fg.lightblue,end="")
		media    = 		input('         video or audio? -> ')
		m = ['video', 'v', 'audio', 'a']
		if media in m:
			pass
		else:
			print(colors.fg.red,"MEDIA ERROR: enter either 'audio' or 'a' or 'video' or 'v'")
			continue

		url =      		input('                     URL -> ')
		if re.search('https://', url.lower()):
			pass
		else:
			print(colors.fg.red,"URL ERROR: valid urls look like one of these:")
			print(colors.fg.red,"https://www.youtube.com/playlist?list=PLEB9493F8CCAA16B4 (a playlist)")
			print(colors.fg.red,"https://music.youtube.com/playlist?list=RDCLAK5uy_l39bpxtMK-nGlOep-fF0yW_rFTdG0P5Ig (a music playlist)")
			print(colors.fg.red,"https://www.youtube.com/watch?v=g12T0_OzLLs (a single video)")
			continue
		category = 		input('file prefix (ie: acoustic guitar) -> ')



		if pls[0] == 'p':
			#url = 'https://www.youtube.com/playlist?app=desktop&list=PLlbnzwCkgkTBLzOPP9uE2n5PFgb_zoo4H' # beast mode music
			#url = 'https://www.youtube.com/playlist?list=PLDFAB5C8B5E211CA7' # my guitar list
			#url = 'https://www.youtube.com/playlist?list=PLEB9493F8CCAA16B4' # flute
			#url = 'https://www.youtube.com/playlist?list=PL1D3132FE49665BEA' # ocarina
			#url = 'https://www.youtube.com/playlist?list=PLFA1685353B850A43' # motivation with error files
			# fixme: regex and err if it's not a youtube playlist
			main_tic = time.perf_counter()
			num_files = downloadPlaylist(category,url,media[0])
			main_toc = time.perf_counter()
			print(colors.fg.green, f"\nCOMPLETED %s FILES: {main_toc - main_tic:0.4f} seconds" % num_files)

		elif pls[0] == 's':
			#url = 'https://www.youtube.com/watch?v=g12T0_OzLLs&t=75s' # roller coaster pov
			#url = 'https://www.youtube.com/watch?v=mw9s8q26JPQ' # account deleted generates error
			# fixme: regex and err if it's not a youtube vide
			main_tic = time.perf_counter()
			num_files = downloadStream(category,url,media[0])
			main_toc = time.perf_counter()
			print(colors.fg.green, f"\nCOMPLETED %s FILES: {main_toc - main_tic:0.4f} seconds" % num_files)



if __name__ == '__main__':
	# capture ctrl c
	try:
		main()
	except KeyboardInterrupt:
		print(colors.fg.pink,"\nExiting...")
		sleep(5)
		print(colors.fg.pink,"\nUSER TERMINATED SESSION")

	sys.exit()