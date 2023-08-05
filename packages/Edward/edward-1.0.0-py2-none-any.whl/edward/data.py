import numpy as np
import tensorflow as tf

class Data:
    """
    Base class for data.

    By default, it assumes the data is a vector and subsamples data
    i.i.d. (independent and identically distributed). Use one of the
    derived classes for subsampling more complex data structures.

    Arguments
    ----------
    data: dict, tf.tensor, np.ndarray, optional
        Data whose type depends on the type of model it is fed into:
        Stan, TensorFlow, and NumPy/SciPy respectively.
    shuffled: bool, optional
        Whether the data is shuffled.
    """
    def __init__(self, data=None, shuffled=True):
        self.data = data
        if not shuffled:
            # TODO
            # shuffle self.data
            raise NotImplementedError()

        self.counter = 0
        if self.data is None:
            self.N = None
        elif isinstance(self.data, tf.Tensor):
            self.N = self.data.get_shape()[0].value
        elif isinstance(self.data, np.ndarray):
            self.N = self.data.shape[0]
        elif isinstance(self.data, dict):
            pass
        else:
            raise

    def sample(self, n_data=None):
        if n_data is None:
            return self.data

        counter_new = self.counter + n_data
        if isinstance(self.data, tf.Tensor):
            if counter_new <= self.N:
                minibatch = self.data[self.counter:counter_new]
                self.counter = counter_new
            else:
                counter_new = counter_new - self.N
                minibatch = tf.concat(0, [self.data[self.counter:],
                                          self.data[:counter_new]])
                self.counter = counter_new

            return minibatch
        elif isinstance(self.data, np.ndarray):
            if counter_new <= self.N:
                minibatch = self.data[self.counter:counter_new]
                self.counter = counter_new
            else:
                counter_new = counter_new - self.N
                minibatch = np.concatenate((self.data[self.counter:],
                                            self.data[:counter_new]))
                self.counter = counter_new

            return minibatch
        else:
            minibatch = self.data.copy()
            if counter_new <= self.N:
                minibatch['y'] = minibatch['y'][self.counter:counter_new]
                self.counter = counter_new
            else:
                counter_new = counter_new - self.N
                minibatch['y'] = minibatch['y'][self.counter:] + \
                                 minibatch['y'][:counter_new]
                self.counter = counter_new

            return minibatch
# TODO
# for more complex data structures, specify a default for sampling,
# e.g., for matrices sample rows or something
