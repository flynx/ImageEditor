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
	def __init__(self):
		'''
		Arity defaults to 1, should be overridden in subclasses if needed
		'''
		self.arity = 1
		self.inputs = [None for i in range(self.arity)]
	def set_inputs(self, *inputs):
		'''
		Sets a set of inputs of current filter.
		Each input should be a filter or a codec
		implementing "get_data()" method.
		'''
		if len(inputs) > self.arity: # too much inputs
			self.inputs = list(inputs[:self.arity])
		elif len(inputs) < self.arity: # not enough inputs
			self.inputs[:self.arity] = list(inputs)
		else:
			self.inputs = list(inputs)
	def set_input(self, input, index = 0):
		'''
		Sets a particular input of current filter.
		'''
		if index < 0 or index >= self.arity:
			raise InputError, 'Wrong index'
		else:
			self.inputs[index] = input
	def get_data(self):
		data = [i.get_data() for i in self.inputs]
		return self.process(*data)
	def process(self, *data):
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
class Filter(BaseFilter, ProcessingEnabledToggleMixin):
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
	def process(self, *data):
		for item in data:
			if not isinstance(item, ImageData):
				raise TypeError, 'One of input items is not an image'
		return self.process_images(*data)
	def process_images(self, *images):
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
	def process_images(self, image):
		width, height = image.get_size()
		cr_width = width * self.cr_size[0]
		cr_height = height * self.cr_size[1]
		cr_left = (width - cr_width) * self.cr_alignment[0]
		cr_top = (height - cr_height) * self.cr_alignment[1]
		cr_rect = (cr_left, cr_top, cr_width, cr_height)
		return image.apply('crop', (int(x) for x in cr_rect))
			
#-----------------------------------------------------------------------
class InvertFilter(ImageFilter):
	'''
	Filter which inverts images
	'''
	def process_images(self, image):
		return image.apply('invert')

#-----------------------------------------------------------------------
class BlendFilter(ImageFilter):
	'''
	Filter which blends images
	'''
	def __init__(self, mode):
		self.mode = mode
		super(BlendFilter, self).__init__()
		self.arity = 2
	def process_images(self, image_1, image_2):
		return image_1.apply('blend', image_2, self.mode)
#=======================================================================
