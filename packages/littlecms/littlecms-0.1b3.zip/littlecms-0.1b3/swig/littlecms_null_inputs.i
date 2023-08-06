/* Throw exceptions for null parameter inputs using typemap checks */

%include exception.i

%typemap(check) char* AccessMode {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL AccessMode.");
    }
}
%typemap(check) char* ASCIIString {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL ASCIIString.");
    }
}
%typemap(check) cmsCIEXYZ* BlackPoint {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL BlackPoint.");
    }
}
%typemap(check) (void* Buffer, cmsUInt32Number BufferSize) {
    /* NULL Buffer is handled IFF BufferSize == 0 */
    if ($1 == 0 && $2 != 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
%typemap(check) (void* Buffer, cmsUInt32Number dwBufferLen) {
    /* NULL Buffer is handled IFF dwBufferLen == 0 */
    if ($1 == 0 && $2 != 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
%typemap(check) void* Buffer {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
%typemap(check) (char* Buffer, cmsUInt32Number BufferSize) {
    /* NULL Buffer is handled IFF BufferSize == 0 */
    if ($1 == 0 && $2 != 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
%typemap(check) char* Buffer {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
/* char* buffer
   NULL value is handled
*/
%typemap(check) (wchar_t* Buffer, cmsUInt32Number BufferSize) {
    /* NULL Buffer is handled IFF BufferSize == 0 */
    if ($1 == 0 && $2 != 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
%typemap(check) wchar_t* Buffer {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Buffer.");
    }
}
%typemap(check) cmsUInt32Number* BytesNeeded {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL BytesNeeded.");
    }
}
%typemap(check) char* cComment {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL cComment.");
    }
}
%typemap(check) char* cFileName {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL cFileName.");
    }
}
%typemap(check) (cmsUInt32Number* Codes, char** Descriptions) {
    /* Both Codes and Descriptions may be NULL, but not only one of them */
    if (($1 == 0) != ($2 == 0)) {
        SWIG_exception(SWIG_ValueError, "NULL Codes or Descriptions.");
    }
}
%typemap(check) cmsUInt32Number* Codes {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Codes.");
    }
}
%typemap(check) cmsUInt16Number* Colorant {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Colorant.");
    }
}
%typemap(check) cmsContext ContextID {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL ContextID.");
    }
}
%typemap(check) char* cPatch {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL cPatch.");
    }
}
%typemap(check) char* cProp {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL cProp.");
    }
}
%typemap(check) char* cSample {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL cSample.");
    }
}
%typemap(check) cmsToneCurve* Curve {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Curve.");
    }
}
/* void* data
   NULL value is handled
*/
%typemap(check) char** Descriptions {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Descriptions.");
    }
}
%typemap(check) struct tm* Dest {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Dest.");
    }
}
%typemap(check) cmsCIExyY* Dest {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Dest.");
    }
}
%typemap(check) cmsCIEXYZ* Dest {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Dest.");
    }
}
%typemap(check) cmsMLU* DisplayName {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL DisplayName.");
    }
}
%typemap(check) cmsMLU* DisplayValue {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL DisplayValue.");
    }
}
%typemap(check) cmsDICTentry* e {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL e.");
    }
}
%typemap(check) char* FileName {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL FileName.");
    }
}
%typemap(check) cmsUInt64Number* Flags {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Flags.");
    }
}
%typemap(check) char* Formatter {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Formatter.");
    }
}
%typemap(check) cmsCIEXYZ* fxyz {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL fxyz.");
    }
}
%typemap(check) cmsHPROFILE hProfile {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL hProfile.");
    }
}
%typemap(check) cmsHTRANSFORM hTransform {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL hTransform.");
    }
}
%typemap(check) char* ICCProfile {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL ICCProfile.");
    }
}
%typemap(check) cmsToneCurve* InGamma {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL InGamma.");
    }
}
%typemap(check) void* InputBuffer {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL InputBuffer.");
    }
}
%typemap(check) cmsIOHANDLER* io {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL io.");
    }
}
%typemap(check) char* Key {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Key.");
    }
}
%typemap(check) cmsCIELab* Lab {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Lab.");
    }
}
%typemap(check) cmsCIELab* Lab1 {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Lab1.");
    }
}
%typemap(check) cmsCIELab* Lab2 {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Lab2.");
    }
}
%typemap(check) cmsCIELCh* LCh {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL LCh.");
    }
}
%typemap(check) cmsPipeline* lut {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL lut.");
    }
}
%typemap(check) cmsFloat64Number* Matrix {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Matrix.");
    }
}
%typemap(check) (void* MemPtr, cmsUInt32Number* BytesNeeded) {
    /* NULL MemPtr is handled, BytesNeeded must be non-NULL */
    if ($2 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL BytesNeeded.");
    }
}
%typemap(check) void* MemPtr {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL MemPtr.");
    }
}
%typemap(check) cmsMLU* mlu {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL mlu.");
    }
}
%typemap(check) cmsStage* mpe {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL mpe.");
    }
}
/* cmsStage** mpe
   NULL value is handled
*/
%typemap(check) (char* Name, char* Prefix, char* Suffix, cmsUInt16Number* PCS, cmsUInt16Number* Colorant) {
   /* NULL values of all of these params are handled in cmsNamedColorInfo */
}
%typemap(check) char* Name {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Name.");
    }
}
%typemap(check) (const wchar_t* Name, const wchar_t* Value, const cmsMLU* DisplayName, const cmsMLU* DisplayValue) {
   /* NULL values of all of these params are handled in cmsDictAddEntry */
}
%typemap(check) wchar_t* Name {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Name.");
    }
}
/* void* NewUserData
   NULL value is handled
*/
/* cmsFloat64Number* Offset
   NULL value is handled
*/
%typemap(check) void* OutputBuffer {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL OutputBuffer,.");
    }
}
%typemap(check) cmsUInt16Number* PCS {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL PCS,.");
    }
}
%typemap(check) cmsCIEXYZ* pIn {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL pIn.");
    }
}
%typemap(check) cmsJCh* pIn {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL pIn.");
    }
}
/* void* Plugin
   NULL value is handled
*/
%typemap(check) cmsCIEXYZ* pOut {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL pOut.");
    }
}
%typemap(check) cmsJCh* pOut {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL pOut.");
    }
}
%typemap(check) char* Prefix {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Prefix.");
    }
}
%typemap(check) cmsCIExyYTRIPLE* Primaries {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Primaries.");
    }
}
%typemap(check) cmsUInt8Number* ProfileID {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL ProfileID.");
    }
}
%typemap(check) char*** PropertyNames {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL PropertyNames.");
    }
}
%typemap(check) cmsSEQ* pseq {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL pseq.");
    }
}
%typemap(check) void* Ptr {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Ptr.");
    }
}
%typemap(check) cmsViewingConditions* pVC {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL pVC.");
    }
}
%typemap(check) char* sAccess {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL sAccess.");
    }
}
/* char*** SampleNames
   NULL value is handled
*/
%typemap(check) cmsCIExyY* Source {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Source.");
    }
}
%typemap(check) cmsCIEXYZ* Source {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Source.");
    }
}
%typemap(check) FILE* Stream {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Stream.");
    }
}
%typemap(check) char* Str {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Str.");
    }
}
%typemap(check) char* SubKey {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL SubKey.");
    }
}
%typemap(check) char*** SubpropertyNames {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL SubpropertyNames.");
    }
}
%typemap(check) char* Suffix {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Suffix.");
    }
}
%typemap(check) cmsToneCurve* t {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL t.");
    }
}
%typemap(check) cmsToneCurve* Tab {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Tab.");
    }
}
/* cmsUInt16Number* Table
   NULL value is handled
*/
/* cmsFloat32Number* Table
   NULL value is handled
*/
%typemap(check) cmsToneCurve* TransferFunction {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL TransferFunction.");
    }
}
%typemap(check) char* Type {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Type.");
    }
}
/* void* UserData
   NULL value is handled
*/
%typemap(check) cmsNAMEDCOLORLIST* v {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL v.");
    }
}
%typemap(check) char* Val {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Val.");
    }
}
%typemap(check) wchar_t* Value {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Value.");
    }
}
%typemap(check) cmsCIExyY* WhitePoint {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL WhitePoint.");
    }
}
%typemap(check) cmsCIEXYZ* WhitePoint {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL WhitePoint.");
    }
}
%typemap(check) wchar_t* WideString {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL WideString.");
    }
}
%typemap(check) cmsToneCurve* X {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL X.");
    }
}
%typemap(check) cmsToneCurve* Y {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL Y.");
    }
}
%typemap(check) cmsCIEXYZ* xyz {
    if ($1 == 0) {
        SWIG_exception(SWIG_ValueError, "NULL xyz.");
    }
}
