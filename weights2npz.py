#! /home/longc/anaconda3/bin/python3

# python3 weights2npz.py --model cfg/darknet19.cfg --load bin/darknet19.weights


from net.build import TFNet
from tensorflow import flags
import os

flags.DEFINE_string("test", "./test/", "path to testing directory")
flags.DEFINE_string("binary", "./bin/", "path to .weights directory")
flags.DEFINE_string("config", "./cfg/", "path to .cfg directory")
flags.DEFINE_string("dataset", "./data/VOCdevkit/VOC2007/JPEGImages/", "path to dataset directory")
flags.DEFINE_string("backup", "./ckpt/", "path to backup folder")
flags.DEFINE_string("annotation", "../pascal/VOCdevkit/ANN/", "path to annotation directory")
flags.DEFINE_float("threshold", 0.1, "detection threshold")
flags.DEFINE_string("model", "cfg/yolo-voc.cfg", "configuration of choice")
flags.DEFINE_string("trainer", "rmsprop", "training algorithm")
flags.DEFINE_float("momentum", 0.0, "applicable for rmsprop and momentum optimizers")
flags.DEFINE_boolean("verbalise", True, "say out loud while building graph")
flags.DEFINE_boolean("train", False, "train the whole net")
flags.DEFINE_string("load", "bin/yolo-voc.weights", "how to initialize the net? Either from .weights or a checkpoint, or even from scratch")
flags.DEFINE_boolean("savepb", False, "save net and weight to a .pb file")
flags.DEFINE_float("gpu", 0.6, "how much gpu (from 0.0 to 1.0)")
flags.DEFINE_float("lr", 1e-5, "learning rate")
flags.DEFINE_integer("keep", 20, "Number of most recent training results to save")
flags.DEFINE_integer("batch", 16, "batch size")
flags.DEFINE_integer("epoch", 1000, "number of epoch")
flags.DEFINE_integer("save", 2000, "save checkpoint every ? training examples")
flags.DEFINE_string("demo", '', "demo on webcam")
flags.DEFINE_boolean("profile", False, "profile")
FLAGS = flags.FLAGS


# make sure all necessary dirs exist
def get_dir(dirs):
    for d in dirs:
        this = os.path.abspath(os.path.join(os.path.curdir, d))
        if not os.path.exists(this): os.makedirs(this)


get_dir([FLAGS.test, FLAGS.binary, FLAGS.backup, os.path.join(FLAGS.test, 'out')])

# fix FLAGS.load to appropriate type
weight_fname = FLAGS.load
try:
    FLAGS.load = int(FLAGS.load)
except:
    pass

tfnet = TFNet(FLAGS)

if FLAGS.profile:
    tfnet.framework.profile(tfnet)
    exit()

if FLAGS.demo:
    tfnet.camera(FLAGS.demo)
    exit()

if FLAGS.train:
    print('Enter training ...');
    tfnet.train()
    if not FLAGS.savepb: exit('Training finished')

if FLAGS.savepb:
    print('Rebuild a constant version ...')
    tfnet.savepb();
    exit('Done')

# # print(tfnet.meta)
# with tfnet.graph.as_default() as g:
#     tfnet.predict()

npz_fname = '{}.npz'.format(weight_fname)
print('save to {}'.format(npz_fname))
tfnet.savenpz(npz_fname)
