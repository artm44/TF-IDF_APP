from .models import Word, Document, document_word
from app.database_utils import commit_cud_operation


class TfIdfDB:
    """ Класс для работы с таблицами """

    def __init__(self, db) -> None:
        self.db = db

    @commit_cud_operation
    def create_document(self, document: Document) -> int:
        self.db.session.add(document)
        self.db.session.commit()
        return document.id

    def read_document(self, doc_id: int) -> Document:
        return self.db.session.query(Document).filter(Document.id == doc_id).first()

    def read_documents(self) -> list[Document]:
        return self.db.session.query(Document).all()

    @commit_cud_operation
    def delete_document(self, document: Document) -> bool:
        # Удаление связанных записей из таблицы document_word
        related_words = Word.query.join(document_word).filter(document_word.c.document_id == document.id).all()
        for word in related_words:
            word.count -= 1

        document_word_query = document_word.delete().where(document_word.c.document_id == document.id)
        self.db.session.execute(document_word_query)
        self.db.session.delete(document)
        self.db.session.commit()
        return True

    @commit_cud_operation
    def create_word(self, word: Word) -> int:
        self.db.session.add(word)
        self.db.session.commit()
        return word.id

    @commit_cud_operation
    def add_data(self, words: list[Word], document: Document) -> bool:
        self.db.session.add(document)
        for word in words:
            existing_word = Word.query.filter_by(word=word.word).first()
            if existing_word:
                existing_word.count += word.count
                document.words.append(existing_word)
            else:
                self.db.session.add(word)
                document.words.append(word)
        self.db.session.commit()
        return True

    @commit_cud_operation
    def delete_word(self, word: Word) -> bool:
        result = self.db.session.query(Word).filter(Word.id == word.id).first()
        self.db.session.delete(result)
        self.db.session.commit()
        return True

    def get_word_count(self, word: str) -> int:
        result = self.db.session.query(Word).filter(Word.word == word).first()
        if result:
            return result.count
        return 0

    def get_count_documents(self) -> int:
        return self.db.session.query(Document).count()
