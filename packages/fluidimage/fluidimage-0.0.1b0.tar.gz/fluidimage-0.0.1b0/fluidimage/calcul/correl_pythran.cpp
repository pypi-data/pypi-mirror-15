#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/numpy/float32.hpp>
#include <pythonic/include/__builtin__/min.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/include/__builtin__/int_.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/__builtin__/xrange.hpp>
#include <pythonic/include/__builtin__/str.hpp>
#include <pythonic/include/__builtin__/max.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/numpy/float32.hpp>
#include <pythonic/__builtin__/min.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/square.hpp>
#include <pythonic/__builtin__/int_.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/__builtin__/xrange.hpp>
#include <pythonic/__builtin__/str.hpp>
#include <pythonic/__builtin__/max.hpp>
#include <pythonic/numpy/empty.hpp>
namespace __pythran_correl_pythran
{
  ;
  ;
  ;
  ;
  struct correl_pythran
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::int_{})>::type>::type>()(std::declval<__type0>())) __type1;
      typedef long __type2;
      typedef decltype((std::declval<__type1>() * std::declval<__type2>())) __type3;
      typedef decltype((std::declval<__type3>() + std::declval<__type2>())) __type5;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float32{})>::type>::type __type7;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type>()(std::declval<__type6>(), std::declval<__type7>()))>::type __type8;
      typedef decltype((std::declval<__type0>() + std::declval<__type2>())) __type10;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type10>())) __type11;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type0>())) __type13;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
      typedef typename __combined<__type12,__type14>::type __type15;
      typedef decltype((std::declval<__type15>() + std::declval<__type0>())) __type16;
      typedef decltype((std::declval<__type16>() + std::declval<__type2>())) __type18;
      typedef decltype((std::declval<__type14>() + std::declval<__type0>())) __type21;
      typedef decltype((std::declval<__type21>() + std::declval<__type2>())) __type23;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type18>(), std::declval<__type23>())) __type24;
      typedef indexable<__type24> __type25;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type18>(), std::declval<__type12>())) __type34;
      typedef indexable<__type34> __type35;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type23>())) __type42;
      typedef indexable<__type42> __type43;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type12>())) __type49;
      typedef indexable<__type49> __type50;
      typedef typename pythonic::assignable<double>::type __type53;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type54;
      typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>()))>::type __type55;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type55>::type>::type>::type __type56;
      typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>()))>::type __type57;
      typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type57>::type>::type>::type __type58;
      typedef decltype((pythonic::operator_::floordiv(std::declval<__type58>(), std::declval<__type2>()))) __type60;
      typedef decltype((pythonic::operator_::floordiv(std::declval<__type56>(), std::declval<__type2>()))) __type62;
      typedef decltype((std::declval<__type60>() - std::declval<__type62>())) __type63;
      typedef decltype((-std::declval<__type0>())) __type64;
      typedef typename pythonic::assignable<decltype((std::declval<__type64>() + std::declval<__type12>()))>::type __type65;
      typedef decltype((std::declval<__type63>() + std::declval<__type65>())) __type66;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::min{})>::type>::type>()(std::declval<__type66>(), std::declval<__type2>())) __type68;
      typedef typename pythonic::assignable<decltype((std::declval<__type56>() + std::declval<__type68>()))>::type __type69;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type69>())) __type70;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type70>::type::iterator>::value_type>::type __type71;
      typedef decltype((std::declval<__type60>() + std::declval<__type62>())) __type76;
      typedef typename pythonic::assignable<decltype((std::declval<__type15>() + std::declval<__type2>()))>::type __type79;
      typedef decltype((std::declval<__type76>() + std::declval<__type79>())) __type80;
      typedef decltype((std::declval<__type80>() - std::declval<__type58>())) __type81;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type81>(), std::declval<__type2>())) __type83;
      typedef typename pythonic::assignable<decltype((std::declval<__type56>() - std::declval<__type83>()))>::type __type84;
      typedef typename __combined<__type69,__type84>::type __type85;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type85>())) __type86;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type86>::type::iterator>::value_type>::type __type87;
      typedef typename __combined<__type71,__type87>::type __type88;
      typedef typename pythonic::assignable<long>::type __type89;
      typedef typename pythonic::assignable<decltype((-std::declval<__type68>()))>::type __type98;
      typedef typename __combined<__type89,__type98>::type __type99;
      typedef decltype((std::declval<__type88>() + std::declval<__type99>())) __type100;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type55>::type>::type>::type __type101;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type57>::type>::type>::type __type102;
      typedef decltype((pythonic::operator_::floordiv(std::declval<__type102>(), std::declval<__type2>()))) __type104;
      typedef decltype((pythonic::operator_::floordiv(std::declval<__type101>(), std::declval<__type2>()))) __type106;
      typedef decltype((std::declval<__type104>() + std::declval<__type106>())) __type107;
      typedef typename pythonic::assignable<decltype((std::declval<__type14>() + std::declval<__type2>()))>::type __type109;
      typedef decltype((std::declval<__type107>() + std::declval<__type109>())) __type110;
      typedef decltype((std::declval<__type110>() - std::declval<__type102>())) __type111;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type111>(), std::declval<__type2>())) __type113;
      typedef typename pythonic::lazy<decltype((std::declval<__type101>() - std::declval<__type113>()))>::type __type114;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type114>())) __type115;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type115>::type::iterator>::value_type>::type __type116;
      typedef decltype((std::declval<__type104>() - std::declval<__type106>())) __type122;
      typedef decltype((std::declval<__type122>() + std::declval<__type65>())) __type125;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::min{})>::type>::type>()(std::declval<__type125>(), std::declval<__type2>())) __type127;
      typedef typename pythonic::assignable<decltype((-std::declval<__type127>()))>::type __type128;
      typedef typename __combined<__type128,__type89>::type __type129;
      typedef decltype((std::declval<__type116>() + std::declval<__type129>())) __type130;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type100>(), std::declval<__type130>())) __type131;
      typedef decltype(std::declval<__type54>()[std::declval<__type131>()]) __type132;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type133;
      typedef typename pythonic::assignable<decltype((std::declval<__type63>() + std::declval<__type79>()))>::type __type139;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type2>(), std::declval<__type66>()))>::type __type147;
      typedef typename __combined<__type139,__type147>::type __type148;
      typedef decltype((std::declval<__type148>() + std::declval<__type88>())) __type150;
      typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type2>(), std::declval<__type125>()))>::type __type158;
      typedef typename pythonic::assignable<decltype((std::declval<__type122>() + std::declval<__type109>()))>::type __type164;
      typedef typename __combined<__type158,__type164>::type __type165;
      typedef decltype((std::declval<__type165>() + std::declval<__type116>())) __type166;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type150>(), std::declval<__type166>())) __type167;
      typedef decltype(std::declval<__type133>()[std::declval<__type167>()]) __type168;
      typedef decltype((std::declval<__type132>() * std::declval<__type168>())) __type169;
      typedef decltype((std::declval<__type53>() + std::declval<__type169>())) __type170;
      typedef typename __combined<__type53,__type169,__type170>::type __type171;
      typedef decltype((std::declval<__type114>() * std::declval<__type85>())) __type173;
      typedef decltype((std::declval<__type171>() / std::declval<__type173>())) __type174;
      typedef container<typename std::remove_reference<__type174>::type> __type175;
      typedef decltype((std::declval<__type71>() + std::declval<__type98>())) __type177;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type177>(), std::declval<__type130>())) __type195;
      typedef decltype(std::declval<__type54>()[std::declval<__type195>()]) __type196;
      typedef decltype((std::declval<__type147>() + std::declval<__type71>())) __type197;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type197>(), std::declval<__type166>())) __type206;
      typedef decltype(std::declval<__type133>()[std::declval<__type206>()]) __type207;
      typedef decltype((std::declval<__type196>() * std::declval<__type207>())) __type208;
      typedef decltype((std::declval<__type53>() + std::declval<__type208>())) __type209;
      typedef typename __combined<__type53,__type208,__type209>::type __type210;
      typedef decltype((std::declval<__type114>() * std::declval<__type69>())) __type211;
      typedef decltype((std::declval<__type210>() / std::declval<__type211>())) __type212;
      typedef container<typename std::remove_reference<__type212>::type> __type213;
      typedef typename pythonic::lazy<decltype((std::declval<__type101>() + std::declval<__type127>()))>::type __type224;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type224>())) __type225;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type225>::type::iterator>::value_type>::type __type226;
      typedef decltype((std::declval<__type226>() + std::declval<__type128>())) __type227;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type177>(), std::declval<__type227>())) __type228;
      typedef decltype(std::declval<__type54>()[std::declval<__type228>()]) __type229;
      typedef decltype((std::declval<__type158>() + std::declval<__type226>())) __type231;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type197>(), std::declval<__type231>())) __type232;
      typedef decltype(std::declval<__type133>()[std::declval<__type232>()]) __type233;
      typedef decltype((std::declval<__type229>() * std::declval<__type233>())) __type234;
      typedef decltype((std::declval<__type53>() + std::declval<__type234>())) __type235;
      typedef typename __combined<__type53,__type234,__type235>::type __type236;
      typedef decltype((std::declval<__type224>() * std::declval<__type69>())) __type237;
      typedef decltype((std::declval<__type236>() / std::declval<__type237>())) __type238;
      typedef container<typename std::remove_reference<__type238>::type> __type239;
      typedef decltype((std::declval<__type226>() + std::declval<__type129>())) __type259;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type100>(), std::declval<__type259>())) __type260;
      typedef decltype(std::declval<__type54>()[std::declval<__type260>()]) __type261;
      typedef decltype((std::declval<__type165>() + std::declval<__type226>())) __type266;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type150>(), std::declval<__type266>())) __type267;
      typedef decltype(std::declval<__type133>()[std::declval<__type267>()]) __type268;
      typedef decltype((std::declval<__type261>() * std::declval<__type268>())) __type269;
      typedef decltype((std::declval<__type53>() + std::declval<__type269>())) __type270;
      typedef typename __combined<__type53,__type269,__type270>::type __type271;
      typedef decltype((std::declval<__type224>() * std::declval<__type85>())) __type273;
      typedef decltype((std::declval<__type271>() / std::declval<__type273>())) __type274;
      typedef container<typename std::remove_reference<__type274>::type> __type275;
      typedef typename __combined<__type8,__type43,__type50,__type239,__type275>::type __type279;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>())) __type280;
      typedef decltype((std::declval<__type279>() * std::declval<__type280>())) __type281;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type>()(std::declval<__type54>())) __type282;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type>()(std::declval<__type282>())) __type283;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type281>(), std::declval<__type283>()))>::type result_type;
    }
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0 const & im0, argument_type1 const & im1, argument_type2 const & disp_max) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename correl_pythran::type<argument_type0, argument_type1, argument_type2>::result_type correl_pythran::operator()(argument_type0 const & im0, argument_type1 const & im1, argument_type2 const & disp_max) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::int_{})>::type>::type>()(std::declval<__type0>())) __type1;
    typedef long __type2;
    typedef decltype((std::declval<__type1>() * std::declval<__type2>())) __type3;
    typedef decltype((std::declval<__type3>() + std::declval<__type2>())) __type5;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type5>(), std::declval<__type5>())) __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::float32{})>::type>::type __type7;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type>()(std::declval<__type6>(), std::declval<__type7>()))>::type __type8;
    typedef decltype((std::declval<__type0>() + std::declval<__type2>())) __type10;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type10>())) __type11;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type0>())) __type13;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
    typedef typename __combined<__type12,__type14>::type __type15;
    typedef decltype((std::declval<__type15>() + std::declval<__type0>())) __type16;
    typedef decltype((std::declval<__type16>() + std::declval<__type2>())) __type18;
    typedef decltype((std::declval<__type14>() + std::declval<__type0>())) __type21;
    typedef decltype((std::declval<__type21>() + std::declval<__type2>())) __type23;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type18>(), std::declval<__type23>())) __type24;
    typedef indexable<__type24> __type25;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type18>(), std::declval<__type12>())) __type34;
    typedef indexable<__type34> __type35;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type23>())) __type42;
    typedef indexable<__type42> __type43;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type12>(), std::declval<__type12>())) __type49;
    typedef indexable<__type49> __type50;
    typedef typename pythonic::assignable<double>::type __type53;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type54;
    typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type>()))>::type __type55;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type55>::type>::type>::type __type56;
    typedef typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>()))>::type __type57;
    typedef typename pythonic::assignable<typename std::tuple_element<0,typename std::remove_reference<__type57>::type>::type>::type __type58;
    typedef decltype((pythonic::operator_::floordiv(std::declval<__type58>(), std::declval<__type2>()))) __type60;
    typedef decltype((pythonic::operator_::floordiv(std::declval<__type56>(), std::declval<__type2>()))) __type62;
    typedef decltype((std::declval<__type60>() - std::declval<__type62>())) __type63;
    typedef decltype((-std::declval<__type0>())) __type64;
    typedef typename pythonic::assignable<decltype((std::declval<__type64>() + std::declval<__type12>()))>::type __type65;
    typedef decltype((std::declval<__type63>() + std::declval<__type65>())) __type66;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::min{})>::type>::type>()(std::declval<__type66>(), std::declval<__type2>())) __type68;
    typedef typename pythonic::assignable<decltype((std::declval<__type56>() + std::declval<__type68>()))>::type __type69;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type69>())) __type70;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type70>::type::iterator>::value_type>::type __type71;
    typedef decltype((std::declval<__type60>() + std::declval<__type62>())) __type76;
    typedef typename pythonic::assignable<decltype((std::declval<__type15>() + std::declval<__type2>()))>::type __type79;
    typedef decltype((std::declval<__type76>() + std::declval<__type79>())) __type80;
    typedef decltype((std::declval<__type80>() - std::declval<__type58>())) __type81;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type81>(), std::declval<__type2>())) __type83;
    typedef typename pythonic::assignable<decltype((std::declval<__type56>() - std::declval<__type83>()))>::type __type84;
    typedef typename __combined<__type69,__type84>::type __type85;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type85>())) __type86;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type86>::type::iterator>::value_type>::type __type87;
    typedef typename __combined<__type71,__type87>::type __type88;
    typedef typename pythonic::assignable<long>::type __type89;
    typedef typename pythonic::assignable<decltype((-std::declval<__type68>()))>::type __type98;
    typedef typename __combined<__type89,__type98>::type __type99;
    typedef decltype((std::declval<__type88>() + std::declval<__type99>())) __type100;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type55>::type>::type>::type __type101;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type57>::type>::type>::type __type102;
    typedef decltype((pythonic::operator_::floordiv(std::declval<__type102>(), std::declval<__type2>()))) __type104;
    typedef decltype((pythonic::operator_::floordiv(std::declval<__type101>(), std::declval<__type2>()))) __type106;
    typedef decltype((std::declval<__type104>() + std::declval<__type106>())) __type107;
    typedef typename pythonic::assignable<decltype((std::declval<__type14>() + std::declval<__type2>()))>::type __type109;
    typedef decltype((std::declval<__type107>() + std::declval<__type109>())) __type110;
    typedef decltype((std::declval<__type110>() - std::declval<__type102>())) __type111;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type111>(), std::declval<__type2>())) __type113;
    typedef typename pythonic::lazy<decltype((std::declval<__type101>() - std::declval<__type113>()))>::type __type114;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type114>())) __type115;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type115>::type::iterator>::value_type>::type __type116;
    typedef decltype((std::declval<__type104>() - std::declval<__type106>())) __type122;
    typedef decltype((std::declval<__type122>() + std::declval<__type65>())) __type125;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::min{})>::type>::type>()(std::declval<__type125>(), std::declval<__type2>())) __type127;
    typedef typename pythonic::assignable<decltype((-std::declval<__type127>()))>::type __type128;
    typedef typename __combined<__type128,__type89>::type __type129;
    typedef decltype((std::declval<__type116>() + std::declval<__type129>())) __type130;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type100>(), std::declval<__type130>())) __type131;
    typedef decltype(std::declval<__type54>()[std::declval<__type131>()]) __type132;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type133;
    typedef typename pythonic::assignable<decltype((std::declval<__type63>() + std::declval<__type79>()))>::type __type139;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type2>(), std::declval<__type66>()))>::type __type147;
    typedef typename __combined<__type139,__type147>::type __type148;
    typedef decltype((std::declval<__type148>() + std::declval<__type88>())) __type150;
    typedef typename pythonic::assignable<decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::max{})>::type>::type>()(std::declval<__type2>(), std::declval<__type125>()))>::type __type158;
    typedef typename pythonic::assignable<decltype((std::declval<__type122>() + std::declval<__type109>()))>::type __type164;
    typedef typename __combined<__type158,__type164>::type __type165;
    typedef decltype((std::declval<__type165>() + std::declval<__type116>())) __type166;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type150>(), std::declval<__type166>())) __type167;
    typedef decltype(std::declval<__type133>()[std::declval<__type167>()]) __type168;
    typedef decltype((std::declval<__type132>() * std::declval<__type168>())) __type169;
    typedef decltype((std::declval<__type53>() + std::declval<__type169>())) __type170;
    typedef typename __combined<__type53,__type169,__type170>::type __type171;
    typedef decltype((std::declval<__type114>() * std::declval<__type85>())) __type173;
    typedef decltype((std::declval<__type171>() / std::declval<__type173>())) __type174;
    typedef container<typename std::remove_reference<__type174>::type> __type175;
    typedef decltype((std::declval<__type71>() + std::declval<__type98>())) __type177;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type177>(), std::declval<__type130>())) __type195;
    typedef decltype(std::declval<__type54>()[std::declval<__type195>()]) __type196;
    typedef decltype((std::declval<__type147>() + std::declval<__type71>())) __type197;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type197>(), std::declval<__type166>())) __type206;
    typedef decltype(std::declval<__type133>()[std::declval<__type206>()]) __type207;
    typedef decltype((std::declval<__type196>() * std::declval<__type207>())) __type208;
    typedef decltype((std::declval<__type53>() + std::declval<__type208>())) __type209;
    typedef typename __combined<__type53,__type208,__type209>::type __type210;
    typedef decltype((std::declval<__type114>() * std::declval<__type69>())) __type211;
    typedef decltype((std::declval<__type210>() / std::declval<__type211>())) __type212;
    typedef container<typename std::remove_reference<__type212>::type> __type213;
    typedef typename pythonic::lazy<decltype((std::declval<__type101>() + std::declval<__type127>()))>::type __type224;
    typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::xrange{})>::type>::type>()(std::declval<__type224>())) __type225;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type225>::type::iterator>::value_type>::type __type226;
    typedef decltype((std::declval<__type226>() + std::declval<__type128>())) __type227;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type177>(), std::declval<__type227>())) __type228;
    typedef decltype(std::declval<__type54>()[std::declval<__type228>()]) __type229;
    typedef decltype((std::declval<__type158>() + std::declval<__type226>())) __type231;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type197>(), std::declval<__type231>())) __type232;
    typedef decltype(std::declval<__type133>()[std::declval<__type232>()]) __type233;
    typedef decltype((std::declval<__type229>() * std::declval<__type233>())) __type234;
    typedef decltype((std::declval<__type53>() + std::declval<__type234>())) __type235;
    typedef typename __combined<__type53,__type234,__type235>::type __type236;
    typedef decltype((std::declval<__type224>() * std::declval<__type69>())) __type237;
    typedef decltype((std::declval<__type236>() / std::declval<__type237>())) __type238;
    typedef container<typename std::remove_reference<__type238>::type> __type239;
    typedef decltype((std::declval<__type226>() + std::declval<__type129>())) __type259;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type100>(), std::declval<__type259>())) __type260;
    typedef decltype(std::declval<__type54>()[std::declval<__type260>()]) __type261;
    typedef decltype((std::declval<__type165>() + std::declval<__type226>())) __type266;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type150>(), std::declval<__type266>())) __type267;
    typedef decltype(std::declval<__type133>()[std::declval<__type267>()]) __type268;
    typedef decltype((std::declval<__type261>() * std::declval<__type268>())) __type269;
    typedef decltype((std::declval<__type53>() + std::declval<__type269>())) __type270;
    typedef typename __combined<__type53,__type269,__type270>::type __type271;
    typedef decltype((std::declval<__type224>() * std::declval<__type85>())) __type273;
    typedef decltype((std::declval<__type271>() / std::declval<__type273>())) __type274;
    typedef container<typename std::remove_reference<__type274>::type> __type275;
    typename pythonic::assignable<typename __combined<__type139,__type147>::type>::type ny0dep;
    typename pythonic::assignable<typename __combined<__type158,__type164>::type>::type nx0dep;
    typename pythonic::assignable<typename __combined<__type71,__type87>::type>::type iy;
    typename pythonic::assignable<typename __combined<__type12,__type14>::type>::type xiy;
    typename pythonic::assignable<typename __combined<__type128,__type89>::type>::type nx1dep;
    typename pythonic::assignable<typename __combined<__type89,__type98>::type>::type ny1dep;
    typename pythonic::assignable<typename __combined<__type69,__type84>::type>::type nymax;
    ;
    ;
    typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(im0))>::type __tuple0 = pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(im0);
    typename pythonic::assignable<decltype(std::get<1>(__tuple0))>::type nx0 = std::get<1>(__tuple0);
    typename pythonic::assignable<decltype(std::get<0>(__tuple0))>::type ny0 = std::get<0>(__tuple0);
    typename pythonic::assignable<decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(im1))>::type __tuple1 = pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(im1);
    typename pythonic::assignable<decltype(std::get<1>(__tuple1))>::type nx1 = std::get<1>(__tuple1);
    typename pythonic::assignable<decltype(std::get<0>(__tuple1))>::type ny1 = std::get<0>(__tuple1);
    ;
    typename pythonic::assignable<typename __combined<__type8,__type43,__type50,__type239,__type275>::type>::type correl = pythonic::numpy::functor::empty{}(pythonic::types::make_tuple(((pythonic::__builtin__::functor::int_{}(disp_max) * 2L) + 1L), ((pythonic::__builtin__::functor::int_{}(disp_max) * 2L) + 1L)), pythonic::numpy::functor::float32{});
    {
      long  __target1 = (disp_max + 1L);
      for ( xiy = 0L; xiy < __target1; xiy += 1L)
      {
        typename pythonic::assignable<decltype(((-disp_max) + xiy))>::type dispy_ = ((-disp_max) + xiy);
        nymax = (ny1 + pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(ny0, 2L)) - (pythonic::operator_::floordiv(ny1, 2L))) + dispy_), 0L));
        ny1dep = (-pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(ny0, 2L)) - (pythonic::operator_::floordiv(ny1, 2L))) + dispy_), 0L));
        ny0dep = pythonic::__builtin__::functor::max{}(0L, (((pythonic::operator_::floordiv(ny0, 2L)) - (pythonic::operator_::floordiv(ny1, 2L))) + dispy_));
        {
          long  __target2 = (disp_max + 1L);
          for (long  xix__ = 0L; xix__ < __target2; xix__ += 1L)
          {
            typename pythonic::assignable<decltype(((-disp_max) + xix__))>::type dispx__ = ((-disp_max) + xix__);
            typename pythonic::lazy<decltype((nx1 + pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx__), 0L)))>::type nxmax__ = (nx1 + pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx__), 0L));
            nx1dep = (-pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx__), 0L));
            nx0dep = pythonic::__builtin__::functor::max{}(0L, (((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx__));
            typename pythonic::assignable<typename __combined<__type53,__type234,__type235>::type>::type tmp___ = 0.0;
            {
              long  __target3 = nymax;
              for ( iy = 0L; iy < __target3; iy += 1L)
              {
                {
                  long  __target4 = nxmax__;
                  for (long  ix__ = 0L; ix__ < __target4; ix__ += 1L)
                  {
                    tmp___ += (im1[pythonic::types::make_tuple((iy + ny1dep), (ix__ + nx1dep))] * im0[pythonic::types::make_tuple((ny0dep + iy), (nx0dep + ix__))]);
                  }
                }
              }
              if (iy == __target3)
              iy -= 1L;
            }
            correl[pythonic::types::make_tuple(xiy, xix__)] = (tmp___ / (nxmax__ * nymax));
          }
        }
        {
          long  __target2 = disp_max;
          for (long  xix_ = 0L; xix_ < __target2; xix_ += 1L)
          {
            typename pythonic::assignable<decltype((xix_ + 1L))>::type dispx_ = (xix_ + 1L);
            typename pythonic::lazy<decltype((nx1 - pythonic::__builtin__::functor::max{}(((((pythonic::operator_::floordiv(nx0, 2L)) + (pythonic::operator_::floordiv(nx1, 2L))) + dispx_) - nx0), 0L)))>::type nxmax_ = (nx1 - pythonic::__builtin__::functor::max{}(((((pythonic::operator_::floordiv(nx0, 2L)) + (pythonic::operator_::floordiv(nx1, 2L))) + dispx_) - nx0), 0L));
            nx1dep = 0L;
            nx0dep = (((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx_);
            typename pythonic::assignable<typename __combined<__type53,__type208,__type209>::type>::type tmp__ = 0.0;
            {
              long  __target3 = nymax;
              for ( iy = 0L; iy < __target3; iy += 1L)
              {
                {
                  long  __target4 = nxmax_;
                  for (long  ix_ = 0L; ix_ < __target4; ix_ += 1L)
                  {
                    tmp__ += (im1[pythonic::types::make_tuple((iy + ny1dep), (ix_ + nx1dep))] * im0[pythonic::types::make_tuple((ny0dep + iy), (nx0dep + ix_))]);
                  }
                }
              }
              if (iy == __target3)
              iy -= 1L;
            }
            correl[pythonic::types::make_tuple(xiy, ((xix_ + disp_max) + 1L))] = (tmp__ / (nxmax_ * nymax));
          }
        }
      }
      if (xiy == __target1)
      xiy -= 1L;
    }
    {
      long  __target1 = disp_max;
      for ( xiy = 0L; xiy < __target1; xiy += 1L)
      {
        typename pythonic::assignable<typename pythonic::assignable<decltype((std::declval<__type15>() + std::declval<__type2>()))>::type>::type dispy = (xiy + 1L);
        nymax = (ny1 - pythonic::__builtin__::functor::max{}(((((pythonic::operator_::floordiv(ny0, 2L)) + (pythonic::operator_::floordiv(ny1, 2L))) + dispy) - ny0), 0L));
        ny1dep = 0L;
        ny0dep = (((pythonic::operator_::floordiv(ny0, 2L)) - (pythonic::operator_::floordiv(ny1, 2L))) + dispy);
        {
          long  __target2 = (disp_max + 1L);
          for (long  xix = 0L; xix < __target2; xix += 1L)
          {
            typename pythonic::assignable<decltype(((-disp_max) + xix))>::type dispx = ((-disp_max) + xix);
            typename pythonic::lazy<decltype((nx1 + pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx), 0L)))>::type nxmax = (nx1 + pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx), 0L));
            nx1dep = (-pythonic::__builtin__::functor::min{}((((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx), 0L));
            nx0dep = pythonic::__builtin__::functor::max{}(0L, (((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx));
            typename pythonic::assignable<typename __combined<__type53,__type269,__type270>::type>::type tmp_ = 0.0;
            {
              long  __target3 = nymax;
              for ( iy = 0L; iy < __target3; iy += 1L)
              {
                {
                  long  __target4 = nxmax;
                  for (long  ix = 0L; ix < __target4; ix += 1L)
                  {
                    tmp_ += (im1[pythonic::types::make_tuple((iy + ny1dep), (ix + nx1dep))] * im0[pythonic::types::make_tuple((ny0dep + iy), (nx0dep + ix))]);
                  }
                }
              }
              if (iy == __target3)
              iy -= 1L;
            }
            correl[pythonic::types::make_tuple(((xiy + disp_max) + 1L), xix)] = (tmp_ / (nxmax * nymax));
          }
        }
        {
          long  __target2 = disp_max;
          for (long  xix___ = 0L; xix___ < __target2; xix___ += 1L)
          {
            typename pythonic::assignable<decltype((xix___ + 1L))>::type dispx___ = (xix___ + 1L);
            typename pythonic::lazy<decltype((nx1 - pythonic::__builtin__::functor::max{}(((((pythonic::operator_::floordiv(nx0, 2L)) + (pythonic::operator_::floordiv(nx1, 2L))) + dispx___) - nx0), 0L)))>::type nxmax___ = (nx1 - pythonic::__builtin__::functor::max{}(((((pythonic::operator_::floordiv(nx0, 2L)) + (pythonic::operator_::floordiv(nx1, 2L))) + dispx___) - nx0), 0L));
            nx1dep = 0L;
            nx0dep = (((pythonic::operator_::floordiv(nx0, 2L)) - (pythonic::operator_::floordiv(nx1, 2L))) + dispx___);
            typename pythonic::assignable<typename __combined<__type53,__type169,__type170>::type>::type tmp = 0.0;
            {
              long  __target3 = nymax;
              for ( iy = 0L; iy < __target3; iy += 1L)
              {
                {
                  long  __target4 = nxmax___;
                  for (long  ix___ = 0L; ix___ < __target4; ix___ += 1L)
                  {
                    tmp += (im1[pythonic::types::make_tuple((iy + ny1dep), (ix___ + nx1dep))] * im0[pythonic::types::make_tuple((ny0dep + iy), (nx0dep + ix___))]);
                  }
                }
              }
              if (iy == __target3)
              iy -= 1L;
            }
            correl[pythonic::types::make_tuple(((xiy + disp_max) + 1L), ((xix___ + disp_max) + 1L))] = (tmp / (nxmax___ * nymax));
          }
        }
      }
      if (xiy == __target1)
      xiy -= 1L;
    }
    ;
    return pythonic::types::make_tuple((correl * pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(im1)), pythonic::numpy::functor::sum{}(pythonic::numpy::functor::square{}(im1)));
  }
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::ndarray<float,2>, pythonic::types::ndarray<float,2>, long>::result_type correl_pythran0(pythonic::types::ndarray<float,2> a0, pythonic::types::ndarray<float,2> a1, long a2)
{
  return __pythran_correl_pythran::correl_pythran()(a0, a1, a2);
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::ndarray<float,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>, long>::result_type correl_pythran1(pythonic::types::ndarray<float,2> a0, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>> a1, long a2)
{
  return __pythran_correl_pythran::correl_pythran()(a0, a1, a2);
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>, pythonic::types::ndarray<float,2>, long>::result_type correl_pythran2(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>> a0, pythonic::types::ndarray<float,2> a1, long a2)
{
  return __pythran_correl_pythran::correl_pythran()(a0, a1, a2);
}
typename __pythran_correl_pythran::correl_pythran::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>, long>::result_type correl_pythran3(pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>> a0, pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>> a1, long a2)
{
  return __pythran_correl_pythran::correl_pythran()(a0, a1, a2);
}

                static PyObject *
                __pythran_wrap_correl_pythran0(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[3+1];
                    if(! PyArg_ParseTuple(args, "OOO", &args_obj[0], &args_obj[1], &args_obj[2]))
                        return nullptr;
                    if(is_convertible<pythonic::types::ndarray<float,2>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<float,2>>(args_obj[1]) and is_convertible<long>(args_obj[2]))
                        return to_python(correl_pythran0(from_python<pythonic::types::ndarray<float,2>>(args_obj[0]), from_python<pythonic::types::ndarray<float,2>>(args_obj[1]), from_python<long>(args_obj[2])));
                    else {
                        return nullptr;
                    }
                }

                static PyObject *
                __pythran_wrap_correl_pythran1(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[3+1];
                    if(! PyArg_ParseTuple(args, "OOO", &args_obj[0], &args_obj[1], &args_obj[2]))
                        return nullptr;
                    if(is_convertible<pythonic::types::ndarray<float,2>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[1]) and is_convertible<long>(args_obj[2]))
                        return to_python(correl_pythran1(from_python<pythonic::types::ndarray<float,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[1]), from_python<long>(args_obj[2])));
                    else {
                        return nullptr;
                    }
                }

                static PyObject *
                __pythran_wrap_correl_pythran2(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[3+1];
                    if(! PyArg_ParseTuple(args, "OOO", &args_obj[0], &args_obj[1], &args_obj[2]))
                        return nullptr;
                    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[0]) and is_convertible<pythonic::types::ndarray<float,2>>(args_obj[1]) and is_convertible<long>(args_obj[2]))
                        return to_python(correl_pythran2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<float,2>>(args_obj[1]), from_python<long>(args_obj[2])));
                    else {
                        return nullptr;
                    }
                }

                static PyObject *
                __pythran_wrap_correl_pythran3(PyObject *self, PyObject *args)
                {
                    PyObject* args_obj[3+1];
                    if(! PyArg_ParseTuple(args, "OOO", &args_obj[0], &args_obj[1], &args_obj[2]))
                        return nullptr;
                    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[0]) and is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[1]) and is_convertible<long>(args_obj[2]))
                        return to_python(correl_pythran3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<float,2>>>(args_obj[1]), from_python<long>(args_obj[2])));
                    else {
                        return nullptr;
                    }
                }

            static PyObject *
            __pythran_wrapall_correl_pythran(PyObject *self, PyObject *args)
            {
                try {
                
                    if(PyObject* obj = __pythran_wrap_correl_pythran0(self, args))
                        return obj;
                    

                    if(PyObject* obj = __pythran_wrap_correl_pythran1(self, args))
                        return obj;
                    

                    if(PyObject* obj = __pythran_wrap_correl_pythran2(self, args))
                        return obj;
                    

                    if(PyObject* obj = __pythran_wrap_correl_pythran3(self, args))
                        return obj;
                    
                PyErr_SetString(PyExc_TypeError,
                  "Invalid argument type for pythranized function `correl_pythran'.\n"
                  "Candidates are:\n   correl_pythran(ndarray<float,2>,ndarray<float,2>,long)\n   correl_pythran(ndarray<float,2>,numpy_texpr<ndarray<float,2>>,long)\n   correl_pythran(numpy_texpr<ndarray<float,2>>,ndarray<float,2>,long)\n   correl_pythran(numpy_texpr<ndarray<float,2>>,numpy_texpr<ndarray<float,2>>,long)\n"
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
                "correl_pythran",
                __pythran_wrapall_correl_pythran,
                METH_VARARGS,
                "Supported prototypes:\n    - correl_pythran(float32[][], float32[][], int)\n    - correl_pythran(float32[][], float32[][].T, int)\n    - correl_pythran(float32[][].T, float32[][], int)\n    - correl_pythran(float32[][].T, float32[][].T, int)\nCorrelations by hand using only numpy.\n\n    Parameters\n    ----------\n\n    im0, im1 : images\n      input images : 2D matrix\n\n    disp_max : int\n      displacement max.\n\n    Notes\n    -------\n\n    im1_shape inf to im0_shape\n\n    Returns\n    -------\n\n    the computing correlation (size of computed correlation = disp_max*2 + 1)\n\n"},
                {NULL, NULL, 0, NULL}
            };

            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "correl_pythran",            /* m_name */
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
            PYTHRAN_MODULE_INIT(correl_pythran)(void)
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible));
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(correl_pythran)(void) {
                #ifdef PYTHONIC_TYPES_NDARRAY_HPP
                    import_array()
                #endif
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("correl_pythran",
                                                     Methods,
                                                     ""
                );
                #endif
                if(not theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.7.4.post1",
                                                  "2016-05-31 00:28:43.045482",
                                                  "a4d40f08c1d42d346bf44077df3fe8fa5577aff82826814e6344c07f1e1b7ee5");
                if(not theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);
                
                PYTHRAN_RETURN;
            }