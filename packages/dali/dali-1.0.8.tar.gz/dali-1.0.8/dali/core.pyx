


from libcpp.string   cimport string
from libcpp11.vector cimport vector
from libcpp11.memory cimport shared_ptr
# Import the Python-level symbols of numpy
import numpy as np
# Import the C-level symbols of numpy
cimport modern_numpy as np

cdef string normalize_s(s):
    if type(s) is str:
        return s.encode("utf-8")
    elif type(s) is bytes:
        return s
    else:
        raise TypeError("Must pass a str or bytes object.")

cdef bint is_fdtype(np.NPY_TYPES type_id) nogil:
    return type_id == np.NPY_FLOAT32 or \
           type_id == np.NPY_FLOAT64

cdef inline void ensure_fdtype(np.NPY_TYPES type_id):
    if not is_fdtype(type_id):
        raise ValueError(
            "Invalid dtype: " +
            str(np.PyArray_DescrFromType(type_id)) +
            " (should be one of float32, float64)")

include "core/utils/config.pyx"

# File IO, save / load, etc...
include "core/utils/core_utils.pyx"

# Used for storing Tensor buffers
include "core/math/TensorInternal.pyx"

# Matrix class
include "core/tensor/Mat.pyx"

cdef copy_name_int(const CMat[int]& source, const CMat[int]& dest):
    if source.name == NULL:
        (<CMat[int]&>source).set_name('')
    (<CMat[int]&>dest).name = source.name
cdef copy_name_float(const CMat[float]& source, const CMat[float]& dest):
    if source.name == NULL:
        (<CMat[float]&>source).set_name('')
    (<CMat[float]&>dest).name = source.name
cdef copy_name_double(const CMat[double]& source, const CMat[double]& dest):
    if source.name == NULL:
        (<CMat[double]&>source).set_name('')
    (<CMat[double]&>dest).name = source.name


# Matrix initialization with random numbers.
include "core/tensor/random.pyx"

# Softmax, crossentropy etc....
include "core/tensor/MatOps.pyx"

# Related to backpropagation.
include "core/tensor/Tape.pyx"

# Layer, RNN, StackedInputLayer, etc...
include "core/layers/Layers.pyx"

include "core/layers/GRU.pyx"

include "core/layers/LSTM.pyx"

# # Matrix class
include "core/data_processing/Batch.pyx"

# # State for StackedModel and StackedGatedModel
include "core/models/StackedModelState.pyx"

# # Stacked Model, a stacked LSTM with embedding and
# # decoder all in one.
include "core/models/StackedModel.pyx"

# SGD, Adagrad, Adadelta, etc...
include "core/tensor/Solver.pyx"

