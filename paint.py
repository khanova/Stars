import colorsys
import math
import sys
import parse
from contextlib import suppress
from geometry import Point
from global_vars import colors, labels, MSecsSinceEpoh
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QDateTimeEdit, QLineEdit)
from PyQt5.QtGui import (QPainter, QColor, QBrush,
                         QStaticText, QFont, QRadialGradient,
                         QFontMetrics, QDoubleValidator)
from PyQt5.QtCore import Qt, QBasicTimer, QPropertyAnimation, QRect, QDateTime

positions = []


class MyValidator(QDoubleValidator):

    def __init__(self, top, bottom=0):
        super().__init__(top, bottom, 4)
        self.top = top
        self.bottom = bottom

    def validate(self, input, pos):
        input = ''.join(list(map(lambda x: '0' if x == ' ' else x, input)))
        angle = parse.convert_str_to_angle(input)
        print(input, angle, self.top < angle or angle < self.bottom)
        if angle is None or self.top < angle or angle < self.bottom:
            return 0, input, pos

        return 2, input, pos


class GardientBrush(QBrush):

    def __init__(self, x, y, c, r, pos):
        radialGradient = QRadialGradient(x, y, r)
        radialGradient.setColorAt(0.0, Qt.white)
        radialGradient.setColorAt(pos, c)
        radialGradient.setColorAt(1, QColor(0, 0, 0, 0))
        super().__init__(radialGradient)


class MyPainter(QPainter):
    font = QFont()

    def __init__(self):
        super().__init__()

        self.font.setPointSize(13)
        self.font.setItalic(True)

    def drawStar(self, x, y, c, r, pos):
        self.setBrush(GardientBrush(x, y, c, r, pos))
        self.setPen(QColor(0, 0, 0, 0))
        self.drawEllipse(x - r, y - r, 2 * r, 2 * r)

    def drawLetter(self, x, y, c, let):
        self.setFont(self.font)
        self.setPen(c)
        self.drawStaticText(x, y, QStaticText(let))


class MyForm(QMainWindow):
    zoom = 0
    pos = None
    constellation = None
    step = 0
    rotation = False
    coordChange = False

    def __init__(self, sky):
        super().__init__()

        self.sky = sky
        self.initUI()

    def initUI(self):
        self.setStyleSheet(
            '''
            .QDateTimeEdit, .QLineEdit {
            background: rgbs(0, 0, 0, 0.5);
            color: #DDDDDD;
            border: 1px solid #5A5A5A;
            border-radius: 5;
            selection-color: #0a214c; 
            selection-background-color: #C19A6B;}
            ''')

        self.initEditors()
        self.setFocusPolicy(Qt.ClickFocus)
        self.setGeometry(300, 300, self.sky.width, self.sky.height)
        self.setWindowTitle('Starry Sky')
        self.timer = QBasicTimer()
        self.timer.start(50, self)
        self.show()

    def initEditors(self):
        self.datetime = QDateTimeEdit(self)
        self.datetime.setFocusPolicy(Qt.ClickFocus)
        self.datetime.setGeometry(30, 10, 138, 30)
        self.datetime.setDisplayFormat('dd.MM.yyyy HH:mm')
        self.datetime.setMaximumDateTime(QDateTime.fromString(
            '31.12.2099 23:59:59', 'dd.MM.yyyy HH:mm'))
        self.datetime.setMinimumDateTime(QDateTime.fromString(
            '01.01.2000 00:00:00', 'dd.MM.yyyy HH:mm'))
        self.datetime.setDateTime(QDateTime.currentDateTime().toUTC())
        self.datetime.dateTimeChanged.connect(self.dateTimeChanged)
        self.dateTimeChanged(self.datetime.dateTime())

        self.coordTheta = QLineEdit(self)
        self.coordTheta.setFocusPolicy(Qt.ClickFocus)
        self.coordTheta.setGeometry(10, 50, 85, 30)
        self.coordTheta.setInputMask('#00°00\'00"')
        self.coordTheta.setText('+90°00\'00"')
        self.coordTheta.setValidator(MyValidator(90, -90))
        self.coordTheta.textChanged.connect(self.coordChanged)

        self.coordPhi = QLineEdit(self)
        self.coordPhi.setFocusPolicy(Qt.ClickFocus)
        self.coordPhi.setGeometry(100, 50, 85, 30)
        self.coordPhi.setInputMask('000°00\'00"')
        self.coordPhi.setText('000°00\'00"')
        self.coordPhi.setValidator(MyValidator(360))
        self.coordPhi.textChanged.connect(self.coordChanged)

    def coordChanged(self, event):
        if self.coordChanged:
            self.coordChanged = False
            return
        self.sky.change_direction(
            str(self.coordTheta.text()), str(self.coordPhi.text()))
        self.repaint()

    def dateTimeChanged(self, event):
        self.sky.set_angle(event.toMSecsSinceEpoch() -
                           MSecsSinceEpoh + event.offsetFromUtc() * 1000)

    def timerEvent(self, e):
        self.step += 1
        if self.rotation:
            self.sky.inc_angle()
            self.datetime.setDateTime(self.datetime.dateTime().addMSecs(45000))
        self.repaint()

    def paintEvent(self, e):
        qp = MyPainter()
        qp.begin(self)
        qp.setBrush(QBrush(Qt.SolidPattern))
        qp.drawRect(0, 0, self.size().width(), self.size().height())
        self.drawPoints(qp)
        self.drawLabels(qp)
        qp.end()

    def drawPoints(self, qp):
        for star in self.sky.get_stars():
            color = QColor(*colors[star.color])
            pos = self.get_gradient_position(star)
            if star.constellation == self.constellation:
                qp.drawStar(star.x, star.y, color, star.r + 3, pos)
                if star.letter:
                    qp.drawLetter(star.x, star.y, color, star.letter)
            else:
                qp.drawStar(star.x, star.y, color, star.r, pos)

    def drawLabels(self, qp):
        if self.sky.in_pole():
            return
        qp.setPen(QColor(255, 255, 255))
        for coord, label in zip(self.sky.get_labels(), labels):
            qp.drawText(coord.x, coord.y, label)

    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y()
        self.sky.zoom(self.zoom)
        self.repaint()

    def refresh_coord(self, theta, phi):
        self.coordChanged = True
        self.coordTheta.setText(self.to_text(theta))
        self.coordChanged = True
        self.coordPhi.setText(self.to_text(phi))

    def to_text(self, angle):
        integer = int(angle)
        angle %= 1
        angle *= 60
        minute = int(angle)
        angle %= 1
        angle *= 60
        secunde = int(angle)
        return '{0:03d}°{1:02d}\'{2:02d}\'\''.format(integer, minute, secunde)

    def get_gradient_position(self, star):
        return positions[int(star.m * 100 + self.step) % len(positions)]

    def get_delta_in_fract(self, pos):
        size = self.size()
        delta = self.pos - pos
        return delta.x() / size.width(), delta.y() / size.height()

    def resizeEvent(self, event):
        self.sky.resize(Point(self.size().width(), self.size().height()))
        self.repaint()

    def mousePressEvent(self, event):
        self.pos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            self.sky.rotate_screen(
                *map(Point.create_from_QPoint, (event.pos(), self.pos)))
        elif event.buttons() == Qt.LeftButton:
            phi, theta = self.sky.rotate_camera(
                *self.get_delta_in_fract(event.pos()))
            self.refresh_coord(phi, theta)
        else:
            return
        self.pos = event.pos()
        self.repaint()

    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            star = self.sky.get_nearest_star(
                Point.create_from_QPoint(event.pos()))
            if star:
                self.constellation = star.constellation
            else:
                self.constellation = None
        self.repaint()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_P:
            self.rotation ^= 1
            return
        if event.key() == Qt.Key_Escape:
            self.constellation = None
            return
        if event.key() == Qt.Key_Left:
            phi, theta = self.sky.rotate_camera(-0.1, 0)
        if event.key() == Qt.Key_Right:
            phi, theta = self.sky.rotate_camera(0.1, 0)
        if event.key() == Qt.Key_Up:
            phi, theta = self.sky.rotate_camera(0, -0.1)
        if event.key() == Qt.Key_Down:
            phi, theta = self.sky.rotate_camera(0, 0.1)
        with suppress(UnboundLocalError):
            self.refresh_coord(phi, theta)


def init_global_vars():
    for i in range(0, 98, 2):
        positions.append(i / 100)
    for i in range(98, 0, -2):
        positions.append(i / 100)


def paint(sky):
    init_global_vars()
    app = QApplication(sys.argv)
    form = MyForm(sky)
    sys.exit(app.exec_())


def add_parser(subparsers):
    parser_learn = subparsers.add_parser(
        'paint',
        help='Visualisation of the sky'
    )
    parser_learn.set_defaults(func=lambda sky, options: paint(sky))
