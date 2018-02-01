import gensim
from gensim.models import word2vec as w2v
from os.path import exists
import numpy as np

def create_model(data_file, model_file, make_new = False):
	if not exists(model_file) or make_new:
		print("creating new model...")
		sentences = w2v.LineSentence(data_file)
		model = w2v.Word2Vec(sentences, size=100, window=3, min_count=5, workers=4)
		model.save(model_file)
	else:
		print("loading existing model...")
		model = w2v.Word2Vec.load(model_file)
		# word_vectors = model.wv
		# del model
	return model

#TODO: implement different methods
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

	return entity_vec.tolist()[0]

def printable_vec(vector):
	printable = ""
	for number in vector:
		printable += str(number) + ','

	return printable[:-1] #remove last ','


#entity is either a song or an input text
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


# model = create_model()
# print(create_test_entity(model, "test4.txt"))


# create_entity_vectors(model, "songlyrics/songdata.txt", "songlyrics/songdata.index.txt")


# model = create_model()
# print(model.wv.most_similar(positive=['woman', 'king'], negative=['man']))
# print(model.most_similar_cosmul(positive=['man', 'queen'], negative=['woman']))
# print()
# print(model.wv.most_similar(positive=['goddess']))
