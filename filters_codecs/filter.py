#=======================================================================

__version__ = '''0.0.02'''

#-----------------------------------------------------------------------

import sys
import pygame
from data import ImageData

#-----------------------------------------------------------------------
class BaseFilter(object):
	'''
	Class which defines processing over program object
	'''
	def set_input(self, input):
		'''
		Sets input of current filter.
		Input should be a filter or a codec
		implementing "get_data()" method
		'''
		self.input = input
	def get_data(self):
		data = self.input.get_data()
		return self.process(data)
	def process(self, data):
		'''
		Processes data and returns the result
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'

#-----------------------------------------------------------------------
class ProcessingEnabledToggleMixin(object):
	'''
	Mixin which allows to enable/disable procesiing performed by filters
	'''
	enabled = True

	def get_data(self):
		if self.enabled:
			return super(ProcessingEnabledToggleMixin, self).get_data()
		return self.input.get_data()

#-----------------------------------------------------------------------
class Filter(ProcessingEnabledToggleMixin, BaseFilter):
	'''
	'''
	pass

#-----------------------------------------------------------------------
class ImageFilter(Filter):
	'''
	Filter which processes images
	'''
	def __init__(self):
		super(ImageFilter, self).__init__()
	def process(self, data):
		if not isinstance(data, ImageData):
			raise TypeError, 'Input data should be an image'
		return self.process_image(data)
	def process_image(self, image):
		raise NotImplementedError, 'Should be overridden in subclasses'
		
#-----------------------------------------------------------------------
class CropFilter(ImageFilter):
	'''
	Filter which crops images
	'''
	def __init__(self):
		super(CropFilter, self).__init__()
		self.cr_alignment = (0.5, 0.5) # crop area alignment, % of source
		self.cr_size = (1.0, 1.0) # crop area size, % of source
	def set_alignment(self, cr_alignment):
		self.cr_alignment = cr_alignment
	def set_size(self, cr_size):
		self.cr_size = cr_size
	def process_image(self, image):
		width, height = image.get_size()
		cr_width = width * self.cr_size[0]
		cr_height = height * self.cr_size[1]
		cr_left = (width - cr_width) * self.cr_alignment[0]
		cr_top = (height - cr_height) * self.cr_alignment[1]
		cr_rect = (cr_left, cr_top, cr_width, cr_height)
		return image.crop((int(x) for x in cr_rect))
			
#-----------------------------------------------------------------------
class InvertFilter(ImageFilter):
	'''
	Filter which inverts images
	'''
	def process_image(self, image):
		return image.invert()
#=======================================================================
