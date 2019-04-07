from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import tensorflow as tf

from nlp_architect.utils.metrics import get_conll_scores


class ConllCallback(tf.keras.callbacks.Callback):
    """
    A Tensorflow(Keras) Conlleval evaluator.
    Runs the conlleval script for given x and y inputs.
    Prints Conlleval F1 score on the end of each epoch.

    Args:
        x: features matrix
        y: labels matrix
        y_vocab (dict): int-to-str labels lexicon
        batch_size (:obj:`int`, optional): batch size
    """

    def __init__(self, x, y, y_vocab, batch_size=1):
        super(ConllCallback, self).__init__()
        self.x = x
        self.y = y
        self.y_vocab = {v: k for k, v in y_vocab.items()}
        self.bsz = batch_size

    def on_epoch_end(self, epoch, logs=None):
        predictions = self.model.predict(self.x, batch_size=self.bsz)
        stats = get_conll_scores(predictions, self.y, self.y_vocab)
        print()
        print('Conll eval: \n{}'.format(stats))
