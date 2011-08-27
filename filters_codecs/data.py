#=======================================================================

__version__ = '''0.0.01'''

#-----------------------------------------------------------------------

import sys, numpy
from PIL import Image, ImageMath, ImageOps

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
	def apply(self, func_str, *args):
		func = getattr(self, '_' + func_str)
		if func != None:
			return func(*args)
	def get_size(self):
		'''
		Returns 2-tuple of (width, height)
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'
	def _crop(self, rect):
		'''
		Returns cropped copy of image.
		"rect" should be a 4-tuple of (left, top, width, height)
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'
	def _invert(self):
		'''
		Returns inverted copy of image
		'''
		raise NotImplementedError, 'Should be overridden in subclasses'
	def _blend(self, image, mode):
		'''
		Returns new image created as the result of blending
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
	def _crop(self, rect):
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
	def _invert(self):
		inv = ImageOps.invert(self.image)
		return PILImageData(inv)
	def _blend(self, image, mode):
		eval_expr = 'a'
		if mode == 'multiply':
			eval_expr = 'a * b / 255'
		elif mode == 'screen':
			eval_expr = '255 - (255 - a) * (255 - b) / 255'

		eval = lambda x, y : ImageMath.eval(eval_expr, a=x, b=y).convert('L')
		layers_1 = self.image.split()
		layers_2 = image.image.split()
		tmp = Image.merge("RGB", map(eval, layers_1, layers_2))
		return PILImageData(tmp)
#-----------------------------------------------------------------------
if __name__ == '__main__':
	pass
#=======================================================================