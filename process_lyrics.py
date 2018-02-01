#The Language detection algorithm from langdetect is non-deterministic

from string import punctuation
import re
from langdetect import detect #https://pypi.python.org/pypi/langdetect

def replace_numbers(lyrics):
	lyrics = re.sub('\d', '6', lyrics)
	return lyrics

def clean_lyrics(lyrics):
	# punctuation string: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
	punctuation_regex = re.compile('[{}]'.format(punctuation.replace("'", "")))
	lyrics = punctuation_regex.sub(' ', lyrics)
	lyrics = re.sub(r"''+", " ", lyrics)
	lyrics = re.sub(r"'", "", lyrics)
	lyrics = re.sub(r"\\uFFFD", '_', lyrics) #replaces unicode unknown characters with underscores
	lyrics = re.sub('\x00', "", lyrics) #remove NUL bytes
	lyrics = lyrics.lower()
	lyrics = re.sub(r"\\r", ' ', lyrics) #remove line ending symbols
	lyrics = re.sub(r"\\n", ' ', lyrics) #remove line ending symbols
	lyrics = re.sub(r"[^a-z]_+[^a-z]", ' ', lyrics) #remove all underscores not preceded by a letter
	lyrics = re.sub(r"\\", ' ', lyrics) #remove backslashes
	lyrics = re.sub('  +', ' ', lyrics) #remove surplus spaces

	lyrics = replace_numbers(lyrics)

	lyrics = re.sub('\n +', '\n', lyrics)
	lyrics = re.sub("\n\n+", '\n', lyrics) #remove empty lines
	return lyrics.strip() #remove spare start end spaces

def detect_languages(languages, lyrics):
	language = ""
	try:
		language = detect(lyrics)
		try: #add language count to frequency dict
			languages[language]+= 1
		except:
			languages[language] = 1
	except:
		print("error:", uri, lyrics)
		print('---')
	return language

def clean_nq(raw_lyrics_loc = "lyrics.nq", new_file = "lyrics.csv"):
	songs = 0
	foreign = 0
	languages = {}
	with open(new_file, 'w') as new:
		with open(raw_lyrics_loc, 'r') as raw:
			for line in raw.readlines():
				line = line.split()
				uri = "<http://purl.org/midi-ld/pattern/" + line[0][25:] #new uri prefix
				lyrics = line[2:-2] #remove index 0 (uri), index 1 (label), index 3 and final '.'
				if len(lyrics) < 5: #do not add lyrics with less then 5 five words
					continue
				lyrics = clean_lyrics(' '.join(lyrics))
				if len(lyrics) < 25: #do not add lyrics with less then 25 letters
					continue
				language = detect_languages(languages, lyrics)
				if language == 'en':
					new.write(uri + ';' + lyrics + '\n')
					songs+= 1
				else:
					foreign+= 1

	print("found", songs, "English song.")
	print("found", foreign, "songs in", len(languages.values()), "foreign languages.")

	print("\nlanguage distribution:")
	print(languages)

#clean_csv creates a file of lyrics without the uri, every line in one song
def clean_csv(csv_lyrics = "lyrics.csv", txt_lyrics = "lyrics.txt"):
	with open(txt_lyrics, 'w') as new:
		with open(csv_lyrics, 'r') as orig:
			for line in orig.readlines():
				uri, lyrics = line.split(';')
				new.write(lyrics)

#only nq_file should exist, csv_file and txt_file will be created/overwritten.
def clean_lyrics_pipeline(nq_file = "lyrics.nq", csv_file = "lyrics.csv", txt_file = "lyrics.txt"):
	clean_nq(nq_file, csv_file)
	clean_csv(csv_file, txt_file)

def clean_kaggle_songlyrics(kaggle_lyrics, new_file, index_file):
	with open(new_file, 'w') as new:
		with open(index_file, 'w') as new_index:
			with open(kaggle_lyrics, 'r') as kaggle:
				kaggle.readline() #skip first line
				data = kaggle.read()
				lines = data.split("\n\n\"")
				index_pointer = 0
				for line in lines:
					try:
						info, lyrics = line.split(".html,\"")
					except:
						print(line)
						break
					lyrics = re.sub("\s*\n\s*\n", '\n', lyrics) #remove empty lines between verses
					lyrics = clean_lyrics(lyrics)
					new.write(lyrics+'\n')
					
					id = (info[-8:])
					artist, song_name = info.split(',')[:2]
					artist = re.sub(r'\n', '', artist)
					song_name = re.sub('\"', '', song_name)

					new_index.write(id + ';' + str(index_pointer)+ ';' + str(index_pointer + len(lyrics.split('\n'))) +  ';' + artist + ';' + song_name + '\n')
					index_pointer += len(lyrics.split('\n'))

#clean one single txt file
def clean_txt(txt_file, new_file = ""):
	with open(txt_file, 'r') as raw:
		lyrics = raw.read()
		lyrics = clean_lyrics(lyrics)
		if new_file != "":
			with open(new_file, 'w') as new:
				new.write(lyrics+'\n')
		else:
			return lyrics