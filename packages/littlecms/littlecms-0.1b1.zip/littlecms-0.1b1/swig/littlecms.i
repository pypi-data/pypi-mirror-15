%module littlecms

/* Some littlecms definitions are needed before the code is wrapped. */
%header %{
  #include "lcms2.h"
  #include "lcms2_plugin.h"
%}

/* Deal with Windows */
%include windows.i              /* Support calling conventions to create a wrapper for use on Linux. */
%define _CRT_BEGIN_C_HEADER     /* Support VS2015 for Python v3.5+; used in limits.h. */
%enddef
%define _CRT_END_C_HEADER
%enddef

/* Casts for littlecms pipelines. */
%include cpointer.i
%pointer_cast(void *, cmsPipeline *, void_to_pipeline);
%pointer_cast(void *, _cmsStageCLutData *, void_to_clut_data);

/* C array classes. */
%include carrays.i
%array_class(unsigned long long, uint64Array);
%array_class(unsigned int, uint32Array);
%array_class(unsigned short, uint16Array);
%array_class(unsigned char, uint8Array);
%array_class(char, charArray);
%array_class(double, doubleArray);

/* Non-default wrapping has been modularised to other swig files. */
%include littlecms_error_handler.i
%include littlecms_null_inputs.i
%include littlecms_sampler_callback.i
%include littlecms_test_helpers.i


/* Wrap the header files. */
%import "limits.h"
%include "lcms2.h"
%include "lcms2_plugin.h"


/* Pythoncode blocks have to come after the wrapping. */
%pythoncode %{
# Marshal the sampler callback to use the Python function.
def cmsStageSampleCLut16bit(mpe, sampler, py_cargo, dwflags):
  cargo = sampler_cargo()
  cargo.in_dims = cmsStageInputChannels(mpe)
  cargo.out_dims = cmsStageOutputChannels(mpe)

  cargo.py_in = uint16Array(cargo.in_dims)
  cargo.py_out = uint16Array(cargo.out_dims)
  cargo.py_cargo = py_cargo
  result = _littlecms.cmsStageSampleCLut16bit(mpe, sampler, cargo, dwflags)
  return result
%}

%pythoncode %{
# Setup the littlecms error callback in all new contexts.
def cmsCreateContext(Plugin, UserData):
  new_context = _littlecms.cmsCreateContext(Plugin, UserData)
  littlecms_set_error_function(new_context)
  return new_context
def cmsDupContext(ContextID, NewUserData):
  new_context = _littlecms.cmsDupContext(ContextID, NewUserData)
  littlecms_set_error_function(new_context)
  return new_context
%}

%pythoncode %{
# Some API functions return data in array params allocated by the client.
# Make it simpler to handle this kind of data for individual functions.
def cmsGetHeaderProfileID(hProfile):
  id = uint8Array(16)
  _littlecms.cmsGetHeaderProfileID(hProfile, id)
  return tuple(id[i] for i in range(16))		# SWIG arrays don't know their length
%}
