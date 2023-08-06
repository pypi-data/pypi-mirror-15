#include <turbodbc/result_sets/field_result_set.h>

#include <boost/python/class.hpp>

namespace turbodbc { namespace bindings {

void for_field_result_set()
{
	boost::python::class_<turbodbc::result_sets::field_result_set, boost::noncopyable>("FieldResultSet", boost::python::no_init)
    		.def("fetch_row", &turbodbc::result_sets::field_result_set::fetch_row)
    		.def("get_column_info", &turbodbc::result_sets::field_result_set::get_column_info)
    	;
}

} }
