# Don't forget to make functions to but parts of the bog function(get_money) in and call them as needed
from pyzbar.pyzbar import decode
import numpy as np
import cv2
from os import path
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import sys
from xlsxwriter import *
from PyQt5.uic import loadUiType
from datetime import date
from datetime import timedelta
import decimal
import pymysql
pymysql.install_as_MySQLdb()
mydata = ''
l = []
ui, _ = loadUiType('ATM.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.DB_Connection()
        self.ui_changes()
        self.handel_buttons()

    def DB_Connection(self):
        # handelling database connection
        self.db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password='withallah',
            db='atm'
        )
        self.cur = self.db.cursor()

    def handel_buttons(self):
        self.pushButton_2.clicked.connect(self.start_qrcode)
        self.pushButton.clicked.connect(self.choose_tab)
        self.pushButton_9.clicked.connect(self.come_out)
        self.pushButton_10.clicked.connect(self.money_in)
        self.pushButton_11.clicked.connect(self.money_out)
        self.pushButton_12.clicked.connect(self.come_out)
        self.pushButton_19.clicked.connect(self.come_out)
        self.pushButton_20.clicked.connect(self.come_out)
        self.pushButton_18.clicked.connect(self.money_data)
        self.pushButton_7.clicked.connect(self.ensur_adding_money)
        self.pushButton_15.clicked.connect(self.get_money)
        self.pushButton_4.clicked.connect(self.report_out)

    def ui_changes(self):
        self.tabWidget.tabBar().setVisible(False)
        self.lineEdit_15.setText("0")
        self.tabWidget.setCurrentIndex(0)
        self.setWindowTitle("ATM")
        # labelB.setPixmap(QtGui.QPixmap('python.jpg'))
        self.groupBox_2.setVisible(False)
        self.groupBox_4.setVisible(False)
        self.label_7.setVisible(False)

    def start_qrcode(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        count = 0
        while True:
            global mydata
            sucsess, img = cap.read()
            for barcode in decode(img):
                mydata = barcode.data.decode('utf-8')
                print(mydata)
                count += 1
            if count == 1:
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow('result', img)
            cv2.waitKey(1)
        self.tabWidget.setCurrentIndex(1)

    def choose_tab(self):
        global mydata
        password = self.lineEdit.text()
        self.cur.execute('''
        select card_number from client_data ;
        ''')
        data = self.cur.fetchall()
        if (mydata,) in data:
            self.cur.execute('''
                select password,money from client_data where card_number=%s;
                ''', (mydata,))
            d = self.cur.fetchone()
            if d[0] == password:

                self.tabWidget.setCurrentIndex(2)
                self.label_4.setText(
                    'you have  '+str(d[1])+'  pound in your cridit card')

            else:
                print('not done')
                self.groupBox_2.setVisible(True)
                self.label_3.setStyleSheet("background-color: red")
        else:
            self.cur.execute('''
                    insert into client_data(card_number,password,money)
                    values(%s,%s,0);
                    ''', (mydata, password))
            self.db.commit()
            self.tabWidget.setCurrentIndex(2)
            self.label_4.setText('you have  0  pound in your cridit card')

    def come_out(self):
        self.tabWidget.setCurrentIndex(0)
        self.groupBox_2.setVisible(False)
        self.lineEdit.setText('')

    def money_in(self):
        self.tabWidget.setCurrentIndex(3)

    def money_out(self):
        self.tabWidget.setCurrentIndex(4)

    def money_data(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        count = 0
        while True:
            global mydata
            global l
            sucsess, img = cap.read()
            for barcode in decode(img):
                output = barcode.data.decode('utf-8')
                l.append(int(output))
                self.lineEdit_18.setText(str(sum(l)))
                self.cur.execute('''
                SELECT * FROM atm.atm_data;
                ''')
                atm_data = self.cur.fetchall()
                two_hundred = atm_data[0][1]
                one_hundred = atm_data[0][2]
                fifty = atm_data[0][3]
                twenty = atm_data[0][4]
                ten = atm_data[0][5]
                five = atm_data[0][6]
                if int(output) == 200:
                    self.cur.execute('''
                    update atm.atm_data set two_hund_pound = %s;
                    ''', (two_hundred+1,))
                    self.db.commit()
                elif int(output) == 100:
                    self.cur.execute('''
                    update atm.atm_data set one_hund_pound = %s;
                    ''', (one_hundred+1,))
                    self.db.commit()
                elif int(output) == 50:
                    self.cur.execute('''
                    update atm.atm_data set fifty_pound = %s;
                    ''', (fifty+1,))
                    self.db.commit()
                elif int(output) == 20:
                    self.cur.execute('''
                    update atm.atm_data set twenty_pound = %s;
                    ''', (twenty+1,))
                    self.db.commit()
                elif int(output) == 10:
                    self.cur.execute('''
                    update atm.atm_data set ten_pound = %s;
                    ''', (ten+1,))
                    self.db.commit()
                elif int(output) == 5:
                    self.cur.execute('''
                    update atm.atm_data set five_pound = %s;
                    ''', (five+1,))
                    self.db.commit()

                count += 1
            if count == 1:
                cap.release()
                cv2.destroyAllWindows()
                break
            cv2.imshow('result', img)
            cv2.waitKey(1)

    def ensur_adding_money(self):
        global mydata
        self.cur.execute('''
                select money from client_data where card_number=%s;
                ''', (mydata,))
        dd = self.cur.fetchone()
        newmoney = int(dd[0])+int(self.lineEdit_18.text())

        self.cur.execute('''
        update client_data set money = %s where card_number=%s ;
        ''', (newmoney, mydata))
        self.db.commit()
        self.label_8.setText('Now,you have  '+str(newmoney) +
                             '  pound in your cridit card')
        # time.sleep(5)
        # self.tabWidget.setCurrentIndex(0)

    def report_out(self):
        money_out_data = self.lineEdit_15.text()
        self.cur.execute(''' 
        SELECT money FROM atm.client_data WHERE card_number = %s;
        ''', (mydata,))
        data = self.cur.fetchall()
        d = list(data[0])
        d.insert(0, money_out_data)
        x = tuple(d)
        l = []
        l.append(x)
        last_data = tuple(l)
        wb = Workbook('report.xlsx')
        sheet1 = wb.add_worksheet()
        sheet1.write(0, 0, 'you got : ')
        sheet1.write(0, 1, 'now you have :')
        row_number = 1
        for row in last_data:
            column_number = 0
            for item in row:
                sheet1.write(row_number, column_number, str(item))
                column_number += 1
            row_number += 1
        wb.close()
        # self.statusBar().showMessage('Book Report Created Successfully')

    def get_money(self):
        required_money = int(self.lineEdit_15.text())
        self.cur.execute('''
                SELECT * FROM atm.atm_data;
                ''')
        atm_data = self.cur.fetchall()
        two_hundred = atm_data[0][1]
        one_hundred = atm_data[0][2]
        fifty = atm_data[0][3]
        twenty = atm_data[0][4]
        ten = atm_data[0][5]
        five = atm_data[0][6]
        atm_total_money = two_hundred*200 + one_hundred * \
            100 + fifty*50 + twenty*20 + ten*10+five*5
        self.cur.execute('''
        SELECT money FROM atm.client_data WHERE card_number = %s;
        ''', (mydata,))
        out = self.cur.fetchone()
        if required_money <= out[0]:
            if required_money <= atm_total_money:
                self.groupBox_4.setVisible(True)
                self.label_7.setVisible(True)
                self.cur.execute('''
                update atm.client_data set money = %s where card_number = %s ;
                ''', (out[0]-required_money, mydata))
                v200 = required_money // 200
                v2001 = required_money % 200
                if v200 <= two_hundred:
                    self.cur.execute('''
                            update atm.atm_data set two_hund_pound = %s;
                            ''', (two_hundred-v200,))
                    self.db.commit()
                    v100 = v2001 // 100
                    v1001 = v2001 % 100
                    if v100 <= one_hundred:
                        self.cur.execute('''
                            update atm.atm_data set one_hund_pound = %s;
                            ''', (one_hundred-v100,))
                        self.db.commit()
                        v50 = v1001 // 50
                        v501 = v1001 % 50
                        if v50 <= fifty:
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = %s;
                            ''', (fifty-v50,))
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()

                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()

                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:
                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                        else:
                            required_money = required_money-fifty*50
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = 0;
                            ''')
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:
                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()

                    else:
                        required_money = required_money-one_hundred*100
                        self.cur.execute('''
                            update atm.atm_data set one_hund_pound = 0;
                            ''')
                        self.db.commit()
                        v50 = v1001 // 50
                        v501 = v1001 % 50
                        if v50 <= fifty:
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = %s;
                            ''', (fifty-v50,))
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()

                        else:
                            required_money = required_money-fifty*50
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = 0;
                            ''')
                            self.db.commit()

                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:
                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                else:
                    required_money = required_money-two_hundred*200
                    self.cur.execute('''
                            update atm.atm_data set two_hund_pound = 0;
                            ''')
                    self.db.commit()

                    v100 = v2001 // 100
                    v1001 = v2001 % 100
                    if v100 <= one_hundred:
                        self.cur.execute('''
                            update atm.atm_data set one_hund_pound = %s;
                            ''', (one_hundred-v100,))
                        self.db.commit()
                        v50 = v1001 // 50
                        v501 = v1001 % 50
                        if v50 <= fifty:
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = %s;
                            ''', (fifty-v50,))
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:

                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:

                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:

                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                        else:
                            required_money = required_money-fifty*50
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = 0;
                            ''')
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:
                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                    else:
                        required_money = required_money-one_hundred*100
                        self.cur.execute('''
                            update atm.atm_data set one_hund_pound = 0;
                            ''')
                        self.db.commit()
                        v50 = v1001 // 50
                        v501 = v1001 % 50
                        if v50 <= fifty:
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = %s;
                            ''', (fifty-v50,))
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:
                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                        else:
                            required_money = required_money-fifty*50
                            self.cur.execute('''
                            update atm.atm_data set fifty_pound = 0;
                            ''')
                            self.db.commit()
                            v20 = v501 // 20
                            v201 = v501 % 20
                            if v20 <= twenty:
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = %s;
                                ''', (twenty-v20,))
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                            else:
                                required_money = required_money-twenty*20
                                self.cur.execute('''
                                update atm.atm_data set twenty_pound = 0;
                                ''')
                                self.db.commit()
                                v10 = v201 // 10
                                v101 = v201 % 10
                                if v10 <= ten:
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = %s;
                                    ''', (ten-v10,))
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()

                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
                                else:
                                    required_money = required_money-ten*10
                                    self.cur.execute('''
                                    update atm.atm_data set ten_pound = 0;
                                    ''')
                                    self.db.commit()
                                    v5 = v101 // 5
                                    v51 = v101 % 5
                                    if v5 <= five:
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = %s;
                                        ''', (five-v5,))
                                        self.db.commit()
                                    else:
                                        required_money = required_money-five*5
                                        self.cur.execute('''
                                        update atm.atm_data set five_pound = 0;
                                        ''')
                                        self.db.commit()
            else:

                self.label_7.setText(' Sorry ,no enough money in the ATM .')
        else:

            self.label_7.setText(
                ' Sorry ,no enough money in your credit card .')


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
