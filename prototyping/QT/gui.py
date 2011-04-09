

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import random


class Size:
	def __init__(self):
		self._minWidth = 0
		self._minHeight = 0
		self._maxWidth = 0
		self._maxHeight = 0
		self._prefWidth = 0
		self._prefHeight = 0
	def __init__(self, minWidth, minHeight, maxWidth, maxHeight, 
			prefWidth, prefHeight):
		self._minWidth = minWidth
		self._minHeight = minHeight
		self._maxWidth = maxWidth
		self._maxHeight = maxHeight
		self._prefWidth = prefWidth
		self._prefHeight = prefHeight
	def setMinSize(self, width, height):
		self._minWidth = width
		self._minHeight = height
	def setMaxSize(self, width, height):
		self._maxWidth = width
		self._maxHeight = height
	def setPrefSize(self, width, height):
		self._prefWidth = width
		self._prefHeight = height
	def minWidth(self):
		return self._minWidth
	def minHeight(self):
		return self._minHeight
	def maxWidth(self):
		return self._maxWidth
	def maxHeight(self):
		return self._maxHeight
	def prefWidth(self):
		return self._prefWidth
	def prefHeight(self):
		return self._prefHeight


class Block(QWidget):
	def __init__(self, parent, bsize):
		QWidget.__init__(self, parent)
		self._parent = parent
		self._brush = QBrush(QColor(random.randint(128, 255), 
			random.randint(128, 255), random.randint(128, 255)))
		self._bsize = bsize
		self.resize(bsize.prefWidth(), bsize.prefHeight())
	def bsize(self):
		return self._bsize
	def paintEvent(self, e):
##		print 'Block paint', self.geometry().width(), \
##				self.geometry().height()
		p = QPainter(self)
		p.setBrush(self._brush)
		p.drawRect(e.rect())


class Container(Block):
	_data = None
	_order = None

	def __init__(self, parent, size, type):
		Block.__init__(self, parent, size)
		self._type = type
		self._data = {}
		self._order = []
	def __getitem__(self, name):
		return self._data[name]
	def __setitem__(self, name, block):
		self._data[name] = block
		if name not in self._order:
			self._order += [name]
		self.calcSize()
		self.rearrange('Parent')
	def __delitem__(self, name):
		self._data.destroy()
		del self._data[name]
		self._order.remove(name)
		self.calcSize()
		self.rearrange('Parent')
	def paintEvent(self, e):
##		print 'Container paint', len(self._data), self.geometry().width(), \
##				self.geometry().height()
		if len(self._data) == 0:
			Block.paintEvent(self, e)
	def resizeEvent(self, e):
		self.rearrange('Local')
	def calcSize(self):
		minWidth = 0
		minHeight = 0
		maxWidth = 0
		maxHeight = 0
		prefWidth = 0
		prefHeight = 0
		if len(self._order) == 0:
			bsize = Size(minWidth, minHeight, maxWidth, maxHeight, prefWidth,
					prefHeight)
			self._bsize = bsize
			return
		first = self._data[self._order[0]].bsize()
		type = self._type
		count = len(self._order)
		if type == "Horizontal":
			minHeight = first.minHeight()
			maxHeight = first.maxHeight()
			for bname in self._order:
				bsize = self._data[bname].bsize()
				size = self._data[bname].size()
				minWidth += bsize.minWidth()
				if bsize.minHeight() > minHeight:
					minHeight = bsize.minHeight()
				maxWidth += bsize.maxWidth()
				if bsize.maxHeight() < maxHeight:
					maxHeight = bsize.maxHeight()
				prefWidth += bsize.prefWidth()
				if bsize.prefWidth() == 0:
					prefWidth += size.width()
				prefHeight += bsize.prefHeight()
				if bsize.prefHeight() == 0:
					count -= 1
			if count > 1:
				prefHeight /= count
			if prefHeight < minHeight:
				minHeight = prefHeight
			if prefHeight > maxHeight:
				maxHeight = prefHeight
		if type == "Vertical":
			minWidth = first.minWidth()
			maxWidth = first.maxWidth()
			for bname in self._order:
				bsize = self._data[bname].bsize()
				size = self._data[bname].size()
				if bsize.minWidth() > minWidth:
					minWidth = bsize.minWidth()
				minHeight += bsize.minHeight()
				if bsize.maxWidth() < maxWidth:
					maxWidth = bsize.maxWidth()
				maxHeight += bsize.maxHeight()
				prefWidth += bsize.prefWidth()
				if bsize.prefWidth() == 0:
					count -= 1
				prefHeight += bsize.prefHeight()
				if bsize.prefHeight() == 0:
					prefHeight += size.height()
			if count > 1:
				prefWidth /= count
			if prefWidth < minWidth:
				minWidth = prefWidth
			if prefWidth > maxWidth:
				maxWidth = prefWidth
		bsize = Size(minWidth, minHeight, maxWidth, maxHeight, prefWidth,
				prefHeight)
		self._bsize = bsize
##		print len(self._order)
##		print minWidth, minHeight, maxWidth, maxHeight, prefWidth, prefHeight
	##!!! exhibits unstable behaviour:
	##!!!	- shrink and grow are asymmetric
	##!!!	- resizing in one step and in several smaller steps exhibit different results -- possible rounding error
	def rearrange(self, type):
		self.calcSize()
		if self._parent != None and type == 'Parent':
			self._parent.rearrange('Parent')
		if len(self._order) == 0:
			return
		type = self._type
		geometry = self.geometry()
		bsize = self._bsize

		if type == "Horizontal":
			dimention = 'width'
			min_size = bsize.minWidth()
			max_size = bsize.maxWidth()
			pref_size = bsize.prefWidth()
		else:
			dimention = 'height'
			min_size = bsize.minHeight()
			max_size = bsize.maxHeight()
			pref_size = bsize.prefHeight()
		geom_dimention = getattr(geometry, dimention)

		##!!! abstract out all the getitem calls -- possibly via attr caching (???) !!!##

		##!!! we ignore the "==" case, is this correct?
		if pref_size > geom_dimention():
			diffMin = 0
			diffSize = pref_size - geom_dimention()
			for bname in self._order:
				bsize = self._data[bname].bsize()
				size = self._data[bname].size()
				if getattr(bsize, 'pref' + dimention.title())() == 0:
					diffMin += getattr(size, dimention)()
				else:
					diffMin += getattr(bsize, 'pref' + dimention.title())() - getattr(bsize, 'min' + dimention.title())()
			for bname in self._order:
				bsize = self._data[bname].bsize()
				size = self._data[bname].size()
				possible = getattr(bsize, 'pref' + dimention.title())() - getattr(bsize, 'min' + dimention.title())()
				if getattr(bsize, 'pref' + dimention.title())() == 0:
					possible = getattr(size, dimention)()
				if diffMin > 0:
					delta = diffSize * possible / diffMin
				else:
					delta = diffSize / len(self._order)
				if getattr(bsize, 'pref' + dimention.title())() > 0:
					getattr(size, 'set' + dimention.title())(getattr(bsize, 'pref' + dimention.title())() - delta)
				else:
					getattr(size, 'set' + dimention.title())(getattr(size, dimention)() - delta)
				self._data[bname].resize(size)
		##!!! we ignore the "==" case, is this correct?
		elif pref_size < geom_dimention():
			diffMax = 0
			diffSize = geom_dimention() - pref_size
			for bname in self._order:
				size = self._data[bname].bsize()
				if getattr(size, 'pref' + dimention.title())() == 0:
					diffMax += 1000
				else:
					diffMax += getattr(size, 'max' + dimention.title())() - getattr(size, 'pref' + dimention.title())()
			for bname in self._order:
				bsize = self._data[bname].bsize()
				size = self._data[bname].size()
				possible = getattr(bsize, 'max' + dimention.title())() - getattr(bsize, 'pref' + dimention.title())()
				if getattr(bsize, 'pref' + dimention.title())() == 0:
					possible = 1000
				if diffMax > 0:
					delta = diffSize * possible / diffMax
				else:
					delta = diffSize / len(self._order)
				if getattr(bsize, 'pref' + dimention.title())() > 0:
					getattr(size, 'set' + dimention.title())(getattr(bsize, 'pref' + dimention.title())() + delta)
				else:
					getattr(size, 'set' + dimention.title())(getattr(size, dimention)() + delta)
				self._data[bname].resize(size)
		x = 0
		y = 0
		for bname in self._order:
			self._data[bname].move(x, y)
			size = self._data[bname].size()
			if type == "Horizontal":
				x += size.width()
##				print 'set height to:', geometry.height(), 'in', bname
				size.setHeight(geometry.height())
			if type == "Vertical":
				y += size.height()
				size.setWidth(geometry.width())
##				print 'set width to:', geometry.width(), 'in', bname
			self._data[bname].resize(size)


class GuiForm(Container):
	def __init__(self):
		Container.__init__(self, None, Size(100, 100, 1000, 800, 500, 400),
				"Vertical")
##		self["Block 0"] = Block(self, Size(100, 100, 1000, 800,
##			500, 400))
##		self["Block 1"] = Block(self, Size(100, 100, 1000, 800,
##			500, 400))
		self["Container 1"] = Container(self, Size(100, 100, 1000, 800,
			550, 450), "Vertical")
		self["Container 1"]["Container 1-1"] = Container(self["Container 1"],
				Size(50, 50, 1000, 800, 500, 100), "Horizontal")
		self["Container 1"]["Container 1-1"]["Block 1"] = Block(
				self["Container 1"]["Container 1-1"], Size(30, 30, 300, 200,
				200, 150))
		self["Container 1"]["Container 1-1"]["Container 1-1-2"] = Container(
				self["Container 1"]["Container 1-1"], Size(10, 10, 450, 350,
				120, 75), "Horizontal")
		self["Container 1"]["Container 1-1"]["Block 3"] = Block(
				self["Container 1"]["Container 1-1"], Size(50, 50, 400, 300,
				200, 175))
		self["Container 1"]["Container 1-2"] = Container(self["Container 1"],
				Size(100, 100, 250, 150, 200, 120), "Horizontal")
##		self["Container 1"]["Container 1-2"]["Block 4"] = Block(
##				self["Container 1"]["Container 1-2"], Size(500, 100, 750, 180,
##				550, 150))
		self["Container 1"]["Container 1-3"] = Container(self["Container 1"],
				Size(500, 100, 750, 180, 550, 150), "Horizontal")
		self["Container 1"]["Container 1-3"]["Block 5"] = Block(
				self["Container 1"]["Container 1-3"], Size(500, 100, 750, 200,
				550, 150))
		self["Container 1"]["Container 1-3"]["Block 6"] = Block(
				self["Container 1"]["Container 1-3"], Size(500, 100, 750, 200,
				550, 150))


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = GuiForm()
	w.show()
	sys.exit(app.exec_())



