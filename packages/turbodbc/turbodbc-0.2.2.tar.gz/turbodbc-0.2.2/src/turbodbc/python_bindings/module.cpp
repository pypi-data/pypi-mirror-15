#include <boost/python/module.hpp>

namespace turbodbc { namespace bindings {

	void for_column_info();
	void for_connect();
	void for_connection();
	void for_cursor();
	void for_error();
	void for_field();

} }

BOOST_PYTHON_MODULE(turbodbc_intern)
{
	using namespace turbodbc;
	bindings::for_column_info();
	bindings::for_connect();
	bindings::for_connection();
	bindings::for_cursor();
	bindings::for_error();
	bindings::for_field();
}
