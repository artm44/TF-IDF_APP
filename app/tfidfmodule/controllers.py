from flask import Blueprint, render_template, request, jsonify

from .models import Word, Document, db as db_
from .TF_IDF_RepositoryDB import TfIdfDB
from .tfidf_utils import *

module = Blueprint('tfidf', __name__)

MAX_COUNT_WORDS = 50  # Максимальное количество записей для вывода

db = TfIdfDB(db_)


@module.route('/')
def index():
    return render_template('index.html'), 200


@module.route('/tfidf', methods=['POST'])
def get_tf_idf():
    """
    Метод для получения tf_idf (Без загрузки файла в БД!)
    """
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        # Обработка файла для вычисления TF-IDF
        word_counts, total_words = words_from_file(file)

        total_documents = db.get_count_documents()

        words_data = []
        for word, count in word_counts.items():
            word_documents = db.get_word_count(word)
            tf, idf = calculate_tf_idf(count, total_words, total_documents + 1, word_documents + 1)
            words_data.append((word, tf, idf))

        # Сортировка данных по убыванию IDF
        words_data.sort(key=lambda x: x[2], reverse=True)

        return render_template('index.html', words=words_data[:MAX_COUNT_WORDS]), 200
    else:
        return "Invalid file format", 400


@module.route('/document', methods=['GET'])
def get_documents():
    """
    Метод для получения всех файлов в БД, используемых для учета TF-IDF
    """
    documents = db.read_documents()
    if documents:
        documents_list = [{'id': document.id, 'name': document.name} for document in documents]
        return jsonify(documents_list), 200
    else:
        return "Not found", 404


@module.route('/document', methods=['POST'])
def upload_document():
    """
    Метод для добавалнения документа в БД, для учета tf_idf
    """
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        # Обработка файла для вычисления TF-IDF
        word_counts, total_words = words_from_file(file)

        words = [Word(word=word, count=1) for word in word_counts.keys()]

        # Процесс добавления нового документа с его словами
        status = db.add_data(words, Document(name=file.filename))
        if status is not True:
            return "Problem with database", 500

        return "Success", 200

    else:
        return "Invalid file format", 400


@module.route('/document/<doc_id>', methods=['DELETE'])
def delete_document(doc_id: int):
    """
    Метод для удаление документа в БД, для учета tf_idf
    """
    document = db.read_document(doc_id)
    if document:
        result = db.delete_document(document)
        if result:
            return "Success", 200
        else:
            return "Problem with database", 500
    else:
        return "Not found", 404
