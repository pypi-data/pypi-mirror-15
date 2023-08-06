#include<utility>
#include<vector>
#include<utility>
#include<iostream>
#include<memory>
#include<limits>
#include<sstream>
#include<string>
#include<Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include<numpy/arrayobject.h>

#include "calcSignature.hpp"
#include "logSigLength.hpp"
#include "logsig.hpp"

#if PY_MAJOR_VERSION <3 && PY_MINOR_VERSION<7
  #define NO_CAPSULES
#endif

//consider  PyErr_CheckSignals()
// for python 3.5+, we can load the new way https://www.python.org/dev/peps/pep-0489/
//This is a python addin to calculate signatures which doesn't use boost python - to be as widely buildable as possible.
//It should be buildable on tinis.

#define ERR(X) {PyErr_SetString(PyExc_RuntimeError,X); return nullptr;}
#define ERRb(X) {PyErr_SetString(PyExc_RuntimeError,X); return false;}

class Deleter{
  PyObject* m_p;
public:
  Deleter(PyObject* p):m_p(p){};
  Deleter(const Deleter&)=delete;
  Deleter operator=(const Deleter&) = delete;
  ~Deleter(){Py_DECREF(m_p);}
};

static PyObject *
version(PyObject *self, PyObject *args){
  //consider returning build time?
  return PyUnicode_FromString(VERSION);
}

static PyObject *
siglength(PyObject *self, PyObject *args){
  int d=0, m=0;
  if (!PyArg_ParseTuple(args, "ii", &d, &m))
    return NULL;
  if(m<1) ERR("level must be positive");
  if(d<1) ERR("dimension must be positive");
  long ans = calcSigTotalLength(d,m);
  //todo - cope with overrun here
#if PY_MAJOR_VERSION >= 3
  return PyLong_FromLong(ans);
#else
  return PyInt_FromLong(ans);
#endif
}


static PyObject *
logsiglength(PyObject *self, PyObject *args){
  int d=0, m=0;
  if (!PyArg_ParseTuple(args, "ii", &d, &m))
    return NULL;
  if(m<1) ERR("level must be positive");
  if(d<1) ERR("dimension must be positive");
  LogSigLength::Int ans = d==1 ? 1 : m==1 ? d : LogSigLength::countNecklacesUptoLengthM(d,m);
  if(ans>std::numeric_limits<long>::max()) ERR("overflow");
  //todo - cope with overrun here
#if PY_MAJOR_VERSION >= 3
  return PyLong_FromLong((long)ans);
#else
  return PyInt_FromLong((long)ans);
#endif
}

//returns true on success
//makes s2 be the signature of the path in data
static bool calcSignature(CalculatedSignature& s2, PyObject* data, int level){
  if(!PyArray_Check(data)) ERRb("data must be a numpy array");
  //PyArrayObject* a = reinterpret_cast<PyArrayObject*>(a1);
  PyArrayObject* a = PyArray_GETCONTIGUOUS(reinterpret_cast<PyArrayObject*>(data));
  Deleter a_(reinterpret_cast<PyObject*>(a));
  if(PyArray_NDIM(a)!=2) ERRb("data must be 2d");
  if(PyArray_TYPE(a)!=NPY_FLOAT32 && PyArray_TYPE(a)!=NPY_FLOAT64) ERRb("data must be float32 or float64");
  const int lengthOfPath = PyArray_DIM(a,0);
  const int d = PyArray_DIM(a,1);
  if(lengthOfPath<1) ERRb("Path has no length");
  if(d<1) ERRb("Path must have positive dimension");
  CalculatedSignature s1;

  if(lengthOfPath==1){
    s2.sigOfNothing(d,level);
  }

  if(PyArray_TYPE(a)==NPY_FLOAT32){
    vector<float> displacement(d);
    float* data = static_cast<float*>(PyArray_DATA(a));
    for(int i=1; i<lengthOfPath; ++i){
      for(int j=0;j<d; ++j)
        displacement[j]=data[i*d+j]-data[(i-1)*d+j];
      s1.sigOfSegment(d,level,&displacement[0]);
      if(i==1)
	s2.swap(s1);
      else
	s2.concatenateWith(d,level,s1);
    }
  }else{
    vector<double> displacement(d);
    double* data = static_cast<double*>(PyArray_DATA(a));
    for(int i=1; i<lengthOfPath; ++i){
      for(int j=0;j<d; ++j)
        displacement[j]=data[i*d+j]-data[(i-1)*d+j];
      s1.sigOfSegment(d,level,&displacement[0]);
      if(i==1)
	s2.swap(s1);
      else
	s2.concatenateWith(d,level,s1);
    }
  }
  return true;
}

static PyObject *
sig(PyObject *self, PyObject *args){
  PyObject* a1;
  int level=0;
  if (!PyArg_ParseTuple(args, "Oi", &a1, &level))
    return NULL;
  if(level<1) ERR("level must be positive");

  CalculatedSignature s;
  if(!calcSignature(s,a1,level))
    return NULL;
  
  long d = s.m_data[0].size();
  long dims[] = {(long) calcSigTotalLength(d,level)};
  PyObject* o = PyArray_SimpleNew(1,dims,NPY_FLOAT32);
  s.writeOut(static_cast<float*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(o))));
  return o;
}

const char* const logSigFunction_id = "iisignature.LogSigFunction";
LogSigFunction* getLogSigFunction(PyObject* p){
#ifdef NO_CAPSULES
  if(!PyCObject_Check(p))
    ERR("I have received an input which is not from iisignature.prepare()");
  return (LogSigFunction*) PyCObject_AsVoidPtr(p);
#else
  if(!PyCapsule_CheckExact(p))
    ERR("I have received an input which is not from iisignature.prepare()");
  return (LogSigFunction*) PyCapsule_GetPointer(p,logSigFunction_id);
#endif
} 

static void killLogSigFunction(PyObject* p){
  delete getLogSigFunction(p);
}

static PyObject *
prepare(PyObject *self, PyObject *args){
  int level=0, dim=0;
  const char* methods = nullptr;
  if (!PyArg_ParseTuple(args, "ii|z", &dim, &level, &methods))
    return NULL;
  WantedMethods wantedmethods;
  if(methods)
    if(setWantedMethods(wantedmethods,methods))
      ERR(methodError);
  if(dim<2) ERR("dimension must be at least 2");
  if(level<1) ERR("level must be positive");
  std::unique_ptr<LogSigFunction> lsf(new LogSigFunction);
  std::string exceptionMessage;
  Py_BEGIN_ALLOW_THREADS
  try{
    makeLogSigFunction(dim,level,*lsf, wantedmethods);
  }catch(std::exception& e){
    exceptionMessage = e.what();
  }
  Py_END_ALLOW_THREADS
  if(!exceptionMessage.empty())
    ERR(exceptionMessage.c_str());
#ifdef NO_CAPSULES
  PyObject * out = PyCObject_FromVoidPtr(lsf.release(), killLogSigFunction);
#else
  PyObject * out = PyCapsule_New(lsf.release(), logSigFunction_id, killLogSigFunction);
#endif
  return out;
}

static PyObject* basis(PyObject *self, PyObject *args){
  PyObject* c;
  if(!PyArg_ParseTuple(args,"O",&c))
    return NULL;
  LogSigFunction* lsf = getLogSigFunction(c);
  if(!lsf)
    return NULL;
  auto& wordlist = lsf->m_basisWords;
  PyObject* o = PyTuple_New(wordlist.size());
  for(size_t i=0; i<wordlist.size(); ++i){
    std::ostringstream oss;
    printLyndonWordBracketsDigits(*wordlist[i],oss);
    std::string s = oss.str();
    PyTuple_SET_ITEM(o,i,PyUnicode_FromString(s.c_str()));
  }
  return o;
}

//this function is basically just numpy.linalg.lstsq
static PyObject* lstsq(PyObject *a1, PyObject *a2){
  PyObject* numpy = PyImport_AddModule("numpy");
  if(!numpy)
    return NULL;
  PyObject* linalg = PyObject_GetAttrString(numpy,"linalg");
  if(!linalg)
    return NULL;
  Deleter linalg_(linalg);
  PyObject* transpose = PyObject_GetAttrString(numpy,"transpose");
  if(!transpose)
    return NULL;
  Deleter transpose_(transpose);
  PyObject* lstsq = PyObject_GetAttrString(linalg,"lstsq");
  if(!lstsq)
    return NULL;
  Deleter lstsq_(lstsq);
  PyObject* a1t = PyObject_CallFunctionObjArgs(transpose,a1,NULL);
  if(!a1t)
    return NULL;
  Deleter a1t_(a1t);
  PyObject* o = PyObject_CallFunctionObjArgs(lstsq,a1t,a2,NULL); 
  //return o;
  //return PyTuple_Pack(2,o,a1);
  Deleter o_(o);
  PyObject* answer = PyTuple_GetItem(o,0);
  Py_INCREF(answer);
  return answer;
}

static PyObject *
logsig(PyObject *self, PyObject *args){
  PyObject* a1, *a2;
  const char* methods = nullptr;
  if (!PyArg_ParseTuple(args, "OO|z", &a1, &a2, &methods))
    return NULL;
  WantedMethods wantedmethods;
  if(methods)
    if(setWantedMethods(wantedmethods,methods))
      ERR(methodError);
  if(!PyArray_Check(a1)) ERR("data must be a numpy array");
  //PyArrayObject* a = reinterpret_cast<PyArrayObject*>(a1);
  PyArrayObject* a = PyArray_GETCONTIGUOUS(reinterpret_cast<PyArrayObject*>(a1));
  Deleter a_(reinterpret_cast<PyObject*>(a));
  if(PyArray_NDIM(a)!=2) ERR("data must be 2d");
  if(PyArray_TYPE(a)!=NPY_FLOAT32 && PyArray_TYPE(a)!=NPY_FLOAT64) ERR("data must be float32 or float64");
  const int lengthOfPath = PyArray_DIM(a,0);
  LogSigFunction* lsf = getLogSigFunction(a2);
  if(!lsf)
    return NULL;
  const int d = PyArray_DIM(a,1);
  if(lengthOfPath<1) ERR("Path has no length");
  if(d!=lsf->m_dim) 
    ERR(("Path has dimension "+std::to_string(d)+" but we prepared for dimension "+std::to_string(lsf->m_dim)).c_str());
  size_t logsiglength = lsf->m_basisWords.size();
  vector<double> out(logsiglength);//why double

  FunctionRunner* f = lsf->m_f.get();
  if ((wantedmethods.m_compiled_bch && f!=nullptr) || (wantedmethods.m_simple_bch && !lsf->m_fd.m_formingT.empty())){
    vector<double> displacement(d);
    const bool useCompiled = (f!=nullptr && wantedmethods.m_compiled_bch);

    if(PyArray_TYPE(a)==NPY_FLOAT32){
      float* data = static_cast<float*>(PyArray_DATA(a));
      if(lengthOfPath>0){
	for(int j=0; j<d; ++j)
	  out[j]=data[1*d+j]-data[0*d+j];
      }
      for(int i=2; i<lengthOfPath; ++i){
	for(int j=0;j<d; ++j)
	  displacement[j]=data[i*d+j]-data[(i-1)*d+j];
	if(useCompiled)
	  f->go(out.data(),displacement.data());
	else
	  slowExplicitFunction(out.data(), displacement.data(), lsf->m_fd);
      }
    }else{
      double* data = static_cast<double*>(PyArray_DATA(a));
      if(lengthOfPath>0){
	for(int j=0; j<d; ++j)
	  out[j]=data[1*d+j]-data[0*d+j];
      }
      for(int i=2; i<lengthOfPath; ++i){
	for(int j=0;j<d; ++j)
	  displacement[j]=data[i*d+j]-data[(i-1)*d+j];
	if(useCompiled)
	  f->go(out.data(),displacement.data());
	else
	  slowExplicitFunction(out.data(), displacement.data(), lsf->m_fd);
      }
    }
    long dims[] = {(long)out.size()};
    PyObject* o = PyArray_SimpleNew(1,dims,NPY_FLOAT32);
    float* dest = static_cast<float*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(o)));
    for(double d : out)
      *dest++ = (float) d;
    return o;
  }
  if((wantedmethods.m_log_of_signature || wantedmethods.m_expanded) && !lsf->m_expandedBasis.empty() ){
    CalculatedSignature sig;
    calcSignature(sig,a1,lsf->m_level);
    logTensor(sig);
    long siglength = (long) calcSigTotalLength(lsf->m_dim,lsf->m_level);
    long dims[] = {siglength};
    PyObject* flattenedFullLogSigAsNumpyArray = PyArray_SimpleNew(1,dims,NPY_FLOAT64);
    //PyObject* flattenedFullLogSigAsNumpyArray = PyArray_SimpleNew(1,dims,NPY_FLOAT32);
    sig.writeOut(static_cast<double*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(flattenedFullLogSigAsNumpyArray))));
    //sig.writeOut(static_cast<float*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(flattenedFullLogSigAsNumpyArray))));
    if(wantedmethods.m_expanded)
      return flattenedFullLogSigAsNumpyArray;
    Deleter f_(flattenedFullLogSigAsNumpyArray);

    long dims2[] = {(long)logsiglength,siglength};
    PyObject* mat = PyArray_SimpleNewFromData(2,dims2,NPY_FLOAT32,lsf->m_expandedBasis.data());
    Deleter m_(mat);

    PyObject* ans = lstsq(mat,flattenedFullLogSigAsNumpyArray);
    return ans;
    //Deleter ans_(ans); 
    //return PyTuple_Pack(3,ans,mat,flattenedFullLogSigAsNumpyArray);
  }
  ERR("We had not prepare()d for this request type");
}

#define METHOD_DESC "some combination of 'd' (the default, compiled bch formula), 'o' (the bch formula evaluated simply and stored in an object without on-the-fly compilation and perhaps more slowly), and 's' (calculating the log signature by first calculating the signature and then taking its log, which may be faster for high levels or long paths)"

static PyMethodDef Methods[] = {
  {"sig",  sig, METH_VARARGS, "sig(X,m)\n Returns the signature of a path X up to level m. X must be a numpy NxD float32 or float64 array of points making up the path in R^d. The initial 1 in the zeroth level of the signature is excluded."},
  {"siglength", siglength, METH_VARARGS, "siglength(d,m) \n Returns the length of the signature (excluding the initial 1) of a d dimensional path up to level m"},
  {"logsiglength", logsiglength, METH_VARARGS, "logsiglength(d,m) \n Returns the length of the log signature of a d dimensional path up to level m"},
  {"prepare", prepare, METH_VARARGS, "prepare(d, m, methods=None) \n  This prepares the way to calculate log signatures of d dimensional paths up to level m. The returned object is used in the logsig and basis functions. \n By default, all methods whill be prepared, but you can restrict it by setting methods to " METHOD_DESC "."}, 
  {"basis", basis, METH_VARARGS, "basis(s) \n  Returns a tuple of strings which are the basis elements of the log signature. s must have come from prepare. This function is work in progress, especially for dimension greater than 8. An example of how to parse the output of this function can be seen in the tests."},
  {"logsig", logsig, METH_VARARGS, "logsig(X, s, methods=None) \n  Calculates the log signature of the path X. X must be a numpy NxD float32 or float64 array of points making up the path in R^d. s must have come from prepare(D,m) for some m. The value is returned as a 1D numpy array of its log signature up to level m. By default, the method used is the default out of those which have been prepared, but you can restrict it by setting methods to " METHOD_DESC "."},
  {"version", version, METH_NOARGS, "return the iisignature version string"},
  {NULL, NULL, 0, NULL}        /* Sentinel */
};

#define MODULEDOC "iisignature: Iterated integral signature and logsignature calculations\n\nPlease find documentation at http://www2.warwick.ac.uk/jreizenstein and code at https://github.com/bottler/iisignature."

#if PY_MAJOR_VERSION >= 3
 static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
    "iisignature",     /* m_name */
    MODULEDOC,  /* m_doc */
    -1,                  /* m_size */
    Methods,    /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
    };

PyMODINIT_FUNC
PyInit_iisignature(void){
  import_array();
  return PyModule_Create(&moduledef);
}
#else

/*extern "C" __attribute__ ((visibility ("default"))) void */
PyMODINIT_FUNC
initiisignature(void)
{
  import_array();
  (void) Py_InitModule3("iisignature", Methods, MODULEDOC);
}

#endif

/*
thinking about builds:
According to
http://python-packaging-user-guide.readthedocs.io/en/latest/distributing/#requirements-for-packaging-and-distributing
we can't distribute platform wheels on linux.
Basically we can only distribute source.
 Therefore we won't make wheels

 Build just with 
python setup.py sdist

*/
