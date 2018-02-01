import operator
import matplotlib.pyplot as plt

#cut off words with frequency lower then threshold
def remove_below_freq(sorted_freq_dict, threshold):
	for i, (key, freq) in enumerate(sorted_freq_dict):
		if freq < threshold:
			sorted_freq_dict = sorted_freq_dict[:i]
			return sorted_freq_dict

def frequence_graph(sorted_freq_dict):
	labels, frequency = list(zip(*sorted_freq_dict))

	print("vocab size:", len(labels))

	plt.plot(frequency)
	
	axes = plt.gca()
	axes.set_ylim([0,1000])

	plt.show()

#returns the frequency dictionary of a text
def get_word_freq_dict(text_file = "lyrics.csv"):
	word_counts = {}
	with open(text_file, 'r') as data:
		for line in data.readlines():
			uri, lyrics = line[:-1].split(';') #remove \n
			for word in lyrics.split():
				if len(word) < 25: #different threshold?
					try:
						word_counts[word]+= 1
					except:
						word_counts[word] = 1
	return word_counts

if __name__ == '__main__':

	word_counts = get_word_frequency_dict()

	sorted_words = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
	sorted_words = remove_below_freq(sorted_words, 5)
