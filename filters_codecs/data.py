#=======================================================================

__version__ = '''0.0.01'''

#-----------------------------------------------------------------------

import sys
from PIL import ImageOps

#-----------------------------------------------------------------------
class ObjectData(object):
	'''
	Class which stores inner representation of program object.
	Each Object has type which is used to determine possibilities
	of it's processing
	'''
	def __init__(self, type):
		self.type = type

#-----------------------------------------------------------------------
class ImageData(ObjectData):
	'''
	ObjectData abstract subclass for storing image as an object.
	All image processing should be performed through this class API
	to avoid binding to certain image format.
	Therefore, image in any format can be passed here,
	but the format should be sufficient to implement class API
	'''
	def __init__(self, image):
		super(ImageData, self).__init__('image')
		self.image = image
	def get_size(self):
		'''
		Returns 2-tuple of (width, height)
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'
	def crop(self, rect):
		'''
		Returns cropped copy of image.
		"rect" should be a 4-tuple of (left, top, width, height)
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'
	def invert(self):
		'''
		Returns inverted copy of image
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'
	# XXX: basic image API should be defined here
	# (maybe it needs to be close to simple 2-dimensional pixel array API,
	# only some pixel-wise operations etc., so that all high-level processing
	# could be moved to filters)

#-----------------------------------------------------------------------
class PILImageData(ImageData):
	'''
	Implementation of ImageData with PIL.Image instance
	'''
	def __init__(self, image):
		super(PILImageData, self).__init__(image)
	def get_size(self):
		return self.image.size
	def crop(self, rect):
		width, height = self.image.size
		cr_left, cr_top, cr_width, cr_height = rect
		if width < cr_left or height < cr_top:
			return None
		if width < cr_left + cr_width:
			cr_width = width - cr_width
		if height < cr_top + cr_height:
			cr_height = height - cr_top
		cr_right = cr_left + cr_width
		cr_bottom = cr_top + cr_height
		cr = self.image.crop((cr_left, cr_top, cr_right, cr_bottom))
		cr.load()
		return PILImageData(cr)
	def invert(self):
		inv = ImageOps.invert(self.image)
		return PILImageData(inv)
	
#-----------------------------------------------------------------------
if __name__ == '__main__':
	pass
#=======================================================================