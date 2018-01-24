#The Language detection algorithm from langdetect is non-deterministic

from string import punctuation
import re
from langdetect import detect #https://pypi.python.org/pypi/langdetect

def clean_lyrics(lyrics):
    # punctuation string: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    punctuation_regex = re.compile('[{}]'.format(punctuation.replace("'", "")))
    lyrics = punctuation_regex.sub(' ', lyrics)
    lyrics = re.sub(r"'+", "", lyrics)
    lyrics = re.sub(r"\\uFFFD", '_', lyrics) #replaces unicode unknown characters with underscores
    lyrics.lower()
    lyrics = re.sub(r"[^a-z]_+[^a-z]", ' ', lyrics) #remove all underscores not preceded by a letter
    lyrics = re.sub(r"\\r", '', lyrics) #remove line ending symbols
    lyrics = re.sub(r"\\n", '', lyrics) #remove line ending symbols
    lyrics = re.sub(r"\\", ' ', lyrics) #remove backslashes
    lyrics = re.sub(' +', ' ', lyrics) #remove 
    return lyrics.strip()

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

def clean_nq(raw_lyrics_loc = "lyrics.nq"):
	songs = 0
	foreign = 0
	languages = {}
	with open("new.csv", 'w') as new:
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

clean_nq()