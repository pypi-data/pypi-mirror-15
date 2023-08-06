/* Helpers that throw python exceptions for:
 * - library errors using the littlecms_error_handler error callback.
 * - memory access violations by catching SIGSEGV signals.
 */

%header %{
  #include <signal.h>

  void littlecms_signal_handler(int signal)
  {
    throw 1;
  }

  cmsBool littlecms_error_status = FALSE;
  static char littlecms_error_message[256];

  void littlecms_error_handler(cmsContext ContextID,
                               cmsUInt32Number ErrorCode,
                               const char *Text)
  {
    littlecms_error_status = TRUE;
    strcpy(littlecms_error_message, Text);
  }

  void clear_exception() {
	  littlecms_error_status = FALSE;
  }
  cmsBool check_exception() {
	  return littlecms_error_status;
  }

  void report_error()
  {
    PyObject *pyerr;

    switch(littlecms_error_status) {
    case cmsERROR_FILE:   pyerr = PyExc_IOError;      break;
    case cmsERROR_RANGE:  pyerr = PyExc_ValueError;   break;
    case cmsERROR_NULL:   pyerr = PyExc_MemoryError;  break;
    case cmsERROR_READ:   pyerr = PyExc_IOError;      break;
    case cmsERROR_SEEK:   pyerr = PyExc_IOError;      break;
    case cmsERROR_WRITE:  pyerr = PyExc_IOError;      break;
    default:              pyerr = PyExc_Exception;    break;
    }

    PyErr_SetString(pyerr, littlecms_error_message);
  }
%}

/* Handle littlecms errors and access violations. */
%exception {
  void (__cdecl *previous_handler)(int);

  clear_exception();
  previous_handler = signal(SIGSEGV , littlecms_signal_handler);
  try {
    $action
  }
  catch (int) {
    PyErr_SetString(PyExc_RuntimeError, "Access violation");
    SWIG_fail;
  }

  signal(SIGSEGV, previous_handler);
  if (check_exception()) {
    report_error();
    SWIG_fail;
  }
}

/* Setup the littlecms error callback in the initial context. */
%init %{
  cmsSetLogErrorHandlerTHR(NULL, littlecms_error_handler);
%}

/* Helper for setting the littlecms error callback in new contexts. */
%inline %{
  void littlecms_set_error_function(cmsContext new_context)
  {
    cmsSetLogErrorHandlerTHR(new_context, littlecms_error_handler);
  }
%}

/* Don't allow python code to replace our error logging callback. */
%ignore cmsSetLogErrorHandler;
%ignore cmsSetLogErrorHandlerTHR;


/* For completeness, this is a list of destructors. Their objects become invalid
 * after the call, but the binding doesn't have any way of ensuring they aren't
 * reused.
 * cmsCIECAM02Done(hModel):
 * cmsCloseIOhandler(io):
 * cmsCloseProfile(hProfile):
 * cmsDeleteContext(ContextID):
 * cmsDeleteTransform(hTransform):
 * cmsDictFree(hDict):
 * cmsFreeNamedColorList(v):
 * cmsFreeProfileSequenceDescription(pseq):
 * cmsFreeToneCurve(Curve):
 * cmsGBDFree(hGBD):
 * cmsIT8Free(cmsIT8):
 * cmsMLUfree(mlu):
 * cmsPipelineFree(lut):
 * cmsStageFree(mpe):
 */
