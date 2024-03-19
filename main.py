import os
import sys
from datetime import date, datetime
import locale
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QDialog, QMessageBox
from PySide6 import QtCore
from osnova import Ui_MainWindow
from cont import Ui_Dialog
from sqlalchemy import  create_engine, text
from sqlalchemy.orm import Session
from docxtpl import DocxTemplate

class Dialog(QDialog):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.engines = create_engine("sqlite+pysqlite:///db/bpk.db", echo=True)
        self.ui.btnAdd.clicked.connect(self.accept)
        self.ui.btnCancel.clicked.connect(self.reject)

        self.load_bd_listwidget_cont()
        self.ui.btnDeletCont.clicked.connect(self.delet_btn_cont)

        self.ui.comboBox.currentIndexChanged.connect(self.on_activ_combobox)


    def get_data(self):
        return {
            
            "name_org_full": self.ui.lineEdit.text(),
            "inn": self.ui.lineEdit_2.text(),
            "kpp": self.ui.lineEdit_3.text(),
            "adres": self.ui.lineEdit_4.text(),
            "bik": self.ui.lineEdit_5.text(),
            "ras_chet": self.ui.lineEdit_6.text(),
            "kor_chet": self.ui.lineEdit_7.text(),
            "tel": self.ui.lineEdit_8.text(),
            "emal": self.ui.lineEdit_9.text(),
            "name_org": self.ui.lineEdit_10.text(),
            "fio": self.ui.lineEdit_11.text(),
            "fio_full": self.ui.lineEdit_12.text(),
            "ogrn": self.ui.lineEdit_13.text(),
            "bank": self.ui.lineEdit_14.text(),
            "dolzhnost": self.ui.comboBox.currentText(),
            "dolzhnost_r": self.ui.comboBox_2.currentText(),
            }
    
    def load_bd_listwidget_cont(self):

        with Session(self.engines) as s:
            query = '''
            SELECT * FROM org
            '''

            rows = s.execute(text(query))
            for r in rows:

                item = QListWidgetItem(f'{r.name_org} {r.inn} {r.fio}')
                item.setData(QtCore.Qt.ItemDataRole.UserRole, r)
                self.ui.listWidget_c.addItem(item)

    def delet_btn_cont(self):

        item = self.ui.listWidget_c.currentItem()
        data = item.data(QtCore.Qt.ItemDataRole.UserRole)

        with Session(self.engines) as s:

            query = '''
            DELETE
            FROM org
            WHERE id = :id
            '''
            s.execute(text(query), {'id': data.id})
            s.commit()
        
        self.ui.listWidget_c.clear()
        self.load_bd_listwidget_cont()

    def on_activ_combobox(self, index):
        self.ui.comboBox_2.setCurrentIndex(index)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.engine = create_engine("sqlite+pysqlite:///db/bpk.db", echo=True)

        self.caledar_today()
        self.ui.dateEdit.dateChanged.connect(self.on_dateedit_change)
        self.ui.calendarWidget.clicked.connect(self.on_click_caledar)

        self.ui.btnClose.clicked.connect(lambda:self.close())


        self.load_bd_comboBox()
        self.load_bd_listwidget_osnova()
        self.ui.comboBox.currentIndexChanged.connect(self.load_bd_listwidget_osnova)
        
        self.ui.btnAddCont.clicked.connect(self.add_btn_cont)
        self.ui.btnSave.clicked.connect(self.save_btn_ocnova)

        self.ui.btnEditCont.clicked.connect(self.edit_btn_cont)

        self.ui.btnDeletOsnova.clicked.connect(self.delet_btn_osnova)

    # Открытие 2-ой формы через кнопку    
    def add_btn_cont(self):
        dialog = Dialog()
        r = dialog.exec()

        if r == 0:
            self.load_bd_listwidget_osnova()
            return
        
        data = dialog.get_data()

        with Session(self.engine) as s:
            query = """
            INSERT INTO org (name_org_full, inn, kpp, adres, bik, ras_chet, kor_chet, tel, emal, name_org, fio, fio_full, ogrn, bank, dolzhnost, dolzhnost_r)
            VALUES (:n_o_f, :i, :k, :a, :bi, :r, :ko, :t, :e, :n_o, :f, :f_f, :o, :ba, :d, :d_r)
            """
            s.execute(text(query), {
                'n_o_f': data ['name_org_full'],
                'i': data['inn'],
                'k': data['kpp'],
                'a': data['adres'],
                'bi': data['bik'],
                'r': data['ras_chet'],
                'ko': data['kor_chet'],
                't': data['tel'],
                'e': data['emal'],
                'n_o': data['name_org'],
                'f': data['fio'],
                'f_f': data['fio_full'],
                'o': data['ogrn'],
                'ba': data['bank'],
                'd': data['dolzhnost'],
                'd_r': data['dolzhnost_r']
            })
            s.commit()
        
        self.load_bd_listwidget_osnova()

    def save_btn_ocnova(self):
        
        item = self.ui.listWidget_o.currentItem() 
        data = item.data(QtCore.Qt.ItemDataRole.UserRole)

        with Session(self.engine) as s:
            query = '''
            SELECT * 
            FROM org 
            WHERE id = :id
            '''

            s.execute(text(query), {'id': data.id})



        doc = DocxTemplate("db/шаблон.docx")
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        nomer_dog = self.ui.dateEdit.dateTime().toString("dd/MM-yyyy")
        data_dog1 = self.ui.dateEdit.dateTime().toString("«dd» MMMM yyyy г.")
        data_dog2 = self.ui.dateEdit.dateTime().toString("dd.MM.yyyy")

        # 'ogrn':data.ogrn,
        context = {'nomer_dog':nomer_dog, 'data_dog1':data_dog1, 'data_dog2':data_dog2, 
                    'name_o_full':data.name_org_full, 'fio_full':data.fio_full,
                    'emal':data.emal, 'tel':data.tel, 'fio':data.fio, 'inn':data.inn,
                    'name_o':data.name_org, 'dolzhnost':data.dolzhnost, 'bik':data.bik,
                    'kpp':data.kpp, 'kor_chet':data.kor_chet, 'bank':data.bank,
                    'adres':data.adres, 'ras_chet':data.ras_chet, 'ogrn':data.ogrn,
                    'dolzhnost_r':data.dolzhnost_r}
        doc.render(context, autoescape=True)
        doc.save(str(f"db/Договор поставки № ИН_{data_dog2} - {data.name_org}.docx"))





    def edit_btn_cont(self):
        dialog = Dialog()
        r = dialog.exec()

    # Удаление данных с основной формы в tablewidget
        
 
 
    def delet_btn_osnova(self):  

        item = self.ui.listWidget_o.currentItem() 
        data = item.data(QtCore.Qt.ItemDataRole.UserRole)


        with Session(self.engine) as s:
            query = '''
            DELETE 
            FROM org 
            WHERE id = :id
            '''

            s.execute(text(query), {'id': data.id})
            s.commit()
        
        self.load_bd_listwidget_osnova()

    def caledar_today(self):

            now = datetime.now()
            self.ui.dateEdit.setDate(now)
            data = self.ui.dateEdit.dateTime().toString("dd/MM-yyyy")
            self.ui.label.setText("%s" % data)

    def on_dateedit_change(self):

        data = self.ui.dateEdit.dateTime().toString("dd/MM-yyyy")
        self.ui.label.setText("%s" % data)

        self.ui.calendarWidget.setSelectedDate(self.ui.dateEdit.date())

        

    def on_click_caledar(self):

        self.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())

    # Вывод данных с БД в tableWidget
        
    def load_bd_listwidget_osnova(self):

        self.orgnam = {}
        org_data = self.ui.comboBox.currentData()
        if org_data:
            org_id = self.ui.comboBox.currentData().id
        else: 
            org_id = 0

        self.ui.listWidget_o.clear()
   

        with Session(self.engine) as s:
            query = '''
            SELECT * FROM org
            WHERE (:oid = 0 OR id = :oid)
            '''

            rows = s.execute(text(query), {'oid': org_id})
            for r in rows:

                item = QListWidgetItem(f'{r.name_org} {r.inn} {r.fio}')
                item.setData(QtCore.Qt.ItemDataRole.UserRole, r)
                self.ui.listWidget_o.addItem(item)

    # Вывод данных с БД в comboBox
                
    def load_bd_comboBox(self):
        
        self.orgname = {}

        with Session(self.engine) as s:
            query = '''
            SELECT * FROM org
            ORDER BY name_org
            '''
            
            rows = s.execute(text(query))
            for r in rows:
                self.orgname[r.id] = r

        self.ui.comboBox.addItem('-')
        for r in self.orgname.values():

            self.ui.comboBox.addItem(r.name_org, r)
        self.load_bd_listwidget_osnova()

        

if __name__ == '__main__':

    app = QApplication(sys.argv)


    window = MainWindow()
    window.show()

    sys.exit(app.exec())
