import pickle
import tempfile

from tensorflow import keras


def save_model(model: keras.models.Model, topology: dict, filepath: str) -> None:
    """
    Save a model to a file (tf.keras models only)
    The method save the model topology, as given as a
    Args:
        model: model object
        topology (dict): a dictionary of topology elements and their values
        filepath (str): path to save model
    """
    with tempfile.NamedTemporaryFile(suffix='.h5', delete=True) as fd:
        model.save_weights(fd.name)
        model_weights = fd.read()
    data = {'model_weights': model_weights,
            'model_topology': topology}
    with open(filepath, 'wb') as fp:
        pickle.dump(data, fp)


def load_model(filepath, model) -> None:
    """
    Load a model (tf.keras) from disk, create topology from loaded values
    and load weights.
    Args:
        filepath (str): path to model
        model: model object to load
    """
    with open(filepath, 'rb') as fp:
        model_data = pickle.load(fp)
    topology = model_data['model_topology']
    model.build(**topology)
    with tempfile.NamedTemporaryFile(suffix='.h5', delete=True) as fd:
        fd.write(model_data['model_weights'])
        fd.flush()
        model.model.load_weights(fd.name)
