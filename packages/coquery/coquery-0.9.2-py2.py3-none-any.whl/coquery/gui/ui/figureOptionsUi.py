# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'figureOptions.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from coquery.gui.pyqt_compat import QtCore, QtGui, frameShadow, frameShape

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FigureOptions(object):
    def setupUi(self, FigureOptions):
        FigureOptions.setObjectName(_fromUtf8("FigureOptions"))
        FigureOptions.resize(476, 538)
        self.gridLayout = QtGui.QGridLayout(FigureOptions)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(FigureOptions)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(FigureOptions)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_labels = QtGui.QWidget()
        self.tab_labels.setObjectName(_fromUtf8("tab_labels"))
        self.formLayout = QtGui.QFormLayout(self.tab_labels)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_5 = QtGui.QLabel(self.tab_labels)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_main = QtGui.QLineEdit(self.tab_labels)
        self.label_main.setObjectName(_fromUtf8("label_main"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.label_main)
        self.label_6 = QtGui.QLabel(self.tab_labels)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_6)
        self.label_x_axis = QtGui.QLineEdit(self.tab_labels)
        self.label_x_axis.setObjectName(_fromUtf8("label_x_axis"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.label_x_axis)
        self.label_7 = QtGui.QLabel(self.tab_labels)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label_y_axis = QtGui.QLineEdit(self.tab_labels)
        self.label_y_axis.setObjectName(_fromUtf8("label_y_axis"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.label_y_axis)
        self.label_8 = QtGui.QLabel(self.tab_labels)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_legend = QtGui.QLineEdit(self.tab_labels)
        self.label_legend.setObjectName(_fromUtf8("label_legend"))
        self.verticalLayout_4.addWidget(self.label_legend)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_13 = QtGui.QLabel(self.tab_labels)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_7.addWidget(self.label_13)
        self.spin_columns = QtGui.QSpinBox(self.tab_labels)
        self.spin_columns.setMinimum(1)
        self.spin_columns.setMaximum(9)
        self.spin_columns.setProperty("value", 1)
        self.spin_columns.setObjectName(_fromUtf8("spin_columns"))
        self.horizontalLayout_7.addWidget(self.spin_columns)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.verticalLayout_4)
        self.tabWidget.addTab(self.tab_labels, _fromUtf8(""))
        self.tab_colors = QtGui.QWidget()
        self.tab_colors.setObjectName(_fromUtf8("tab_colors"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_colors)
        self.verticalLayout_3.setContentsMargins(8, 6, 8, 6)
        self.verticalLayout_3.setSpacing(16)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.frame_2 = QtGui.QFrame(self.tab_colors)
        self.frame_2.setFrameShape(frameShape)
        self.frame_2.setFrameShadow(frameShadow)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_15 = QtGui.QLabel(self.frame_2)
        self.label_15.setWordWrap(True)
        self.label_15.setOpenExternalLinks(True)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.verticalLayout_7.addWidget(self.label_15)
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.radio_qualitative = QtGui.QRadioButton(self.frame_2)
        self.radio_qualitative.setChecked(True)
        self.radio_qualitative.setObjectName(_fromUtf8("radio_qualitative"))
        self.gridLayout_6.addWidget(self.radio_qualitative, 0, 0, 1, 1)
        self.combo_qualitative = QtGui.QComboBox(self.frame_2)
        self.combo_qualitative.setObjectName(_fromUtf8("combo_qualitative"))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.combo_qualitative.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.combo_qualitative, 0, 1, 1, 1)
        self.radio_sequential = QtGui.QRadioButton(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radio_sequential.sizePolicy().hasHeightForWidth())
        self.radio_sequential.setSizePolicy(sizePolicy)
        self.radio_sequential.setObjectName(_fromUtf8("radio_sequential"))
        self.gridLayout_6.addWidget(self.radio_sequential, 1, 0, 1, 1)
        self.combo_sequential = QtGui.QComboBox(self.frame_2)
        self.combo_sequential.setObjectName(_fromUtf8("combo_sequential"))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.combo_sequential.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.combo_sequential, 1, 1, 1, 1)
        self.radio_diverging = QtGui.QRadioButton(self.frame_2)
        self.radio_diverging.setObjectName(_fromUtf8("radio_diverging"))
        self.gridLayout_6.addWidget(self.radio_diverging, 2, 0, 1, 1)
        self.combo_diverging = QtGui.QComboBox(self.frame_2)
        self.combo_diverging.setObjectName(_fromUtf8("combo_diverging"))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.combo_diverging.addItem(_fromUtf8(""))
        self.gridLayout_6.addWidget(self.combo_diverging, 2, 1, 1, 1)
        self.radio_custom = QtGui.QRadioButton(self.frame_2)
        self.radio_custom.setObjectName(_fromUtf8("radio_custom"))
        self.gridLayout_6.addWidget(self.radio_custom, 3, 0, 1, 1)
        self.combo_custom = QtGui.QComboBox(self.frame_2)
        self.combo_custom.setObjectName(_fromUtf8("combo_custom"))
        self.gridLayout_6.addWidget(self.combo_custom, 3, 1, 1, 1)
        self.button_remove_custom = QtGui.QPushButton(self.frame_2)
        self.button_remove_custom.setObjectName(_fromUtf8("button_remove_custom"))
        self.gridLayout_6.addWidget(self.button_remove_custom, 3, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 3, 3, 1, 1)
        self.verticalLayout_7.addLayout(self.gridLayout_6)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(self.tab_colors)
        self.frame.setFrameShape(frameShape)
        self.frame.setFrameShadow(frameShadow)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.spin_number = QtGui.QSpinBox(self.frame)
        self.spin_number.setMinimum(1)
        self.spin_number.setProperty("value", 6)
        self.spin_number.setObjectName(_fromUtf8("spin_number"))
        self.horizontalLayout_6.addWidget(self.spin_number)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame1 = QtGui.QFrame(self.tab_colors)
        self.frame1.setFrameShape(frameShape)
        self.frame1.setFrameShadow(frameShadow)
        self.frame1.setObjectName(_fromUtf8("frame1"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.frame1)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_14 = QtGui.QLabel(self.frame1)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.verticalLayout_5.addWidget(self.label_14)
        self.color_test_area = QtGui.QListWidget(self.frame1)
        self.color_test_area.setDragEnabled(True)
        self.color_test_area.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.color_test_area.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.color_test_area.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.color_test_area.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.color_test_area.setMovement(QtGui.QListView.Snap)
        self.color_test_area.setObjectName(_fromUtf8("color_test_area"))
        self.verticalLayout_5.addWidget(self.color_test_area)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.button_reverse_order = QtGui.QPushButton(self.frame1)
        self.button_reverse_order.setObjectName(_fromUtf8("button_reverse_order"))
        self.horizontalLayout_8.addWidget(self.button_reverse_order)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.verticalLayout_3.addWidget(self.frame1)
        self.frame.raise_()
        self.frame.raise_()
        self.frame_2.raise_()
        self.tabWidget.addTab(self.tab_colors, _fromUtf8(""))
        self.tab_fonts = QtGui.QWidget()
        self.tab_fonts.setObjectName(_fromUtf8("tab_fonts"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_fonts)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.tab_fonts)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 452, 458))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setContentsMargins(-1, -1, -1, 4)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_16 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_9.addWidget(self.label_16)
        self.combo_font_figure = QtGui.QFontComboBox(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo_font_figure.sizePolicy().hasHeightForWidth())
        self.combo_font_figure.setSizePolicy(sizePolicy)
        self.combo_font_figure.setObjectName(_fromUtf8("combo_font_figure"))
        self.horizontalLayout_9.addWidget(self.combo_font_figure)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.group_main = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.group_main.setObjectName(_fromUtf8("group_main"))
        self.gridLayout_2 = QtGui.QGridLayout(self.group_main)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.group_main)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_sample_main = QtGui.QLabel(self.group_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_main.sizePolicy().hasHeightForWidth())
        self.label_sample_main.setSizePolicy(sizePolicy)
        self.label_sample_main.setFrameShape(frameShape)
        self.label_sample_main.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_main.setObjectName(_fromUtf8("label_sample_main"))
        self.horizontalLayout.addWidget(self.label_sample_main)
        self.spin_size_main = QtGui.QSpinBox(self.group_main)
        self.spin_size_main.setMinimum(1)
        self.spin_size_main.setMaximum(96)
        self.spin_size_main.setObjectName(_fromUtf8("spin_size_main"))
        self.horizontalLayout.addWidget(self.spin_size_main)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.group_main)
        self.group_x_axis = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.group_x_axis.setObjectName(_fromUtf8("group_x_axis"))
        self.gridLayout_3 = QtGui.QGridLayout(self.group_x_axis)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.group_x_axis)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_sample_x_axis = QtGui.QLabel(self.group_x_axis)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_x_axis.sizePolicy().hasHeightForWidth())
        self.label_sample_x_axis.setSizePolicy(sizePolicy)
        self.label_sample_x_axis.setFrameShape(frameShape)
        self.label_sample_x_axis.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_x_axis.setObjectName(_fromUtf8("label_sample_x_axis"))
        self.horizontalLayout_2.addWidget(self.label_sample_x_axis)
        self.spin_size_x_axis = QtGui.QSpinBox(self.group_x_axis)
        self.spin_size_x_axis.setMinimum(1)
        self.spin_size_x_axis.setMaximum(96)
        self.spin_size_x_axis.setObjectName(_fromUtf8("spin_size_x_axis"))
        self.horizontalLayout_2.addWidget(self.spin_size_x_axis)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.group_x_axis)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_sample_x_ticks = QtGui.QLabel(self.group_x_axis)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_x_ticks.sizePolicy().hasHeightForWidth())
        self.label_sample_x_ticks.setSizePolicy(sizePolicy)
        self.label_sample_x_ticks.setFrameShape(frameShape)
        self.label_sample_x_ticks.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_x_ticks.setObjectName(_fromUtf8("label_sample_x_ticks"))
        self.horizontalLayout_4.addWidget(self.label_sample_x_ticks)
        self.spin_size_x_ticks = QtGui.QSpinBox(self.group_x_axis)
        self.spin_size_x_ticks.setMinimum(1)
        self.spin_size_x_ticks.setMaximum(96)
        self.spin_size_x_ticks.setObjectName(_fromUtf8("spin_size_x_ticks"))
        self.horizontalLayout_4.addWidget(self.spin_size_x_ticks)
        self.gridLayout_3.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.group_x_axis)
        self.group_y_axis = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.group_y_axis.setObjectName(_fromUtf8("group_y_axis"))
        self.gridLayout_4 = QtGui.QGridLayout(self.group_y_axis)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_9 = QtGui.QLabel(self.group_y_axis)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_sample_y_axis = QtGui.QLabel(self.group_y_axis)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_y_axis.sizePolicy().hasHeightForWidth())
        self.label_sample_y_axis.setSizePolicy(sizePolicy)
        self.label_sample_y_axis.setFrameShape(frameShape)
        self.label_sample_y_axis.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_y_axis.setObjectName(_fromUtf8("label_sample_y_axis"))
        self.horizontalLayout_3.addWidget(self.label_sample_y_axis)
        self.spin_size_y_axis = QtGui.QSpinBox(self.group_y_axis)
        self.spin_size_y_axis.setMinimum(1)
        self.spin_size_y_axis.setMaximum(96)
        self.spin_size_y_axis.setObjectName(_fromUtf8("spin_size_y_axis"))
        self.horizontalLayout_3.addWidget(self.spin_size_y_axis)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.label_10 = QtGui.QLabel(self.group_y_axis)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_4.addWidget(self.label_10, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_sample_y_ticks = QtGui.QLabel(self.group_y_axis)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_y_ticks.sizePolicy().hasHeightForWidth())
        self.label_sample_y_ticks.setSizePolicy(sizePolicy)
        self.label_sample_y_ticks.setFrameShape(frameShape)
        self.label_sample_y_ticks.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_y_ticks.setObjectName(_fromUtf8("label_sample_y_ticks"))
        self.horizontalLayout_5.addWidget(self.label_sample_y_ticks)
        self.spin_size_y_ticks = QtGui.QSpinBox(self.group_y_axis)
        self.spin_size_y_ticks.setMinimum(1)
        self.spin_size_y_ticks.setMaximum(96)
        self.spin_size_y_ticks.setObjectName(_fromUtf8("spin_size_y_ticks"))
        self.horizontalLayout_5.addWidget(self.spin_size_y_ticks)
        self.gridLayout_4.addLayout(self.horizontalLayout_5, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.group_y_axis)
        self.group_legend = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.group_legend.setObjectName(_fromUtf8("group_legend"))
        self.gridLayout_5 = QtGui.QGridLayout(self.group_legend)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_11 = QtGui.QLabel(self.group_legend)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_sample_legend = QtGui.QLabel(self.group_legend)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_legend.sizePolicy().hasHeightForWidth())
        self.label_sample_legend.setSizePolicy(sizePolicy)
        self.label_sample_legend.setFrameShape(frameShape)
        self.label_sample_legend.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_legend.setObjectName(_fromUtf8("label_sample_legend"))
        self.horizontalLayout_12.addWidget(self.label_sample_legend)
        self.spin_size_legend = QtGui.QSpinBox(self.group_legend)
        self.spin_size_legend.setMinimum(1)
        self.spin_size_legend.setMaximum(96)
        self.spin_size_legend.setObjectName(_fromUtf8("spin_size_legend"))
        self.horizontalLayout_12.addWidget(self.spin_size_legend)
        self.gridLayout_5.addLayout(self.horizontalLayout_12, 0, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.group_legend)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_5.addWidget(self.label_12, 1, 0, 1, 1)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.label_sample_legend_entries = QtGui.QLabel(self.group_legend)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_sample_legend_entries.sizePolicy().hasHeightForWidth())
        self.label_sample_legend_entries.setSizePolicy(sizePolicy)
        self.label_sample_legend_entries.setFrameShape(frameShape)
        self.label_sample_legend_entries.setFrameShadow(QtGui.QFrame.Sunken)
        self.label_sample_legend_entries.setObjectName(_fromUtf8("label_sample_legend_entries"))
        self.horizontalLayout_13.addWidget(self.label_sample_legend_entries)
        self.spin_size_legend_entries = QtGui.QSpinBox(self.group_legend)
        self.spin_size_legend_entries.setMinimum(1)
        self.spin_size_legend_entries.setMaximum(96)
        self.spin_size_legend_entries.setObjectName(_fromUtf8("spin_size_legend_entries"))
        self.horizontalLayout_13.addWidget(self.spin_size_legend_entries)
        self.gridLayout_5.addLayout(self.horizontalLayout_13, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.group_legend)
        spacerItem4 = QtGui.QSpacerItem(20, 220, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.tabWidget.addTab(self.tab_fonts, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.label_16.setBuddy(self.combo_font_figure)

        self.retranslateUi(FigureOptions)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FigureOptions.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FigureOptions.reject)
        QtCore.QMetaObject.connectSlotsByName(FigureOptions)

    def retranslateUi(self, FigureOptions):
        FigureOptions.setWindowTitle(_translate("FigureOptions", "Figure options – Coquery", None))
        self.label_5.setText(_translate("FigureOptions", "Main", None))
        self.label_6.setText(_translate("FigureOptions", "X axis", None))
        self.label_7.setText(_translate("FigureOptions", "Y axis", None))
        self.label_8.setText(_translate("FigureOptions", "Legend", None))
        self.label_13.setText(_translate("FigureOptions", "Number of columns in legend:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_labels), _translate("FigureOptions", "Labels", None))
        self.label_15.setText(_translate("FigureOptions", "<html><head/><body><p>Choose palette:<br/>(see <a href=\"http://colorbrewer2.org\"><span style=\" text-decoration: underline; color:#006e28;\">http://colorbrewer2.org</span></a> for a demonstration)</p></body></html>", None))
        self.radio_qualitative.setText(_translate("FigureOptions", "Qualitative", None))
        self.combo_qualitative.setItemText(0, _translate("FigureOptions", "Set1", None))
        self.combo_qualitative.setItemText(1, _translate("FigureOptions", "Set2", None))
        self.combo_qualitative.setItemText(2, _translate("FigureOptions", "Set3", None))
        self.combo_qualitative.setItemText(3, _translate("FigureOptions", "Paired", None))
        self.combo_qualitative.setItemText(4, _translate("FigureOptions", "Accent", None))
        self.combo_qualitative.setItemText(5, _translate("FigureOptions", "Pastel1", None))
        self.combo_qualitative.setItemText(6, _translate("FigureOptions", "Pastel2", None))
        self.combo_qualitative.setItemText(7, _translate("FigureOptions", "Dark2", None))
        self.radio_sequential.setText(_translate("FigureOptions", "Sequential", None))
        self.combo_sequential.setItemText(0, _translate("FigureOptions", "Greys", None))
        self.combo_sequential.setItemText(1, _translate("FigureOptions", "Reds", None))
        self.combo_sequential.setItemText(2, _translate("FigureOptions", "Greens", None))
        self.combo_sequential.setItemText(3, _translate("FigureOptions", "Blues", None))
        self.combo_sequential.setItemText(4, _translate("FigureOptions", "Oranges", None))
        self.combo_sequential.setItemText(5, _translate("FigureOptions", "Purples", None))
        self.combo_sequential.setItemText(6, _translate("FigureOptions", "BuGn", None))
        self.combo_sequential.setItemText(7, _translate("FigureOptions", "BuPu", None))
        self.combo_sequential.setItemText(8, _translate("FigureOptions", "GnBu", None))
        self.combo_sequential.setItemText(9, _translate("FigureOptions", "OrRd", None))
        self.combo_sequential.setItemText(10, _translate("FigureOptions", "PuBu", None))
        self.combo_sequential.setItemText(11, _translate("FigureOptions", "PuRd", None))
        self.combo_sequential.setItemText(12, _translate("FigureOptions", "RdPu", None))
        self.combo_sequential.setItemText(13, _translate("FigureOptions", "YlGn", None))
        self.combo_sequential.setItemText(14, _translate("FigureOptions", "PuBuGn", None))
        self.combo_sequential.setItemText(15, _translate("FigureOptions", "YlGnBu", None))
        self.combo_sequential.setItemText(16, _translate("FigureOptions", "YlOrBr", None))
        self.combo_sequential.setItemText(17, _translate("FigureOptions", "YlOrRd", None))
        self.radio_diverging.setText(_translate("FigureOptions", "Diverging", None))
        self.combo_diverging.setItemText(0, _translate("FigureOptions", "RdBu", None))
        self.combo_diverging.setItemText(1, _translate("FigureOptions", "RdGy", None))
        self.combo_diverging.setItemText(2, _translate("FigureOptions", "PRGn", None))
        self.combo_diverging.setItemText(3, _translate("FigureOptions", "PiYG", None))
        self.combo_diverging.setItemText(4, _translate("FigureOptions", "BrBG", None))
        self.combo_diverging.setItemText(5, _translate("FigureOptions", "RdYlBu", None))
        self.combo_diverging.setItemText(6, _translate("FigureOptions", "RdYlGn", None))
        self.combo_diverging.setItemText(7, _translate("FigureOptions", "Spectral", None))
        self.radio_custom.setText(_translate("FigureOptions", "Custom", None))
        self.button_remove_custom.setText(_translate("FigureOptions", "Remove", None))
        self.label_4.setText(_translate("FigureOptions", "Number of colors:", None))
        self.label_14.setText(_translate("FigureOptions", "Click to modify color, drag to change order:", None))
        self.button_reverse_order.setText(_translate("FigureOptions", "Reverse order", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_colors), _translate("FigureOptions", "Colors", None))
        self.label_16.setText(_translate("FigureOptions", "&Figure font:", None))
        self.group_main.setTitle(_translate("FigureOptions", "Main", None))
        self.label.setText(_translate("FigureOptions", "Label", None))
        self.label_sample_main.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_main.setSuffix(_translate("FigureOptions", " pt", None))
        self.group_x_axis.setTitle(_translate("FigureOptions", "X axis", None))
        self.label_2.setText(_translate("FigureOptions", "Label", None))
        self.label_sample_x_axis.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_x_axis.setSuffix(_translate("FigureOptions", " pt", None))
        self.label_3.setText(_translate("FigureOptions", "Ticks", None))
        self.label_sample_x_ticks.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_x_ticks.setSuffix(_translate("FigureOptions", " pt", None))
        self.group_y_axis.setTitle(_translate("FigureOptions", "Y axis", None))
        self.label_9.setText(_translate("FigureOptions", "Label", None))
        self.label_sample_y_axis.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_y_axis.setSuffix(_translate("FigureOptions", " pt", None))
        self.label_10.setText(_translate("FigureOptions", "Ticks", None))
        self.label_sample_y_ticks.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_y_ticks.setSuffix(_translate("FigureOptions", " pt", None))
        self.group_legend.setTitle(_translate("FigureOptions", "Legend", None))
        self.label_11.setText(_translate("FigureOptions", "Label", None))
        self.label_sample_legend.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_legend.setSuffix(_translate("FigureOptions", " pt", None))
        self.label_12.setText(_translate("FigureOptions", "Entries", None))
        self.label_sample_legend_entries.setText(_translate("FigureOptions", "Default font", None))
        self.spin_size_legend_entries.setSuffix(_translate("FigureOptions", " pt", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fonts), _translate("FigureOptions", "Fonts", None))


