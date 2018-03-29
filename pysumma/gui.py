from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
#import pyqtgraph as pg

class userinterface(object):

    def __init__(self, Simulation_obj):
        self.S = Simulation_obj

    def setupUi(self, Form):
        Form.setObjectName("pySUMMA 0.1v")

        # define size of pysumma_main window
        Form.resize(1200, 800)
        # define Tab_Widget
        self.tabWidget = QtWidgets.QTabWidget(Form)
        # define size of inside window
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 1100, 750))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        # define Table_Widget
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 20, 1100, 750))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)

        # define Table_Widget
        self.tableWidget.setRowCount(21)

        for i_col in range(0, 21, 1):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i_col, item)

        for i_row in range(0, 3, 1):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i_row, item)
            self.tableWidget.setColumnWidth(0,550)
            self.tableWidget.setColumnWidth(1,350)
            self.tableWidget.setColumnWidth(2,150)

        for i_col_cell in range(0, 21, 1):
            i_row_cell = 0
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(i_col_cell, i_row_cell, item)

            for i_row_cell in range(0, 3, 1):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i_col_cell, i_row_cell, item)


        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.tabWidget.addTab(self.tab, "")

        self.tabWidget.addTab(self.tab_3, "")

        # self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        # self.pushButton_2.setGeometry(QtCore.QRect(950, 680, 75, 23))
        # self.pushButton_2.setObjectName("file_save")
        # self.pushButton_2.clicked.connect(self.edit_filemanager)
        #
        # self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        # self.pushButton_3.setGeometry(QtCore.QRect(680, 460, 75, 23))
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.pushButton_3.clicked.connect(self.edit_Decision)

        # need to change default date & time from Deicision file
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(self.tab_3)
        self.dateTimeEdit.setGeometry(QtCore.QRect(180, 20, 181, 22))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        simulStart_str = self.S.decision_obj.simulStart.value
        simulStart_dt = datetime.datetime.strptime(simulStart_str, "%Y-%m-%d %H:%M")
        simulStart1 = QtCore.QDateTime(simulStart_dt.year,
                                       simulStart_dt.month,
                                       simulStart_dt.day,
                                       simulStart_dt.hour,
                                       simulStart_dt.minute)
        self.dateTimeEdit.setDateTime(simulStart1)


        # need to change default date & time from Deicision file
        self.dateTimeEdit_2 = QtWidgets.QDateTimeEdit(self.tab_3)
        self.dateTimeEdit_2.setGeometry(QtCore.QRect(180, 50, 181, 22))
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        simulFinsh_str = self.S.decision_obj.simulFinsh.value
        simulFinsh_dt = datetime.datetime.strptime(simulFinsh_str, "%Y-%m-%d %H:%M")
        simulFinsh1 = QtCore.QDateTime(simulFinsh_dt.year,
                                       simulFinsh_dt.month,
                                       simulFinsh_dt.day,
                                       simulFinsh_dt.hour,
                                       simulFinsh_dt.minute)
        self.dateTimeEdit_2.setDateTime(simulFinsh1)


        self.comboBox_3 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_3.setGeometry(QtCore.QRect(180, 80, 181, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItems(self.S.decision_obj.soilCatTbl.options)
        self.comboBox_3.setCurrentText(self.S.decision_obj.soilCatTbl.value)

        self.comboBox_4 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_4.setGeometry(QtCore.QRect(180, 110, 181, 22))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItems(self.S.decision_obj.vegeParTbl.options)
        self.comboBox_4.setCurrentText(self.S.decision_obj.vegeParTbl.value)

        self.comboBox_5 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_5.setGeometry(QtCore.QRect(180, 140, 181, 22))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItems(self.S.decision_obj.soilStress.options)
        self.comboBox_5.setCurrentText(self.S.decision_obj.soilStress.value)

        self.comboBox_6 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_6.setGeometry(QtCore.QRect(180, 170, 181, 22))
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItems(self.S.decision_obj.stomResist.options)
        self.comboBox_6.setCurrentText(self.S.decision_obj.stomResist.value)

        self.comboBox_7 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_7.setGeometry(QtCore.QRect(180, 200, 181, 22))
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItems(self.S.decision_obj.num_method.options)
        self.comboBox_7.setCurrentText(self.S.decision_obj.num_method.value)

        self.comboBox_8 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_8.setGeometry(QtCore.QRect(180, 230, 181, 22))
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItems(self.S.decision_obj.fDerivMeth.options)
        self.comboBox_8.setCurrentText(self.S.decision_obj.fDerivMeth.value)

        self.comboBox_9 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_9.setGeometry(QtCore.QRect(180, 260, 181, 22))
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItems(self.S.decision_obj.LAI_method.options)
        self.comboBox_9.setCurrentText(self.S.decision_obj.LAI_method.value)

        self.comboBox_10 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_10.setGeometry(QtCore.QRect(180, 290, 181, 22))
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItems(self.S.decision_obj.f_Richards.options)
        self.comboBox_10.setCurrentText(self.S.decision_obj.f_Richards.value)

        self.comboBox_11 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_11.setGeometry(QtCore.QRect(180, 320, 181, 22))
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_11.addItems(self.S.decision_obj.groundwatr.options)
        self.comboBox_11.setCurrentText(self.S.decision_obj.groundwatr.value)

        self.comboBox_12 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_12.setGeometry(QtCore.QRect(180, 350, 181, 22))
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_12.addItems(self.S.decision_obj.hc_profile.options)
        self.comboBox_12.setCurrentText(self.S.decision_obj.hc_profile.value)

        self.comboBox_13 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_13.setGeometry(QtCore.QRect(180, 380, 181, 22))
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItems(self.S.decision_obj.bcUpprTdyn.options)
        self.comboBox_13.setCurrentText(self.S.decision_obj.bcUpprTdyn.value)

        self.comboBox_14 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_14.setGeometry(QtCore.QRect(180, 410, 181, 22))
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_14.addItems(self.S.decision_obj.bcLowrTdyn.options)
        self.comboBox_14.setCurrentText(self.S.decision_obj.bcLowrTdyn.value)

        self.comboBox_15 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_15.setGeometry(QtCore.QRect(180, 440, 181, 22))
        self.comboBox_15.setObjectName("comboBox_15")
        self.comboBox_15.addItems(self.S.decision_obj.bcUpprSoiH.options)
        self.comboBox_15.setCurrentText(self.S.decision_obj.bcUpprSoiH.value)

        self.comboBox_16 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_16.setGeometry(QtCore.QRect(580, 20, 181, 22))
        self.comboBox_16.setObjectName("comboBox_16")
        self.comboBox_16.addItems(self.S.decision_obj.bcLowrSoiH.options)
        self.comboBox_16.setCurrentText(self.S.decision_obj.bcLowrSoiH.value)

        self.comboBox_17 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_17.setGeometry(QtCore.QRect(580, 50, 181, 22))
        self.comboBox_17.setObjectName("comboBox_17")
        self.comboBox_17.addItems(self.S.decision_obj.veg_traits.options)
        self.comboBox_17.setCurrentText(self.S.decision_obj.veg_traits.value)

        self.comboBox_18 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_18.setGeometry(QtCore.QRect(580, 80, 181, 22))
        self.comboBox_18.setObjectName("comboBox_18")
        self.comboBox_18.addItems(self.S.decision_obj.canopyEmis.options)
        self.comboBox_18.setCurrentText(self.S.decision_obj.canopyEmis.value)

        self.comboBox_19 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_19.setGeometry(QtCore.QRect(580, 110, 181, 22))
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItems(self.S.decision_obj.snowIncept.options)
        self.comboBox_19.setCurrentText(self.S.decision_obj.snowIncept.value)

        self.comboBox_20 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_20.setGeometry(QtCore.QRect(580, 140, 181, 22))
        self.comboBox_20.setObjectName("comboBox_20")
        self.comboBox_20.addItems(self.S.decision_obj.windPrfile.options)
        self.comboBox_20.setCurrentText(self.S.decision_obj.windPrfile.value)

        self.comboBox_21 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_21.setGeometry(QtCore.QRect(580, 170, 181, 22))
        self.comboBox_21.setObjectName("comboBox_21")
        self.comboBox_21.addItems(self.S.decision_obj.astability.options)
        self.comboBox_21.setCurrentText(self.S.decision_obj.astability.value)

        self.comboBox_22 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_22.setGeometry(QtCore.QRect(580, 200, 181, 22))
        self.comboBox_22.setObjectName("comboBox_22")
        self.comboBox_22.addItems(self.S.decision_obj.canopySrad.options)
        self.comboBox_22.setCurrentText(self.S.decision_obj.canopySrad.value)

        self.comboBox_23 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_23.setGeometry(QtCore.QRect(580, 230, 181, 22))
        self.comboBox_23.setObjectName("comboBox_23")
        self.comboBox_23.addItems(self.S.decision_obj.alb_method.options)
        self.comboBox_23.setCurrentText(self.S.decision_obj.alb_method.value)

        self.comboBox_24 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_24.setGeometry(QtCore.QRect(580, 260, 181, 22))
        self.comboBox_24.setObjectName("comboBox_24")
        self.comboBox_24.addItems(self.S.decision_obj.compaction.options)
        self.comboBox_24.setCurrentText(self.S.decision_obj.compaction.value)

        self.comboBox_25 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_25.setGeometry(QtCore.QRect(580, 290, 181, 22))
        self.comboBox_25.setObjectName("comboBox_25")
        self.comboBox_25.addItems(self.S.decision_obj.snowLayers.options)
        self.comboBox_25.setCurrentText(self.S.decision_obj.snowLayers.value)

        self.comboBox_26 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_26.setGeometry(QtCore.QRect(580, 320, 181, 22))
        self.comboBox_26.setObjectName("comboBox_26")
        self.comboBox_26.addItems(self.S.decision_obj.thCondSnow.options)
        self.comboBox_26.setCurrentText(self.S.decision_obj.thCondSnow.value)

        self.comboBox_27 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_27.setGeometry(QtCore.QRect(580, 350, 181, 22))
        self.comboBox_27.setObjectName("comboBox_27")
        self.comboBox_27.addItems(self.S.decision_obj.thCondSoil.options)
        self.comboBox_27.setCurrentText(self.S.decision_obj.thCondSoil.value)

        self.comboBox_43 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_43.setGeometry(QtCore.QRect(580, 380, 181, 22))
        self.comboBox_43.setObjectName("comboBox_43")
        self.comboBox_43.addItems(self.S.decision_obj.spatial_gw.options)
        self.comboBox_43.setCurrentText(self.S.decision_obj.spatial_gw.value)

        self.comboBox_44 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_44.setGeometry(QtCore.QRect(580, 410, 181, 22))
        self.comboBox_44.setObjectName("comboBox_44")
        self.comboBox_44.addItems(self.S.decision_obj.subRouting.options)
        self.comboBox_44.setCurrentText(self.S.decision_obj.subRouting.value)

        self.lineEdit = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 161, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 50, 161, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(410, 20, 161, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 80, 161, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(10, 110, 161, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")

        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(10, 140, 161, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")

        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_7.setGeometry(QtCore.QRect(10, 170, 161, 21))
        self.lineEdit_7.setObjectName("lineEdit_7")

        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_8.setGeometry(QtCore.QRect(10, 200, 161, 21))
        self.lineEdit_8.setObjectName("lineEdit_8")

        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_9.setGeometry(QtCore.QRect(10, 230, 161, 21))
        self.lineEdit_9.setObjectName("lineEdit_9")

        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_10.setGeometry(QtCore.QRect(10, 260, 161, 21))
        self.lineEdit_10.setObjectName("lineEdit_10")

        self.lineEdit_11 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_11.setGeometry(QtCore.QRect(10, 290, 161, 21))
        self.lineEdit_11.setObjectName("lineEdit_11")

        self.lineEdit_12 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_12.setGeometry(QtCore.QRect(10, 320, 161, 21))
        self.lineEdit_12.setObjectName("lineEdit_12")

        self.lineEdit_13 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_13.setGeometry(QtCore.QRect(10, 350, 161, 21))
        self.lineEdit_13.setObjectName("lineEdit_13")

        self.lineEdit_14 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_14.setGeometry(QtCore.QRect(10, 410, 161, 21))
        self.lineEdit_14.setObjectName("lineEdit_14")

        self.lineEdit_15 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_15.setGeometry(QtCore.QRect(10, 380, 161, 21))
        self.lineEdit_15.setObjectName("lineEdit_15")

        self.lineEdit_16 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_16.setGeometry(QtCore.QRect(10, 440, 161, 21))
        self.lineEdit_16.setObjectName("lineEdit_16")

        self.lineEdit_17 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_17.setGeometry(QtCore.QRect(410, 50, 161, 21))
        self.lineEdit_17.setObjectName("lineEdit_17")

        self.lineEdit_35 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_35.setGeometry(QtCore.QRect(410, 290, 161, 21))
        self.lineEdit_35.setObjectName("lineEdit_35")

        self.lineEdit_36 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_36.setGeometry(QtCore.QRect(410, 380, 161, 21))
        self.lineEdit_36.setObjectName("lineEdit_36")

        self.lineEdit_38 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_38.setGeometry(QtCore.QRect(410, 410, 161, 21))
        self.lineEdit_38.setObjectName("lineEdit_38")

        self.lineEdit_39 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_39.setGeometry(QtCore.QRect(410, 320, 161, 21))
        self.lineEdit_39.setObjectName("lineEdit_39")

        self.lineEdit_40 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_40.setGeometry(QtCore.QRect(410, 350, 161, 21))
        self.lineEdit_40.setObjectName("lineEdit_40")

        self.lineEdit_41 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_41.setGeometry(QtCore.QRect(410, 200, 161, 21))
        self.lineEdit_41.setObjectName("lineEdit_41")

        self.lineEdit_42 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_42.setGeometry(QtCore.QRect(410, 260, 161, 21))
        self.lineEdit_42.setObjectName("lineEdit_42")

        self.lineEdit_43 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_43.setGeometry(QtCore.QRect(410, 170, 161, 21))
        self.lineEdit_43.setObjectName("lineEdit_43")

        self.lineEdit_44 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_44.setGeometry(QtCore.QRect(410, 110, 161, 21))
        self.lineEdit_44.setObjectName("lineEdit_44")

        self.lineEdit_45 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_45.setGeometry(QtCore.QRect(410, 230, 161, 21))
        self.lineEdit_45.setObjectName("lineEdit_45")

        self.lineEdit_46 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_46.setGeometry(QtCore.QRect(410, 80, 161, 21))
        self.lineEdit_46.setObjectName("lineEdit_46")

        self.lineEdit_47 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_47.setGeometry(QtCore.QRect(410, 140, 161, 21))
        self.lineEdit_47.setObjectName("lineEdit_47")

        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(950, 680, 75, 23))
        self.pushButton_2.setObjectName("file_save")
        self.pushButton_2.clicked.connect(self.edit_filemanager)

        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_3.setGeometry(QtCore.QRect(680, 460, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.edit_Decision)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("pySUMMA 0.1v", "pySUMMA 0.1v"))

        for i_header in range(0, 21, 1):
            item = self.tableWidget.verticalHeaderItem(i_header)
            item.setText(_translate("Form", ""))

        # self.pushButton.setText(_translate("Form", "Save"))
        self.pushButton_2.setText(_translate("Form", "Save"))
        self.pushButton_3.setText(_translate("Form", "Save"))

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "FilePath"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "FileName"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "LineName"))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)

        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Form", ""))
        item = self.tableWidget.item(0, 0).setBackground(QtGui.QColor(250, 250, 170))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("Form", self.S.fman_ver.filename))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("Form", self.S.fman_ver.name))
        item = self.tableWidget.item(0, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(1, 0)
        item.setText(_translate("Form", self.S.setting_path.filepath))
        item = self.tableWidget.item(1, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(1, 1)
        item.setText(_translate("Form", self.S.setting_path.filename))
        item = self.tableWidget.item(1, 2)
        item.setText(_translate("Form", self.S.setting_path.name))
        item = self.tableWidget.item(1, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(2, 0)
        item.setText(_translate("Form", self.S.input_path.filepath))
        item = self.tableWidget.item(2, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(2, 1)
        item.setText(_translate("Form", self.S.input_path.filename))
        item = self.tableWidget.item(2, 2)
        item.setText(_translate("Form", self.S.input_path.name))
        item = self.tableWidget.item(2, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(3, 0)
        item.setText(_translate("Form", self.S.output_path.filepath))
        item = self.tableWidget.item(3, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(3, 1)
        item.setText(_translate("Form", self.S.output_path.filename))
        item = self.tableWidget.item(3, 2)
        item.setText(_translate("Form", self.S.output_path.name))
        item = self.tableWidget.item(3, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(4, 0)
        item.setText(_translate("Form", self.S.decision_path.filepath))
        item = self.tableWidget.item(4, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(4, 1)
        item.setText(_translate("Form", self.S.decision_path.filename))
        item = self.tableWidget.item(4, 2)
        item.setText(_translate("Form", self.S.decision_path.name))
        item = self.tableWidget.item(4, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(5, 0)
        item.setText(_translate("Form", self.S.meta_time.filepath))
        item = self.tableWidget.item(5, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(5, 1)
        item.setText(_translate("Form", self.S.meta_time.filename))
        item = self.tableWidget.item(5, 2)
        item.setText(_translate("Form", self.S.meta_time.name))
        item = self.tableWidget.item(5, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(6, 0)
        item.setText(_translate("Form", self.S.meta_attr.filepath))
        item = self.tableWidget.item(6, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(6, 1)
        item.setText(_translate("Form", self.S.meta_attr.filename))
        item = self.tableWidget.item(6, 2)
        item.setText(_translate("Form", self.S.meta_attr.name))
        item = self.tableWidget.item(6, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(7, 0)
        item.setText(_translate("Form", self.S.meta_type.filepath))
        item = self.tableWidget.item(7, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(7, 1)
        item.setText(_translate("Form", self.S.meta_type.filename))
        item = self.tableWidget.item(7, 2)
        item.setText(_translate("Form", self.S.meta_type.name))
        item = self.tableWidget.item(7, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(8, 0)
        item.setText(_translate("Form", self.S.meta_force.filepath))
        item = self.tableWidget.item(8, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(8, 1)
        item.setText(_translate("Form", self.S.meta_force.filename))
        item = self.tableWidget.item(8, 2)
        item.setText(_translate("Form", self.S.meta_force.name))
        item = self.tableWidget.item(8, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(9, 0)
        item.setText(_translate("Form", self.S.meta_localpar.filepath))
        item = self.tableWidget.item(9, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(9, 1)
        item.setText(_translate("Form", self.S.meta_localpar.filename))
        item = self.tableWidget.item(9, 2)
        item.setText(_translate("Form", self.S.meta_localpar.name))
        item = self.tableWidget.item(9, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(10, 0)
        item.setText(_translate("Form", self.S.OUTPUT_CONTROL.filepath))
        item = self.tableWidget.item(10, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(10, 1)
        item.setText(_translate("Form", self.S.OUTPUT_CONTROL.filename))
        item = self.tableWidget.item(10, 2)
        item.setText(_translate("Form", self.S.OUTPUT_CONTROL.name))
        item = self.tableWidget.item(10, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(11, 0)
        item.setText(_translate("Form", self.S.meta_index.filepath))
        item = self.tableWidget.item(11, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(11, 1)
        item.setText(_translate("Form", self.S.meta_index.filename))
        item = self.tableWidget.item(11, 2)
        item.setText(_translate("Form", self.S.meta_index.name))
        item = self.tableWidget.item(11, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(12, 0)
        item.setText(_translate("Form", self.S.meta_basinpar.filepath))
        item = self.tableWidget.item(12, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(12, 1)
        item.setText(_translate("Form", self.S.meta_basinpar.filename))
        item = self.tableWidget.item(12, 2)
        item.setText(_translate("Form", self.S.meta_basinpar.name))
        item = self.tableWidget.item(12, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(13, 0)
        item.setText(_translate("Form", self.S.meta_basinvar.filepath))
        item = self.tableWidget.item(13, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(13, 1)
        item.setText(_translate("Form", self.S.meta_basinvar.filename))
        item = self.tableWidget.item(13, 2)
        item.setText(_translate("Form", self.S.meta_basinvar.name))
        item = self.tableWidget.item(13, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(14, 0)
        item.setText(_translate("Form", self.S.local_attr.filepath))
        item = self.tableWidget.item(14, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(14, 1)
        item.setText(_translate("Form", self.S.local_attr.filename))
        item = self.tableWidget.item(14, 2)
        item.setText(_translate("Form", self.S.local_attr.name))
        item = self.tableWidget.item(14, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(15, 0)
        item.setText(_translate("Form", self.S.local_par.filepath))
        item = self.tableWidget.item(15, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(15, 1)
        item.setText(_translate("Form", self.S.local_par.filename))
        item = self.tableWidget.item(15, 2)
        item.setText(_translate("Form", self.S.local_par.name))
        item = self.tableWidget.item(15, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(16, 0)
        item.setText(_translate("Form", self.S.basin_par.filepath))
        item = self.tableWidget.item(16, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(16, 1)
        item.setText(_translate("Form", self.S.basin_par.filename))
        item = self.tableWidget.item(16, 2)
        item.setText(_translate("Form", self.S.basin_par.name))
        item = self.tableWidget.item(16, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(17, 0)
        item.setText(_translate("Form", self.S.forcing_list.filepath))
        item = self.tableWidget.item(17, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(17, 1)
        item.setText(_translate("Form", self.S.forcing_list.filename))
        item = self.tableWidget.item(17, 2)
        item.setText(_translate("Form", self.S.forcing_list.name))
        item = self.tableWidget.item(17, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(18, 0)
        item.setText(_translate("Form", self.S.initial_cond.filepath))
        item = self.tableWidget.item(18, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(18, 1)
        item.setText(_translate("Form", self.S.initial_cond.filename))
        item = self.tableWidget.item(18, 2)
        item.setText(_translate("Form", self.S.initial_cond.name))
        item = self.tableWidget.item(18, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(19, 0)
        item.setText(_translate("Form", self.S.para_trial.filepath))
        item = self.tableWidget.item(19, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(19, 1)
        item.setText(_translate("Form", self.S.para_trial.filename))
        item = self.tableWidget.item(19, 2)
        item.setText(_translate("Form", self.S.para_trial.name))
        item = self.tableWidget.item(19, 2).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(20, 0)
        item.setText(_translate("Form", ""))
        item = self.tableWidget.item(20, 0).setBackground(QtGui.QColor(250, 250, 170))

        item = self.tableWidget.item(20, 1)
        item.setText(_translate("Form", self.S.output_prefix.filename))
        item = self.tableWidget.item(20, 2)
        item.setText(_translate("Form", self.S.output_prefix.name))
        item = self.tableWidget.item(20, 2).setBackground(QtGui.QColor(250, 250, 170))


        self.lineEdit.setText(_translate("Form", "simulStart"))
        self.lineEdit_2.setText(_translate("Form", "simulFinsh"))
        self.lineEdit_3.setText(_translate("Form", "bcLowrSoiH"))
        self.lineEdit_4.setText(_translate("Form", "soilCatTbl"))
        self.lineEdit_5.setText(_translate("Form", "vegeParTbl"))
        self.lineEdit_6.setText(_translate("Form", "soilStress"))
        self.lineEdit_7.setText(_translate("Form", "stomResist"))
        self.lineEdit_8.setText(_translate("Form", "num_method"))
        self.lineEdit_9.setText(_translate("Form", "fDerivMeth"))
        self.lineEdit_10.setText(_translate("Form", "LAI_method"))
        self.lineEdit_11.setText(_translate("Form", "f_Richards"))
        self.lineEdit_12.setText(_translate("Form", "groundwatr"))
        self.lineEdit_13.setText(_translate("Form", "hc_profile"))
        self.lineEdit_14.setText(_translate("Form", "bcLowrTdyn"))
        self.lineEdit_15.setText(_translate("Form", "bcUpprTdyn"))
        self.lineEdit_16.setText(_translate("Form", "bcUpprSoiH"))
        self.lineEdit_17.setText(_translate("Form", "veg_traits"))
        self.lineEdit_35.setText(_translate("Form", "snowLayers"))
        self.lineEdit_36.setText(_translate("Form", "spatial_gw"))
        self.lineEdit_38.setText(_translate("Form", "subRouting"))
        self.lineEdit_39.setText(_translate("Form", "thCondSnow"))
        self.lineEdit_40.setText(_translate("Form", "thCondSoil"))
        self.lineEdit_41.setText(_translate("Form", "canopySrad"))
        self.lineEdit_42.setText(_translate("Form", "compaction"))
        self.lineEdit_43.setText(_translate("Form", "astability"))
        self.lineEdit_44.setText(_translate("Form", "snowIncept"))
        self.lineEdit_45.setText(_translate("Form", "alb_method"))
        self.lineEdit_46.setText(_translate("Form", "canopyEmis"))
        self.lineEdit_47.setText(_translate("Form", "windPrfile"))

        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "File Manager"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Decision File"))

    def edit_Decision(self):

        start = self.dateTimeEdit.dateTime()
        start_dt = start.toPyDateTime()
        start_str = start_dt.strftime("%Y-%m-%d %H:%M")
        self.S.decision_obj.simulStart.value = start_str

        finsh = self.dateTimeEdit_2.dateTime()
        finsh_dt = finsh.toPyDateTime()
        finsh_str = finsh_dt.strftime("%Y-%m-%d %H:%M")
        self.S.decision_obj.simulFinsh.value = finsh_str

        self.S.decision_obj.soilCatTbl.value = self.comboBox_3.currentText()
        self.S.decision_obj.soilCatTbl.value
        self.S.decision_obj.vegeParTbl.value = self.comboBox_4.currentText()
        self.S.decision_obj.vegeParTbl.value
        self.S.decision_obj.soilStress.value = self.comboBox_5.currentText()
        self.S.decision_obj.soilStress.value
        self.S.decision_obj.stomResist.value = self.comboBox_6.currentText()
        self.S.decision_obj.stomResist.value
        self.S.decision_obj.num_method.value = self.comboBox_7.currentText()
        self.S.decision_obj.num_method.value
        self.S.decision_obj.fDerivMeth.value = self.comboBox_8.currentText()
        self.S.decision_obj.fDerivMeth.value
        self.S.decision_obj.LAI_method.value = self.comboBox_9.currentText()
        self.S.decision_obj.LAI_method.value
        self.S.decision_obj.f_Richards.value = self.comboBox_10.currentText()
        self.S.decision_obj.f_Richards.value
        self.S.decision_obj.groundwatr.value = self.comboBox_11.currentText()
        self.S.decision_obj.groundwatr.value
        self.S.decision_obj.hc_profile.value = self.comboBox_12.currentText()
        self.S.decision_obj.hc_profile.value
        self.S.decision_obj.bcUpprTdyn.value = self.comboBox_13.currentText()
        self.S.decision_obj.bcUpprTdyn.value
        self.S.decision_obj.bcLowrTdyn.value = self.comboBox_14.currentText()
        self.S.decision_obj.bcLowrTdyn.value
        self.S.decision_obj.bcUpprSoiH.value = self.comboBox_15.currentText()
        self.S.decision_obj.bcUpprSoiH.value
        self.S.decision_obj.bcLowrSoiH.value = self.comboBox_16.currentText()
        self.S.decision_obj.bcLowrSoiH.value
        self.S.decision_obj.veg_traits.value = self.comboBox_17.currentText()
        self.S.decision_obj.veg_traits.value
        self.S.decision_obj.canopyEmis.value = self.comboBox_18.currentText()
        self.S.decision_obj.canopyEmis.value
        self.S.decision_obj.snowIncept.value = self.comboBox_19.currentText()
        self.S.decision_obj.snowIncept.value
        self.S.decision_obj.windPrfile.value = self.comboBox_20.currentText()
        self.S.decision_obj.windPrfile.value
        self.S.decision_obj.astability.value = self.comboBox_21.currentText()
        self.S.decision_obj.astability.value
        self.S.decision_obj.canopySrad.value = self.comboBox_22.currentText()
        self.S.decision_obj.canopySrad.value
        self.S.decision_obj.alb_method.value = self.comboBox_23.currentText()
        self.S.decision_obj.alb_method.value
        self.S.decision_obj.compaction.value = self.comboBox_24.currentText()
        self.S.decision_obj.compaction.value
        self.S.decision_obj.snowLayers.value = self.comboBox_25.currentText()
        self.S.decision_obj.snowLayers.value
        self.S.decision_obj.thCondSnow.value = self.comboBox_26.currentText()
        self.S.decision_obj.thCondSnow.value
        self.S.decision_obj.thCondSoil.value = self.comboBox_27.currentText()
        self.S.decision_obj.thCondSoil.value
        self.S.decision_obj.spatial_gw.value = self.comboBox_43.currentText()
        self.S.decision_obj.spatial_gw.value
        self.S.decision_obj.subRouting.value = self.comboBox_44.currentText()
        self.S.decision_obj.subRouting.value

    def edit_filemanager(self):
        self.S.fman_ver.filepath = str(self.tableWidget.item(0, 0).text())
        self.S.fman_ver.filename = str(self.tableWidget.item(0, 1).text())
        self.S.setting_path.filepath = str(self.tableWidget.item(1, 0).text())
        self.S.setting_path.filename = str(self.tableWidget.item(1, 1).text())
        self.S.input_path.filepath = str(self.tableWidget.item(2, 0).text())
        self.S.input_path.filename = str(self.tableWidget.item(2, 1).text())
        self.S.output_path.filepath = str(self.tableWidget.item(3, 0).text())
        self.S.output_path.filename = str(self.tableWidget.item(3, 1).text())
        self.S.decision_path.filepath = str(self.tableWidget.item(4, 0).text())
        self.S.decision_path.filename = str(self.tableWidget.item(4, 1).text())
        self.S.meta_time.filepath = str(self.tableWidget.item(5, 0).text())
        self.S.meta_time.filename = str(self.tableWidget.item(5, 1).text())
        self.S.meta_attr.filepath = str(self.tableWidget.item(6, 0).text())
        self.S.meta_attr.filename = str(self.tableWidget.item(6, 1).text())
        self.S.meta_type.filepath = str(self.tableWidget.item(7, 0).text())
        self.S.meta_type.filename = str(self.tableWidget.item(7, 1).text())
        self.S.meta_force.filepath = str(self.tableWidget.item(8, 0).text())
        self.S.meta_force.filename = str(self.tableWidget.item(8, 1).text())
        self.S.meta_localpar.filepath = str(self.tableWidget.item(9, 0).text())
        self.S.meta_localpar.filename = str(self.tableWidget.item(9, 1).text())
        self.S.OUTPUT_CONTROL.filepath = str(self.tableWidget.item(10, 0).text())
        self.S.OUTPUT_CONTROL.filename = str(self.tableWidget.item(10, 1).text())
        self.S.meta_index.filepath = str(self.tableWidget.item(11, 0).text())
        self.S.meta_index.filename = str(self.tableWidget.item(11, 1).text())
        self.S.meta_basinpar.filepath = str(self.tableWidget.item(12, 0).text())
        self.S.meta_basinpar.filename = str(self.tableWidget.item(12, 1).text())
        self.S.meta_basinvar.filepath = str(self.tableWidget.item(13, 0).text())
        self.S.meta_basinvar.filename = str(self.tableWidget.item(13, 1).text())
        self.S.local_attr.filepath = str(self.tableWidget.item(14, 0).text())
        self.S.local_attr.filename = str(self.tableWidget.item(14, 1).text())
        self.S.local_par.filepath = str(self.tableWidget.item(15, 0).text())
        self.S.local_par.filename = str(self.tableWidget.item(15, 1).text())
        self.S.basin_par.filepath = str(self.tableWidget.item(16, 0).text())
        self.S.basin_par.filename = str(self.tableWidget.item(16, 1).text())
        self.S.forcing_list.filepath = str(self.tableWidget.item(17, 0).text())
        self.S.forcing_list.filename = str(self.tableWidget.item(17, 1).text())
        self.S.initial_cond.filepath = str(self.tableWidget.item(18, 0).text())
        self.S.initial_cond.filename = str(self.tableWidget.item(18, 1).text())
        self.S.para_trial.filepath = str(self.tableWidget.item(19, 0).text())
        self.S.para_trial.filename = str(self.tableWidget.item(19, 1).text())
        self.S.output_prefix.filepath = str(self.tableWidget.item(20, 0).text())
        self.S.output_prefix.filename = str(self.tableWidget.item(20, 1).text())