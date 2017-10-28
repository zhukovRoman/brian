import png
import numpy

f = open('images/1.png', 'rb')      # binary mode is important

r=png.Reader(f)
pngdata = r.read()
print(list(pngdata[2]))
image_2d = numpy.vstack(itertools.imap(numpy.uint16, pngdata))
print(image_2d)
f.close()