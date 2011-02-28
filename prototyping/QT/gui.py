from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import random

class Block(QWidget):
	def __init__(self, parent, rect):
		QWidget.__init__(self, parent)
		self._brush = QBrush(QColor(random.randint(128, 255), 
			random.randint(128, 255), random.randint(128, 255)))
		self._rect = rect
		self.resize(rect.size())

	def paintEvent(self, e):
		p = QPainter(self)
		p.setBrush(self._brush)
		p.drawRect(e.rect())

class Container(Block):
	_data = None
	_order = None

	def __init__(self, parent, rect, type):
		Block.__init__(self, parent, rect)
		self._type = type
		self._data = {}
		self._order = []

	def __getitem__(self, name):
		return self._data[name]

	def __setitem__(self, name, block):
		self._data[name] = block
		if name not in self._order:
			# by default add to the end...
			self._order += [name]
		self.reorder()

	def __delitem__(self, name):
		self._data.destroy()
		del self._data[name]
		self._order.remove(name)
		self.reorder()

	def paintEvent(self, e):
		if len(self._data) == 0:
			Block.paintEvent(self, e)

	def reorder(self):
		type = self._type
		if type == "Free":
			return
		x = 0
		y = 0
		for bname in self._order:
			geometry = self._data[bname].geometry()
			self._data[bname].move(x, y)
			if type == "Horizontal":
				x += geometry.width()
				print "Horizontal"
			if type == "Vertical":
				y += geometry.height()
				print "Vertical"

class GuiForm(Container):
	def __init__(self):
		Container.__init__(self, None, QRect(0, 0, 500, 500), "Free")
		self["Container 1"] = Container(self, QRect(0, 0, 450, 450),
				"Vertical")
		self["Container 1"]["Container 1-1"] = Container(self["Container 1"],
				QRect(0, 0, 450, 150), "Horizontal")
		self["Container 1"]["Container 1-1"]["Block 1"] = Block(
				self["Container 1"]["Container 1-1"], QRect(0, 0, 150, 100))
		self["Container 1"]["Container 1-1"]["Block 2"] = Block(
				self["Container 1"]["Container 1-1"], QRect(0, 0, 150, 150))
		self["Container 1"]["Container 1-1"]["Block 3"] = Block(
				self["Container 1"]["Container 1-1"], QRect(0, 0, 100, 50))
		self["Container 1"]["Container 1-2"] = Container(self["Container 1"],
				QRect(0, 0, 250, 100), "Horizontal")
		self["Container 1"]["Container 1-2"]["Block 4"] = Block(
				self["Container 1"]["Container 1-2"], QRect(0, 0, 250, 100))
		self["Container 1"]["Container 1-3"] = Container(self["Container 1"],
				QRect(0, 0, 350, 75), "Horizontal")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = GuiForm()
	w.show()
	sys.exit(app.exec_())
