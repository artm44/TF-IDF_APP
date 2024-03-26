from app.database import db


# Таблица реализующая связь многие ко многим
document_word = db.Table('document_word',
                         db.Column('document_id', db.Integer, db.ForeignKey('document.id')),
                         db.Column('word_id', db.Integer, db.ForeignKey('word.id'))
                         )


class Document(db.Model):
    """ Модель записи о документах """
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название документа
    words = db.relationship('Word', secondary=document_word, backref='words')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return 'Document %r' % self.id


class Word(db.Model):
    """ Модель записи о словах """
    __tablename__ = 'word'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)  # Слово
    count = db.Column(db.Integer, nullable=False, default=0)  # Число документов, в которых встречается слово

    def __init__(self, word: str, count: int = 0):
        self.word = word
        self.count = count

    def __repr__(self) -> str:
        return 'Word %r' % self.id
