import gensim
from gensim.models import word2vec as w2v
from os.path import exists
import numpy as np

#if an model is found it is loaded, otherwise a new model is created
#from the datafile, make_new forces a new model to be created, regardless 
#of any already existing model.
def create_model(data_file, model_file, make_new = False):
	if not exists(model_file) or make_new:
		print("creating new model...")
		sentences = w2v.LineSentence(data_file)
		model = w2v.Word2Vec(sentences, size=100, window=3, min_count=5, workers=4)
		model.save(model_file)
	else:
		print("loading existing model...")
		model = w2v.Word2Vec.load(model_file)
	return model

#creates a vector for an entity (either song or input text)
#by averaging all the words in the entity
def create_entity_vector(model, words):
	entity_vec = 0
	word_vecs = []
	for word in words:
		try:
			word_vecs.append(model.wv[word])
		except:
			#word not recognized
			pass #anders?

	#method 1
	entity_vec = np.average(np.matrix(word_vecs), axis=0)
	#TODO: implement different methods?

	return entity_vec.tolist()[0]

def printable_vec(vector):
	printable = ""
	for number in vector:
		printable += str(number) + ','
	return printable[:-1] #remove last ','

#creates a vector for each song, as retrieved from lyrics_txt with the use of index_txt
#all the new songvectors are saved in the newly created song_vectors_file
def create_entity_vectors(model, lyrics_txt, index_txt, song_vectors_file):
	with open(lyrics_txt, 'r') as lyrics_doc:
		with open(index_txt, 'r') as index_doc:
			with open(song_vectors_file, 'w') as vector_doc:
				index_lines = index_doc.readlines()
				pointer = 0
				for line in index_lines:
					song_id, index_begin, index_end = line.split(';')[:3]
					words = []
					while pointer < int(index_end):
						line = lyrics_doc.readline()
						words += line.split()
						pointer += 1
					entity_vec = create_entity_vector(model, words)
					vector_doc.write(song_id + ';' + printable_vec(entity_vec) + '\n')

def create_test_entity(model, lyrics_txt):
	words = []
	with open(lyrics_txt, 'r') as lyrics_doc:
		for line in lyrics_doc.readlines():
			words += line.split()
	entity_vec = create_entity_vector(model, words)
	return entity_vec