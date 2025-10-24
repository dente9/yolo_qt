# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'display.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 639)
        Form.setMinimumSize(QSize(1000, 600))
        Form.setMaximumSize(QSize(16677215, 16777215))
        self.verticalLayout_6 = QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lb_title = QLabel(Form)
        self.lb_title.setObjectName(u"lb_title")
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.lb_title)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.display = QLabel(Form)
        self.display.setObjectName(u"display")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.display.sizePolicy().hasHeightForWidth())
        self.display.setSizePolicy(sizePolicy)
        self.display.setScaledContents(False)
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.display)

        self.tableWidget = QTableWidget(Form)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(700, 150))
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.tableWidget)

        self.verticalLayout_4.setStretch(0, 3)
        self.verticalLayout_4.setStretch(1, 1)

        self.horizontalLayout_7.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.btn_model_select = QPushButton(self.groupBox)
        self.btn_model_select.setObjectName(u"btn_model_select")
        sizePolicy.setHeightForWidth(self.btn_model_select.sizePolicy().hasHeightForWidth())
        self.btn_model_select.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.btn_model_select)

        self.le_model_path = QLineEdit(self.groupBox)
        self.le_model_path.setObjectName(u"le_model_path")
        sizePolicy.setHeightForWidth(self.le_model_path.sizePolicy().hasHeightForWidth())
        self.le_model_path.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_model_path)

        self.btn_camera = QPushButton(self.groupBox)
        self.btn_camera.setObjectName(u"btn_camera")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_camera.sizePolicy().hasHeightForWidth())
        self.btn_camera.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.btn_camera)

        self.lb_cameracheck = QLabel(self.groupBox)
        self.lb_cameracheck.setObjectName(u"lb_cameracheck")
        sizePolicy2.setHeightForWidth(self.lb_cameracheck.sizePolicy().hasHeightForWidth())
        self.lb_cameracheck.setSizePolicy(sizePolicy2)
        self.lb_cameracheck.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.lb_cameracheck)

        self.btn_open_one_file = QPushButton(self.groupBox)
        self.btn_open_one_file.setObjectName(u"btn_open_one_file")
        sizePolicy2.setHeightForWidth(self.btn_open_one_file.sizePolicy().hasHeightForWidth())
        self.btn_open_one_file.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.btn_open_one_file)

        self.btn_open_dir = QPushButton(self.groupBox)
        self.btn_open_dir.setObjectName(u"btn_open_dir")
        sizePolicy2.setHeightForWidth(self.btn_open_dir.sizePolicy().hasHeightForWidth())
        self.btn_open_dir.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.btn_open_dir)

        self.le_open_one_file = QLineEdit(self.groupBox)
        self.le_open_one_file.setObjectName(u"le_open_one_file")
        sizePolicy.setHeightForWidth(self.le_open_one_file.sizePolicy().hasHeightForWidth())
        self.le_open_one_file.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.le_open_one_file)

        self.le_open_dir = QLineEdit(self.groupBox)
        self.le_open_dir.setObjectName(u"le_open_dir")
        sizePolicy.setHeightForWidth(self.le_open_dir.sizePolicy().hasHeightForWidth())
        self.le_open_dir.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.le_open_dir)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout.addWidget(self.label_14, 7, 2, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.lb_ymax = QLabel(self.groupBox_2)
        self.lb_ymax.setObjectName(u"lb_ymax")

        self.gridLayout.addWidget(self.lb_ymax, 8, 3, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 2, 1, 1)

        self.lb_xmin = QLabel(self.groupBox_2)
        self.lb_xmin.setObjectName(u"lb_xmin")

        self.gridLayout.addWidget(self.lb_xmin, 7, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 5, 2, 1, 1)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 6, 0, 1, 1)

        self.label_47 = QLabel(self.groupBox_2)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout.addWidget(self.label_47, 8, 2, 1, 1)

        self.cb_select_target = QComboBox(self.groupBox_2)
        self.cb_select_target.setObjectName(u"cb_select_target")

        self.gridLayout.addWidget(self.cb_select_target, 4, 1, 1, 3)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.lb_time = QLabel(self.groupBox_2)
        self.lb_time.setObjectName(u"lb_time")

        self.gridLayout.addWidget(self.lb_time, 3, 1, 1, 1)

        self.lb_type = QLabel(self.groupBox_2)
        self.lb_type.setObjectName(u"lb_type")

        self.gridLayout.addWidget(self.lb_type, 5, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 7, 0, 1, 1)

        self.label_29 = QLabel(self.groupBox_2)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout.addWidget(self.label_29, 8, 0, 1, 1)

        self.lb_ymin = QLabel(self.groupBox_2)
        self.lb_ymin.setObjectName(u"lb_ymin")

        self.gridLayout.addWidget(self.lb_ymin, 7, 3, 1, 1)

        self.lb_xmax = QLabel(self.groupBox_2)
        self.lb_xmax.setObjectName(u"lb_xmax")

        self.gridLayout.addWidget(self.lb_xmax, 8, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lb_num = QLabel(self.groupBox_2)
        self.lb_num.setObjectName(u"lb_num")

        self.horizontalLayout_2.addWidget(self.lb_num)


        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 3, 1, 1)

        self.lb_conf = QLabel(self.groupBox_2)
        self.lb_conf.setObjectName(u"lb_conf")

        self.gridLayout.addWidget(self.lb_conf, 5, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btn_clear = QPushButton(self.groupBox_3)
        self.btn_clear.setObjectName(u"btn_clear")

        self.verticalLayout_3.addWidget(self.btn_clear)

        self.btn_save = QPushButton(self.groupBox_3)
        self.btn_save.setObjectName(u"btn_save")

        self.verticalLayout_3.addWidget(self.btn_save)

        self.btn_exit = QPushButton(self.groupBox_3)
        self.btn_exit.setObjectName(u"btn_exit")

        self.verticalLayout_3.addWidget(self.btn_exit)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.verticalLayout_5.setStretch(1, 2)
        self.verticalLayout_5.setStretch(2, 1)

        self.horizontalLayout_7.addLayout(self.verticalLayout_5)

        self.horizontalLayout_7.setStretch(0, 3)
        self.horizontalLayout_7.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lb_title.setText(QCoreApplication.translate("Form", u"\u7cfb\u7edf", None))
        self.display.setText(QCoreApplication.translate("Form", u"display", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u5e8f\u53f7", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u8def\u5f84", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u7c7b\u522b", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"\u7f6e\u4fe1\u5ea6", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"\u5750\u6807\u4f4d\u7f6e", None));
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u4fe1\u606f\u8f93\u5165", None))
        self.btn_model_select.setText(QCoreApplication.translate("Form", u"\u6a21\u578b\u9009\u62e9", None))
        self.btn_camera.setText(QCoreApplication.translate("Form", u"\u542f\u7528/\u5173\u95ed\u6444\u50cf\u5934", None))
        self.lb_cameracheck.setText(QCoreApplication.translate("Form", u"\u6444\u50cf\u5934\u5df2\u5173\u95ed", None))
        self.btn_open_one_file.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u6587\u4ef6", None))
        self.btn_open_dir.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u6587\u4ef6\u5939", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u68c0\u6d4b\u7ed3\u679c", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"ymin", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u76ee\u6807\u9009\u62e9", None))
        self.lb_ymax.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u7c7b\u578b", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u76ee\u6807\u6570\u91cf", None))
        self.lb_xmin.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u7f6e\u4fe1\u5ea6", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u76ee\u6807\u4f4d\u7f6e", None))
        self.label_47.setText(QCoreApplication.translate("Form", u"ymax", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7528\u65f6", None))
        self.lb_time.setText(QCoreApplication.translate("Form", u"0s", None))
        self.lb_type.setText(QCoreApplication.translate("Form", u"type", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"xmin", None))
        self.label_29.setText(QCoreApplication.translate("Form", u"xmax", None))
        self.lb_ymin.setText(QCoreApplication.translate("Form", u"0", None))
        self.lb_xmax.setText(QCoreApplication.translate("Form", u"0", None))
        self.lb_num.setText(QCoreApplication.translate("Form", u"0", None))
        self.lb_conf.setText(QCoreApplication.translate("Form", u"0%", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u64cd\u4f5c", None))
        self.btn_clear.setText(QCoreApplication.translate("Form", u"\u6e05\u9664", None))
        self.btn_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u5386\u53f2\u8bb0\u5f55", None))
        self.btn_exit.setText(QCoreApplication.translate("Form", u"\u9000\u51fa", None))
    # retranslateUi

