import math
import string

ALLOWED_EXTENSIONS = {'txt'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def calculate_tf_idf(word_count, total_words, total_documents, word_documents):
    tf = word_count / total_words
    idf = math.log(total_documents / word_documents, 10)
    return tf, idf


def words_from_file(file):
    word_counts = {}
    total_words = 0

    for line in file:
        # Удаляем знаки препинания
        line = line.decode().translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))).strip()
        words = [word for word in line.split()]
        total_words += len(words)
        for word in words:
            # Приводим к нижнему регистру
            word = word.lower()
            word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts, total_words
