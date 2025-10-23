# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(915, 593)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.le_path = QLineEdit(Form)
        self.le_path.setObjectName(u"le_path")

        self.horizontalLayout.addWidget(self.le_path)


        self.horizontalLayout_5.addLayout(self.horizontalLayout)

        self.pb_get_path = QPushButton(Form)
        self.pb_get_path.setObjectName(u"pb_get_path")

        self.horizontalLayout_5.addWidget(self.pb_get_path)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.le_class_num = QLineEdit(Form)
        self.le_class_num.setObjectName(u"le_class_num")

        self.horizontalLayout_2.addWidget(self.le_class_num)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.le_class_name = QTextEdit(Form)
        self.le_class_name.setObjectName(u"le_class_name")

        self.horizontalLayout_3.addWidget(self.le_class_name)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.pb_get_len_names = QPushButton(Form)
        self.pb_get_len_names.setObjectName(u"pb_get_len_names")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_get_len_names.sizePolicy().hasHeightForWidth())
        self.pb_get_len_names.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.pb_get_len_names)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.pb_save = QPushButton(Form)
        self.pb_save.setObjectName(u"pb_save")
        sizePolicy.setHeightForWidth(self.pb_save.sizePolicy().hasHeightForWidth())
        self.pb_save.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pb_save, 1, 0, 1, 4)

        self.lb_show = QLabel(Form)
        self.lb_show.setObjectName(u"lb_show")
        self.lb_show.setWordWrap(True)

        self.gridLayout.addWidget(self.lb_show, 0, 1, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u96c6\u5730\u5740", None))
        self.pb_get_path.setText(QCoreApplication.translate("Form", u"\u4ece\u6587\u4ef6\u5939\u83b7\u53d6", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7c7b\u522b\u6570\u91cf", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u7c7b\u522b\u540d\u79f0", None))
        self.pb_get_len_names.setText(QCoreApplication.translate("Form", u"\u4ece\u6587\u4ef6\u5939\u83b7\u53d6", None))
        self.pb_save.setText(QCoreApplication.translate("Form", u"\u63d0\u4ea4\u5e76\u5199\u5165", None))
        self.lb_show.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

