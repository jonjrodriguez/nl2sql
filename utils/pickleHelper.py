try:
    import cPickle as pickle
except:
    import pickle


def load_pickle(path):
    f = open(path, 'rb')
    result = pickle.load(f)
    f.close()
    return result


def save_pickle(data, path):
    with open(path, "wb") as data_file:
        pickle.dump(data, data_file)