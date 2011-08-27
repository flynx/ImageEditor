#=======================================================================

__version__ = '''0.0.01'''

#-----------------------------------------------------------------------

from codec import PILJpegCodec
from filter import CropFilter, InvertFilter, BlendFilter
import pickle

#-----------------------------------------------------------------------
def test_1():
	in_path = 'test_image.jpg'
	out_path = 'test_image_out.jpg'

	in_codec = PILJpegCodec()
	out_codec = PILJpegCodec()

	f1 = InvertFilter()

	f2 = CropFilter()
	f2.set_size((1.0, 0.5))
	
	f3 = BlendFilter()
	
	in_codec.load(in_path)
	f1.set_input(in_codec)
	f2.set_input(f1)

	f3.set_inputs(in_codec, f2)
	
#	f1.set_visible(False)
#	f2.set_visible(False)		

	out_codec.set_data(f3.get_data())
	out_codec.save(out_path)
#-----------------------------------------------------------------------
def test_2():
	f1 = InvertFilter()

	f2 = CropFilter()
	f2.set_size((1.0, 0.5))
	
	f_lst = [f1, f2]
	
	pkl_out = open('filters.pkl', 'wb')
	pickle.dump(f_lst, pkl_out)

	pkl_out.close()
#-----------------------------------------------------------------------
def test_3():
	in_path = 'test_image.jpg'
	out_path = 'test_image_out.jpg'

	in_codec = PILJpegCodec()
	out_codec = PILJpegCodec()

	f_lst_in = open('filters.pkl', 'rb')
	f_lst = pickle.load(f_lst_in)
	
	input = in_codec
	input.load(in_path)
	for f in f_lst:
		f.set_input(input)
		input = f
		
	out_codec.set_data(input.get_data())
	out_codec.save(out_path)
#-----------------------------------------------------------------------
def test_4():
	in_path = 'test_image.jpg'
	in_path_2 = 'test_image_2.jpg'
	out_path = 'test_image_out.jpg'

	in_codec = PILJpegCodec()
	in_codec_2 = PILJpegCodec()
	out_codec = PILJpegCodec()

	in_codec.load(in_path)
	in_codec_2.load(in_path_2)

	f1 = BlendFilter('screen')	
#	f1 = BlendFilter('multiply')
	
	f1.set_inputs(in_codec, in_codec_2)
	f1.set_input(in_codec, 1) # example of changing second input
	
	out_codec.set_data(f1.get_data())
	out_codec.save(out_path)
#-----------------------------------------------------------------------
if __name__ == '__main__':
#	test_1()
#	test_2()
#	test_3()
	test_4()
#=======================================================================