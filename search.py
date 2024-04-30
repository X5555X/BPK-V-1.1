from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Определение модели базы данных
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Создание сессии
engine = create_engine('sqlite:///db/bpk.db')
Session = sessionmaker(bind=engine)
session = Session()

# Функция поиска
def search_users(query):
    return session.query(User).filter(User.name.like(f'%{query}%')).all()

# Пользовательский интерфейс PySide6
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Поиск")
        self.results_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.results_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.search_button.clicked.connect(self.on_search)

    def on_search(self):
        query = self.search_input.text()
        results = search_users(query)
        self.results_list.clear()
        for user in results:
            self.results_list.addItem(f'{user.name} - {user.email}')

# Запуск приложения
app = QApplication([])
window = MainWindow()
window.show()
app.exec()