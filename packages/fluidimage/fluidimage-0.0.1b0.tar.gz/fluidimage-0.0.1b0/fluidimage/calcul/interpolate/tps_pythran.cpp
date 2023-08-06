#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/include/numpy/log.hpp>
#include <pythonic/include/__builtin__/assert.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/__builtin__/xrange.hpp>
#include <pythonic/include/__builtin__/enumerate.hpp>
#include <pythonic/include/numpy/ones.hpp>
#include <pythonic/include/__builtin__/str.hpp>
#include <pythonic/numpy/log.hpp>
#include <pythonic/__builtin__/assert.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/__builtin__/xrange.hpp>
#include <pythonic/__builtin__/enumerate.hpp>
#include <pythonic/numpy/ones.hpp>
#include <pythonic/__builtin__/str.hpp>
namespace __pythran_tps_pythran
{
  ;
  ;
  ;
  ;
  struct compute_tps_matrix
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>()))>::type __type0;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type>::type __type1;
      typedef long __type2;
      typedef decltype((std::declval<__type1>() + std::declval<__type2>())) __type3;
      typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>()))>::type __type4;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type>::type __type5;
      typedef decltype((std::declval<__type3>() + std::declval<__type5>())) __type6;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type>::type __type7;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type7>())) __type8;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type>()(std::declval<__type8>()))>::type __type9;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type>()(std::declval<__type7>())) __type10;
      typedef container<typename std::remove_reference<__type10>::type> __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type1>(), std::declval<__type7>())) __type12;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type>()(std::declval<__type12>()))>::type __type13;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type14;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type5>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef decltype(std::declval<__type14>()[std::declval<__type16>()]) __type17;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::enumerate{})>::type>::type>()(std::declval<__type17>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type19>::type>::type>::type __type20;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type1>())) __type21;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type __type22;
      typedef typename __combined<__type20,__type22>::type __type23;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type7>())) __type24;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type24>::type::iterator>::value_type>::type __type25;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type23>(), std::declval<__type25>())) __type26;
      typedef indexable<__type26> __type27;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type28;
      typedef decltype(std::declval<__type28>()[std::declval<__type16>()]) __type29;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::enumerate{})>::type>::type>()(std::declval<__type29>())) __type30;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type30>::type::iterator>::value_type>::type __type31;
      typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type31>::type>::type>::type __type32;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type20>(), std::declval<__type32>())) __type33;
      typedef indexable<__type33> __type34;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type31>::type>::type __type37;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type19>::type>::type>::type __type38;
      typedef decltype((std::declval<__type37>() - std::declval<__type38>())) __type39;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type>()(std::declval<__type39>())) __type40;
      typedef container<typename std::remove_reference<__type40>::type> __type41;
      typedef typename __combined<__type13,__type34,__type41>::type __type43;
      typedef typename pythonic::assignable<decltype(std::declval<__type43>()[std::declval<__type26>()])>::type __type46;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type>()(std::declval<__type46>())) __type47;
      typedef decltype((std::declval<__type46>() * std::declval<__type47>())) __type48;
      typedef decltype((std::declval<__type48>() / std::declval<__type2>())) __type50;
      typedef container<typename std::remove_reference<__type50>::type> __type51;
      typedef typename __combined<__type13,__type27,__type34,__type41,__type51>::type __type53;
      typedef container<typename std::remove_reference<__type53>::type> __type54;
      typedef container<typename std::remove_reference<__type28>::type> __type55;
      typedef typename pythonic::returnable<typename __combined<__type9,__type54,__type55>::type>::type result_type;
    }
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0 const & new_pos, argument_type1 const & centers) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 >
  typename compute_tps_matrix::type<argument_type0, argument_type1>::result_type compute_tps_matrix::operator()(argument_type0 const & new_pos, argument_type1 const & centers) const
  {
    typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>()))>::type __type0;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type>::type __type1;
    typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>()))>::type __type2;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type>::type __type3;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type1>(), std::declval<__type3>())) __type4;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type>()(std::declval<__type4>()))>::type __type5;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type6;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type>::type __type7;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type7>())) __type8;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type __type9;
    typedef decltype(std::declval<__type6>()[std::declval<__type9>()]) __type10;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::enumerate{})>::type>::type>()(std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type12>::type>::type>::type __type13;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type1>())) __type14;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
    typedef typename __combined<__type13,__type15>::type __type16;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type3>())) __type17;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type17>::type::iterator>::value_type>::type __type18;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type16>(), std::declval<__type18>())) __type19;
    typedef indexable<__type19> __type20;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type21;
    typedef decltype(std::declval<__type21>()[std::declval<__type9>()]) __type22;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::enumerate{})>::type>::type>()(std::declval<__type22>())) __type23;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type23>::type::iterator>::value_type>::type __type24;
    typedef typename pythonic::lazy<typename std::tuple_element<0,typename std::remove_reference<__type24>::type>::type>::type __type25;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type13>(), std::declval<__type25>())) __type26;
    typedef indexable<__type26> __type27;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type24>::type>::type __type30;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type12>::type>::type>::type __type31;
    typedef decltype((std::declval<__type30>() - std::declval<__type31>())) __type32;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type>()(std::declval<__type32>())) __type33;
    typedef container<typename std::remove_reference<__type33>::type> __type34;
    typedef typename __combined<__type5,__type27,__type34>::type __type36;
    typedef typename pythonic::assignable<decltype(std::declval<__type36>()[std::declval<__type19>()])>::type __type39;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::log{})>::type>::type>()(std::declval<__type39>())) __type40;
    typedef decltype((std::declval<__type39>() * std::declval<__type40>())) __type41;
    typedef long __type42;
    typedef decltype((std::declval<__type41>() / std::declval<__type42>())) __type43;
    typedef container<typename std::remove_reference<__type43>::type> __type44;
    typedef decltype((std::declval<__type1>() + std::declval<__type42>())) __type47;
    typedef decltype((std::declval<__type47>() + std::declval<__type7>())) __type48;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type48>(), std::declval<__type3>())) __type49;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type>()(std::declval<__type49>()))>::type __type50;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::ones{})>::type>::type>()(std::declval<__type3>())) __type51;
    typedef container<typename std::remove_reference<__type51>::type> __type52;
    typedef typename __combined<__type5,__type20,__type27,__type34,__type44>::type __type53;
    typedef container<typename std::remove_reference<__type53>::type> __type54;
    typedef container<typename std::remove_reference<__type21>::type> __type55;
    typename pythonic::assignable<typename __combined<__type13,__type15>::type>::type ic;
    typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(new_pos))>::type __tuple0 = pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(new_pos);
    typename pythonic::assignable<decltype(std::get<0>(__tuple0))>::type d = std::get<0>(__tuple0);
    typename pythonic::assignable<decltype(std::get<1>(__tuple0))>::type nb_new_pos = std::get<1>(__tuple0);
    typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(centers))>::type __tuple1 = pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(centers);
    ;
    typename pythonic::assignable<decltype(std::get<1>(__tuple1))>::type nb_centers = std::get<1>(__tuple1);
    pythonic::pythran_assert(d == std::get<0>(__tuple1));
    typename pythonic::assignable<typename __combined<__type5,__type20,__type27,__type34,__type44>::type>::type EM = pythonic::numpy::functor::zeros{}(pythonic::types::make_tuple(nb_centers, nb_new_pos));
    {
      long  __target1 = d;
      for (long  ind_d = 0L; ind_d < __target1; ind_d += 1L)
      {
        {
          for (auto&& __tuple2: pythonic::__builtin__::functor::enumerate{}(centers[ind_d]))
          {
            ic = std::get<0>(__tuple2);
            typename pythonic::assignable<decltype(std::get<1>(__tuple2))>::type center = std::get<1>(__tuple2);
            {
              for (auto&& __tuple3: pythonic::__builtin__::functor::enumerate{}(new_pos[ind_d]))
              {
                ;
                typename pythonic::lazy<decltype(std::get<0>(__tuple3))>::type inp = std::get<0>(__tuple3);
                EM[pythonic::types::make_tuple(ic, inp)] += pythonic::numpy::functor::square{}((std::get<1>(__tuple3) - center));
              }
            }
          }
        }
      }
    }
    {
      long  __target1 = nb_centers;
      for ( ic = 0L; ic < __target1; ic += 1L)
      {
        {
          long  __target2 = nb_new_pos;
          for (long  inp_ = 0L; inp_ < __target2; inp_ += 1L)
          {
            typename pythonic::assignable<typename pythonic::assignable<decltype(std::declval<__type36>()[std::declval<__type19>()])>::type>::type tmp = EM[pythonic::types::make_tuple(ic, inp_)];
            if (tmp != 0L)
            {
              EM[pythonic::types::make_tuple(ic, inp_)] = ((tmp * pythonic::numpy::functor::log{}(tmp)) / 2L);
            }
          }
        }
      }
      if (ic == __target1)
      ic -= 1L;
    }
    typename pythonic::assignable<typename __combined<__type50,__type54,__type55>::type>::type EM_ret = pythonic::numpy::functor::empty{}(pythonic::types::make_tuple(((nb_centers + 1L) + d), nb_new_pos));
    EM_ret(pythonic::types::contiguous_slice(pythonic::__builtin__::None,nb_centers),pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)) = EM;
    EM_ret(nb_centers,pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)) = pythonic::numpy::functor::ones{}(nb_new_pos);
    EM_ret(pythonic::types::contiguous_slice((nb_centers + 1L),((nb_centers + 1L) + d)),pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None)) = new_pos;
    return EM_ret;
  }
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type compute_tps_matrix0(pythonic::types::ndarray<double,2> a0, pythonic::types::ndarray<double,2> a1)
{
  return __pythran_tps_pythran::compute_tps_matrix()(a0, a1);
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type compute_tps_matrix1(pythonic::types::ndarray<double,2> a0, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> a1)
{
  return __pythran_tps_pythran::compute_tps_matrix()(a0, a1);
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type compute_tps_matrix2(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> a0, pythonic::types::ndarray<double,2> a1)
{
  return __pythran_tps_pythran::compute_tps_matrix()(a0, a1);
}
typename __pythran_tps_pythran::compute_tps_matrix::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type compute_tps_matrix3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> a0, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>> a1)
{
  return __pythran_tps_pythran::compute_tps_matrix()(a0, a1);
}

                static PyObject *
                __pythran_wrap_compute_tps_matrix0(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[2+1];
                    if(! PyArg_ParseTuple(args, "OO", &args_obj[0], &args_obj[1]))
                        return nullptr;
                    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]))
                        return to_python(compute_tps_matrix0(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1])));
                    else {
                        return nullptr;
                    }
                }

                static PyObject *
                __pythran_wrap_compute_tps_matrix1(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[2+1];
                    if(! PyArg_ParseTuple(args, "OO", &args_obj[0], &args_obj[1]))
                        return nullptr;
                    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]))
                        return to_python(compute_tps_matrix1(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1])));
                    else {
                        return nullptr;
                    }
                }

                static PyObject *
                __pythran_wrap_compute_tps_matrix2(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[2+1];
                    if(! PyArg_ParseTuple(args, "OO", &args_obj[0], &args_obj[1]))
                        return nullptr;
                    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]))
                        return to_python(compute_tps_matrix2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1])));
                    else {
                        return nullptr;
                    }
                }

                static PyObject *
                __pythran_wrap_compute_tps_matrix3(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[2+1];
                    if(! PyArg_ParseTuple(args, "OO", &args_obj[0], &args_obj[1]))
                        return nullptr;
                    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]))
                        return to_python(compute_tps_matrix3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1])));
                    else {
                        return nullptr;
                    }
                }

            static PyObject *
            __pythran_wrapall_compute_tps_matrix(PyObject *self, PyObject *args)
            {
                try {
                
                    if(PyObject* obj = __pythran_wrap_compute_tps_matrix0(self, args))
                        return obj;
                    

                    if(PyObject* obj = __pythran_wrap_compute_tps_matrix1(self, args))
                        return obj;
                    

                    if(PyObject* obj = __pythran_wrap_compute_tps_matrix2(self, args))
                        return obj;
                    

                    if(PyObject* obj = __pythran_wrap_compute_tps_matrix3(self, args))
                        return obj;
                    
                PyErr_SetString(PyExc_TypeError,
                  "Invalid argument type for pythranized function `compute_tps_matrix'.\n"
                  "Candidates are:\n   compute_tps_matrix(ndarray<double,2>,ndarray<double,2>)\n   compute_tps_matrix(ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   compute_tps_matrix(numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   compute_tps_matrix(numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                }
                
            #ifdef PYTHONIC_BUILTIN_BASEEXCEPTION_HPP
                catch(pythonic::types::BaseException & e) {
                    PyErr_SetString(PyExc_BaseException,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_SYSTEMEXIT_HPP
                catch(pythonic::types::SystemExit & e) {
                    PyErr_SetString(PyExc_SystemExit,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_KEYBOARDINTERRUPT_HPP
                catch(pythonic::types::KeyboardInterrupt & e) {
                    PyErr_SetString(PyExc_KeyboardInterrupt,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_EXCEPTION_HPP
                catch(pythonic::types::Exception & e) {
                    PyErr_SetString(PyExc_Exception,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_STANDARDERROR_HPP
                catch(pythonic::types::StandardError & e) {
                    PyErr_SetString(PyExc_StandardError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_IMPORTERROR_HPP
                catch(pythonic::types::ImportError & e) {
                    PyErr_SetString(PyExc_ImportError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_REFERENCEERROR_HPP
                catch(pythonic::types::ReferenceError & e) {
                    PyErr_SetString(PyExc_ReferenceError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_ASSERTIONERROR_HPP
                catch(pythonic::types::AssertionError & e) {
                    PyErr_SetString(PyExc_AssertionError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_RUNTIMEERROR_HPP
                catch(pythonic::types::RuntimeError & e) {
                    PyErr_SetString(PyExc_RuntimeError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_NOTIMPLEMENTEDERROR_HPP
                catch(pythonic::types::NotImplementedError & e) {
                    PyErr_SetString(PyExc_NotImplementedError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_SYNTAXERROR_HPP
                catch(pythonic::types::SyntaxError & e) {
                    PyErr_SetString(PyExc_SyntaxError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_INDENTATIONERROR_HPP
                catch(pythonic::types::IndentationError & e) {
                    PyErr_SetString(PyExc_IndentationError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_TYPEERROR_HPP
                catch(pythonic::types::TypeError & e) {
                    PyErr_SetString(PyExc_TypeError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_ENVIRONMENTERROR_HPP
                catch(pythonic::types::EnvironmentError & e) {
                    PyErr_SetString(PyExc_EnvironmentError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_IOERROR_HPP
                catch(pythonic::types::IOError & e) {
                    PyErr_SetString(PyExc_IOError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_SYSTEMERROR_HPP
                catch(pythonic::types::SystemError & e) {
                    PyErr_SetString(PyExc_SystemError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_EOFERROR_HPP
                catch(pythonic::types::EOFError & e) {
                    PyErr_SetString(PyExc_EOFError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_ATTRIBUTEERROR_HPP
                catch(pythonic::types::AttributeError & e) {
                    PyErr_SetString(PyExc_AttributeError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_NAMEERROR_HPP
                catch(pythonic::types::NameError & e) {
                    PyErr_SetString(PyExc_NameError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_UNBOUNDLOCALERROR_HPP
                catch(pythonic::types::UnboundLocalError & e) {
                    PyErr_SetString(PyExc_UnboundLocalError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_BUFFERERROR_HPP
                catch(pythonic::types::BufferError & e) {
                    PyErr_SetString(PyExc_BufferError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_MEMORYERROR_HPP
                catch(pythonic::types::MemoryError & e) {
                    PyErr_SetString(PyExc_MemoryError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_LOOKUPERROR_HPP
                catch(pythonic::types::LookupError & e) {
                    PyErr_SetString(PyExc_LookupError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_KEYERROR_HPP
                catch(pythonic::types::KeyError & e) {
                    PyErr_SetString(PyExc_KeyError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_INDEXERROR_HPP
                catch(pythonic::types::IndexError & e) {
                    PyErr_SetString(PyExc_IndexError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_ARITHMETICERROR_HPP
                catch(pythonic::types::ArithmeticError & e) {
                    PyErr_SetString(PyExc_ArithmeticError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_FLOATINGPOINTERROR_HPP
                catch(pythonic::types::FloatingPointError & e) {
                    PyErr_SetString(PyExc_FloatingPointError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_STOPITERATION_HPP
                catch(pythonic::types::StopIteration & e) {
                    PyErr_SetString(PyExc_StopIteration,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_WARNING_HPP
                catch(pythonic::types::Warning & e) {
                    PyErr_SetString(PyExc_Warning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_SYNTAXWARNING_HPP
                catch(pythonic::types::SyntaxWarning & e) {
                    PyErr_SetString(PyExc_SyntaxWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_RUNTIMEWARNING_HPP
                catch(pythonic::types::RuntimeWarning & e) {
                    PyErr_SetString(PyExc_RuntimeWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_DEPRECATIONWARNING_HPP
                catch(pythonic::types::DeprecationWarning & e) {
                    PyErr_SetString(PyExc_DeprecationWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_IMPORTWARNING_HPP
                catch(pythonic::types::ImportWarning & e) {
                    PyErr_SetString(PyExc_ImportWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_UNICODEWARNING_HPP
                catch(pythonic::types::UnicodeWarning & e) {
                    PyErr_SetString(PyExc_UnicodeWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_BYTESWARNING_HPP
                catch(pythonic::types::BytesWarning & e) {
                    PyErr_SetString(PyExc_BytesWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_USERWARNING_HPP
                catch(pythonic::types::UserWarning & e) {
                    PyErr_SetString(PyExc_UserWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_GENERATOREXIT_HPP
                catch(pythonic::types::GeneratorExit & e) {
                    PyErr_SetString(PyExc_GeneratorExit,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_VALUEERROR_HPP
                catch(pythonic::types::ValueError & e) {
                    PyErr_SetString(PyExc_ValueError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_UNICODEERROR_HPP
                catch(pythonic::types::UnicodeError & e) {
                    PyErr_SetString(PyExc_UnicodeError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_ZERODIVISIONERROR_HPP
                catch(pythonic::types::ZeroDivisionError & e) {
                    PyErr_SetString(PyExc_ZeroDivisionError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_FUTUREWARNING_HPP
                catch(pythonic::types::FutureWarning & e) {
                    PyErr_SetString(PyExc_FutureWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_TABERROR_HPP
                catch(pythonic::types::TabError & e) {
                    PyErr_SetString(PyExc_TabError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_OSERROR_HPP
                catch(pythonic::types::OSError & e) {
                    PyErr_SetString(PyExc_OSError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_OVERFLOWERROR_HPP
                catch(pythonic::types::OverflowError & e) {
                    PyErr_SetString(PyExc_OverflowError,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            #ifdef PYTHONIC_BUILTIN_PENDINGDEPRECATIONWARNING_HPP
                catch(pythonic::types::PendingDeprecationWarning & e) {
                    PyErr_SetString(PyExc_PendingDeprecationWarning,
                        pythonic::__builtin__::functor::str{}(e.args).c_str());
                }
            #endif
                

            catch(...) {
                PyErr_SetString(PyExc_RuntimeError,
                    "Something happened on the way to heaven"
                );
            }
                return nullptr;
            }

            static PyMethodDef Methods[] = {
                {
                "compute_tps_matrix",
                __pythran_wrapall_compute_tps_matrix,
                METH_VARARGS,
                "Supported prototypes:\n    - compute_tps_matrix(float64[][], float64[][])\n    - compute_tps_matrix(float64[][], float64[][].T)\n    - compute_tps_matrix(float64[][].T, float64[][])\n    - compute_tps_matrix(float64[][].T, float64[][].T)\ncalculate the thin plate spline (tps) interpolation at a set of points\n\n    Parameters\n    ----------\n\n    dsites: np.array\n        ``[nb_dim, M]`` array representing the postions of the M\n        'observation' sites, with nb_dim the space dimension.\n\n    centers: np.array\n        ``[nb_dim, N]`` array representing the postions of the N centers,\n        sources of the tps.\n\n    Returns\n    -------\n\n    EM : np.array\n        ``[(N+nb_dim), M]`` matrix representing the contributions at the M sites.\n\n        From unit sources located at each of the N centers, +\n        (nb_dim+1) columns representing the contribution of the linear\n        gradient part.\n\n    Notes\n    -----\n\n    >>> U_interp = np.dot(U_tps, EM)\n\n"},
                {NULL, NULL, 0, NULL}
            };

            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "tps_pythran",            /* m_name */
                "",         /* m_doc */
                -1,                  /* m_size */
                Methods,             /* m_methods */
                NULL,                /* m_reload */
                NULL,                /* m_traverse */
                NULL,                /* m_clear */
                NULL,                /* m_free */
              };
            #define PYTHRAN_RETURN return theModule
            #define PYTHRAN_MODULE_INIT(s) PyInit_##s
            #else
            #define PYTHRAN_RETURN return
            #define PYTHRAN_MODULE_INIT(s) init##s
            #endif
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(tps_pythran)(void)
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible));
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(tps_pythran)(void) {
                #ifdef PYTHONIC_TYPES_NDARRAY_HPP
                    import_array()
                #endif
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("tps_pythran",
                                                     Methods,
                                                     ""
                );
                #endif
                if(not theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.7.4.post1",
                                                  "2016-05-31 00:28:43.369370",
                                                  "a5fa6ccbc9458aa72a598aaf853f75c2361f3b383b23fda80134fbeb0f2111bc");
                if(not theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);
                
                PYTHRAN_RETURN;
            }