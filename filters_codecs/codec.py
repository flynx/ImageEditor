#=======================================================================

__version__ = '''0.0.02'''

#-----------------------------------------------------------------------

import sys
from PIL import Image
from data import PILImageData

#-----------------------------------------------------------------------
class Codec(object):
	'''
	Class which gets data in some format and can return it wrapped
	as ObjectData; vice versa, wrapped data can be passed to codec
	and it should propagate it back to some format
	'''
	def __init__(self):
		self.data = None
	def set_data(self, data):
		self.data = data
	def get_data(self):
		return self.data

#-----------------------------------------------------------------------
class PILJpegCodec(Codec):
	'''
	Codec which works with jpeg images using PIL.Image 
	'''
	def load(self, img_path):
		self.data = PILImageData(Image.open(img_path))
	def save(self, img_out_path):
		self.data.image.save(img_out_path, 'JPEG')

#-----------------------------------------------------------------------
if __name__ == '__main__':
	pass
#=======================================================================