import numpy as np
import tensorflow as tf
import vgg19
import utils

BATCH_SIZE = 50


filenames = []
f = open('../data/image_ids.txt', 'r')
for line in f:
	filenames.append(line.strip())
f.close()

def print_visembed(nameimg, sumsecond, f):
	strtoadd = nameimg + " " + " ".join([str(i) for i in sumsecond]) + "\n"
	f.write(strtoadd)  # python will convert \n to os.linesep

fi = open('./notused.txt', 'w')
	
def imageget(startind, endind):
	imgs = []
	for i, filen in enumerate(filenames[startind:endind]):
		im = utils.load_image("/home/alisha/VG_100K/" + filen + ".jpg")
		if len(im.shape) != 3:
			fi.write(filen + '\n')
			continue
		imgs.append(im.reshape((224, 224, 3)))
	imgsnp = np.array(imgs)
	return imgsnp

f = open('../cnn.txt', 'w')
with tf.Session() as sess:
    size = len(filenames)
    for step in xrange(size / BATCH_SIZE):
      offset = step * BATCH_SIZE
      batch_data = imageget(offset,offset + BATCH_SIZE)
      images = tf.placeholder("float", [BATCH_SIZE, 224, 224, 3])
      feed_dict = {images: batch_data}
      vgg = vgg19.Vgg19()
      with tf.name_scope("content_vgg"):
      	vgg.build(images)
      output = sess.run(vgg.output, feed_dict=feed_dict)
      for ind, out in enumerate(output):
	npyout = np.array(out)
	sumit = np.concatenate(npyout[:])
	print_visembed(filenames[offset+ind], sumit, f)
f.close()
fi.close()
