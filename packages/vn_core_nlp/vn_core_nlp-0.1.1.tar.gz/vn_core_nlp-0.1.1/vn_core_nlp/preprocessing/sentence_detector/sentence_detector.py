from subprocess import Popen
import os


path = os.path.dirname(os.path.realpath(__file__)) + '/vn.hus.nlp.sd-2.0.0-bin'


class SentenceDetector(object):
    def sentence_detector(self, input_dir, output_dir):
        Popen(['chmod', '-R', '777', './vnSentDetector.sh'], cwd=path)
        Popen(['./vnSentDetector.sh', '-i',  input_dir, '-o', output_dir], cwd=path).communicate()
