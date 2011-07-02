#=======================================================================

__version__ = '''0.0.01'''

#-----------------------------------------------------------------------

from codec import PILJpegCodec
from filter import CropFilter, InvertFilter

#-----------------------------------------------------------------------
def test_1():
	in_path = 'test_image.jpg'
	out_path = 'test_image_out.jpg'

	in_codec = PILJpegCodec()
	out_codec = PILJpegCodec()

	f1 = InvertFilter()

	f2 = CropFilter()
	f2.set_size((1.0, 0.5))
	
	in_codec.load(in_path)
	f1.set_input(in_codec)
	f2.set_input(f1)
#	f1.set_visible(False)
#	f2.set_visible(False)		

	out_codec.set_data(f2.get_data())
	out_codec.save(out_path)
#-----------------------------------------------------------------------
if __name__ == '__main__':
	test_1()
#=======================================================================