/* Wrapping the littlecms sampler callback functions needs extra help. */

/* The PyObject * fields in sampler_cargo require their python refcnts managed. */
%typemap(memberin) PyObject * {
  Py_DecRef($1);
  $1 = $input;
  Py_IncRef($1);
}

%inline %{
  /* The sampler_cargo struct for sampler16 callbacks */
  typedef struct sampler_cargo {
    int in_dims;
    int out_dims;
    PyObject *py_in;
    PyObject *py_out;
    PyObject *py_cargo;
  } sampler_cargo;
%}

/* The trampoline callback for cmsSAMPLER16.
 * It marshals the In and Out arrays to/from Python array_class arrays and calls
 * the Python callback that has been squirrelled into py_sample_func.
 */
%header %{
  static PyObject *py_sample_func;

  static cmsInt32Number sample_func(register const cmsUInt16Number In[],
                                    register cmsUInt16Number Out[],
                                    register sampler_cargo *Cargo)
  {
    PyObject *py_in;
    PyObject *py_out;
    PyObject *py_cargo;
    PyObject *py_result;
    unsigned int in_dims;
    unsigned int out_dims;
    short *c_in = NULL;
    short *c_out = NULL;
    unsigned int i;

    in_dims = Cargo->in_dims;
    out_dims = Cargo->out_dims;
    py_in = Cargo->py_in;
    py_out = Cargo->py_out;

    /* py_in & py_out must be uint16Array  objects*/
    SWIG_ConvertPtr(py_in, (void **) &c_in, SWIGTYPE_p_uint16Array, 0);
    SWIG_ConvertPtr(py_out, (void **) &c_out, SWIGTYPE_p_uint16Array, 0);

    /* Copy the contents of In & Out to the py_in & py_out Python wrapping objects */
    for (i = 0; i < in_dims; i++)
      c_in[i] = In[i];
    for (i = 0; i < out_dims; i++)
      c_out[i] = Out[i];

    /* Pass python callback data back to python unmodified */
    py_cargo = Cargo->py_cargo;

    py_result = PyObject_CallFunctionObjArgs(py_sample_func, py_in, py_out, py_cargo, NULL);

    /* Copy the contents of Out back to the py_out Python wrapping objects */
    for (i = 0; i < out_dims; i++)
      Out[i] = c_out[i];

    return TRUE;
  }
%}

/* Trampoline the real python callback from sample_func() and store the real
 * callback in py_sample_func.
 */
%typemap(in) cmsSAMPLER16 {
  py_sample_func = $input;
  $1 = (cmsSAMPLER16) sample_func;
}
