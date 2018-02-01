from process_lyrics import clean_kaggle_songlyrics, clean_txt
from create_embeddings import create_model, create_entity_vectors, create_test_entity
from compare_embeddings import compare_vectors

from datetime import datetime

#to be used in the creation of a new file
def date_name():
	return str(datetime.now())[:16].replace('-', '_').replace(':', '.'). replace(' ', '_') 

##file_locations:
kaggle_songfile = "songlyrics/songdata.csv"

test_file = "test3_raw.txt"

##intermediate files
clean_lyrics_file = "data/songlyrics.txt"
lyrics_index_file = clean_lyrics_file[:-4]+".index"
model_file = "data/lyrics.model"
song_vectors_file = "data/songs.vectors"

clean_test_file = "data/test.txt"
# clean_test_file = "data/test[" + date_name() + "].txt"



make_new_model = False

if make_new_model:
	clean_kaggle_songlyrics(kaggle_songfile, clean_lyrics_file, lyrics_index_file)

model = create_model(clean_lyrics_file, model_file, make_new_model)

if make_new_model:
	create_entity_vectors(model, clean_lyrics_file, lyrics_index_file, song_vectors_file)

clean_txt(test_file, clean_test_file)
test_entity = create_test_entity(model, clean_test_file)

compare_vectors(test_entity, song_vectors_file, lyrics_index_file)