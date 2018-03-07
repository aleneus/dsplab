import numpy as np

print("Warning! dsplab.io deprecated.")

def read_signal_from_csv(file_name, t_column=0, x_column=1, start_line=1, fs=None, delimiter=';'):
    """ Deprecated. """
    data = np.genfromtxt(file_name, delimiter=delimiter)
    data = data.transpose()
    x = np.array(data[x_column][start_line:])
    if not fs:
        t = np.array(data[t_column][start_line:])
    else:
        t = np.linspace(0, (len(x)-1)/fs, len(x))
    return x, t
