from sqlalchemy import Column, String

class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name_org_full = Column(String)
    inn = Column(String)
    kpp = Column(String)

# Метод для загрузки данных из базы данных в QLineEdit виджеты
def load_data_to_line_edits(self):
    # Предполагается, что у вас есть сессия под названием 'session'
    # и вы хотите получить первую запись из таблицы 'organizations'
    organization = session.query(Organization).first()
    if organization:
        # Установка значений в QLineEdit виджеты
        self.ui.lineEdit.setText(organization.name_org_full)
        self.ui.lineEdit_2.setText(organization.inn)
        self.ui.lineEdit_3.setText(organization.kpp)
    else:
        # Если организация не найдена, можно установить пустые строки
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit_3.setText("")