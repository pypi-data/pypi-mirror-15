/* Custom param wrapping, for arrays of pointers as input and output

/* Used in cmsCreateRGBProfile(). Wrap the TransferFunction array as a python sequence. */
%typemap(in) cmsToneCurve* const TransferFunction[ANY] (void* temp[$1_dim0]) {
  int i;
  if (!PySequence_Check($input)) {
    PyErr_SetString(PyExc_ValueError,"Expected a sequence");
    return NULL;
  }
  if (PySequence_Length($input) != $1_dim0) {
    PyErr_SetString(PyExc_ValueError,"Size mismatch. Expected $1_dim0 elements");
    return NULL;
  }
  for (i = 0; i < $1_dim0; i++) {
    int res;
    PyObject *o = PySequence_GetItem($input,i);
    res = SWIG_ConvertPtr(o, &temp[i], SWIGTYPE_p__cms_curve_struct, 0 |  0 );
    if (!SWIG_IsOK(res)) {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be cmsToneCurve*");
      return NULL;
    }
  }
  $1 = (cmsToneCurve **)temp;
}

/* Used in cmsStageAllocToneCurves(). Wrap the Curves array as a python sequence. */
%typemap(in) cmsToneCurve* const Curves[ANY] (void* temp[16]) {
  int i;
  if ($input == Py_None) {
    $1 = (cmsToneCurve **)NULL;
  }
  else {
    if (!PySequence_Check($input)) {
      PyErr_SetString(PyExc_ValueError,"Expected a sequence");
      return NULL;
    }
    if (PySequence_Length($input) == 0) {
      PyErr_SetString(PyExc_ValueError,"No curves.");
      return NULL;
    }
    if (PySequence_Length($input) > 16) {
      PyErr_SetString(PyExc_ValueError,"Too many curves, max 16.");
      return NULL;
    }
    for (i = 0; i < PySequence_Length($input); i++) {
      int res;
      PyObject *o = PySequence_GetItem($input,i);
      res = SWIG_ConvertPtr(o, &temp[i], SWIGTYPE_p__cms_curve_struct, 0 |  0 );
      if (!SWIG_IsOK(res)) {
        PyErr_SetString(PyExc_ValueError,"Sequence elements must be cmsToneCurve*");
        return NULL;
      }
    }
    $1 = (cmsToneCurve **)temp;
  }
}
