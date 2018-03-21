#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
ZetCode Advanced PyQt5 tutorial 

This program animates the size of a
widget with QPropertyAnimation.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
'''

from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QPushButton, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtCore import QRect, QPropertyAnimation, Qt
import sys


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setStyleSheet('''

            * {
    background: black;
    color: #DDDDDD;
    border: 1px solid #5A5A5A;
}

/* Nice Windows-XP-style password character. */
QLineEdit[echoMode="2"] {
    lineedit-password-character: 9679;
}

/* We provide a min-width and min-height for push buttons
   so that they look elegant regardless of the width of the text. */
QPushButton {
    background-color: #191919;
    border-width: 2px;
    border-color: #5A5A5A;
    border-style: solid;
    border-radius: 5;
    padding: 3px;
    min-width: 9ex;
    min-height: 2.5ex;
}

QPushButton:hover {
   background-color: #353535;
}

/* Increase the padding, so the text is shifted when the button is
   pressed. */
QPushButton:pressed {
    padding-left: 5px;
    padding-top: 5px;
    background-color: #3D7848;
}

/* Mark mandatory fields with a brownish color. */
.mandatory {
    color: brown;
}

/* Bold text on status bar looks awful. */
QStatusBar QLabel {
   font: normal;
}

QStatusBar::item {
    border-width: 1;
    border-color: darkkhaki;
    border-style: solid;
    border-radius: 2;
}

QComboBox, QLineEdit, QSpinBox, QTextEdit, QListView {
    background-color: cornsilk;
    selection-color: #0a214c; 
    selection-background-color: #C19A6B;
}

QListView {
    show-decoration-selected: 1;
}

QListView::item:hover {
    background-color: wheat;
}

/* We reserve 1 pixel space in padding. When we get the focus,
   we kill the padding and enlarge the border. This makes the items
   glow. */
QLineEdit, QFrame {
    border-width: 2px;
    padding: 1px;
    border-style: solid;
    border-color: darkkhaki;
    border-radius: 5px;
}

/* As mentioned above, eliminate the padding and increase the border. */
QLineEdit:focus, QFrame:focus {
    border-width: 3px;
    padding: 0px;
}

/* A QToolTip is a QLabel ... */
QToolTip {
    border: 2px solid darkkhaki;
    padding: 5px;
    border-radius: 3px;
    opacity: 200;
}

/* Nice to have the background color change when hovered. */
QRadioButton:hover, QCheckBox:hover {
    background-color: wheat;
}

/* Force the dialog's buttons to follow the Windows guidelines. */
QDialogButtonBox {
    button-layout: 0;
}

QFrame {
    background: rgba(25,25,25,0.3);
    border-color: #5A5A5A;
    border-width: 1px;
    border-radius: 5px;
}


/* A QLabel is a QFrame ... */
QLabel {
    border: none;
    padding: 0;
    font-family : Tahoma;
}

QFrame>QLayout{
    border: none;
    padding: 0;
    margin: 0;
    background: none;
    
}

QScrollArea{
    border: none;
    padding: 0;
    margin: 0;
    background: rgba(25,25,25,0);
    
}

QScrollArea>QWidget {
    background: none;
    border: none;
    padding: 0;
    margin: 0;
}

QVBoxLayout {
    background: red;
    border: none;
}

QFrame>QLayout {
    background: none;
    border: 1px;
    padding: 0;
    margin: 0;
}

QScrollBar:vertical {

  border-color: #5A5A5A;
  border-width: 1px;
  border-style: solid;
  border-radius: 7px;


  background: #191919;
  width: 14px;
  margin: 5px 0 5px 0;
}

QScrollBar::handle:vertical {
    
  border-color: #5A5A5A;
  border-width: 1px;
  border-style: solid;
  border-radius: 6px;

  background: #353535;
  min-height: 30px;
}

QScrollBar::add-line:vertical {
    border: none;
    background-color: none;
    height: 0px;
}


QScrollBar::handle:hover {
   background-color: white;
}

QScrollBar::handle:pressed {
    background-color: #3D7848;
}

QScrollBar::sub-line:vertical {
    border: none;
    background-color: none;
    height: 0px;
}

QScrollBar:horizontal {

  border-color: #5A5A5A;
  border-width: 1px;
  border-style: solid;
  border-radius: 7px;


  background: #191919;
  height: 14px;
  margin: 0 5px 0 5px;
}

QScrollBar::handle:horizontal {
    
  border-color: #5A5A5A;
  border-width: 1px;
  border-style: solid;
  border-radius: 6px;

  background: #353535;
  min-width: 30px;
}

QScrollBar::add-line:horizontal {
    border: none;
    background-color: none;
    width: 0px;
}

QScrollBar::sub-line:horizontal {
    border: none;
    background-color: none;
    width: 0px;
}
            ''')

        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.doAnim)
        self.button.move(30, 30)

        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setGeometry(150, 30, 400, 200)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(False)

        w = QWidget(scroll)
        grid = QVBoxLayout(w)

        for i in range(1, 100):
            grid.addWidget(QLabel('asdfgsadfsdfsdfg   '))

        w.setLayout(grid)
        grid.setParent(w)

        scroll.setWidget(w)
        w.setParent(scroll)

        # Scroll Area Layer add
        vLayout = QVBoxLayout()
        vLayout.addWidget(scroll)

        self.frame.setLayout(vLayout)

        self.l = QLabel('abc', self)
        self.l.setGeometry(150, 300, 400, 200)

        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Animation')
        self.show()

    def doAnim(self):

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(150, 500, 400, 0))
        self.anim.setEndValue(QRect(150, 500, 400, 200))
        self.anim.start()

if __name__ == "__main__":

    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec_()
