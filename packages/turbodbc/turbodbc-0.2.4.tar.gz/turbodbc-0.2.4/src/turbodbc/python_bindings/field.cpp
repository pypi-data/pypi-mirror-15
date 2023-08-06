#include <turbodbc/field.h>

#include <boost/python.hpp>

#include <vector>

#include <datetime.h> // Python header

namespace turbodbc { namespace bindings {


struct utf8_from_unicode_object {
	static bool is_convertible(PyObject * object)
	{
		return PyUnicode_Check(object);
	}

	static std::string convert(PyObject * object)
	{
		auto utf8 = boost::python::handle<>{PyUnicode_AsUTF8String(object)};
		return PyString_AsString(utf8.get());
	}
};


struct nullable_field_from_object{
	static bool is_convertible (PyObject * object)
	{
		return	object == Py_None
			or	boost::python::extract<long>(object).check()
			or	boost::python::extract<double>(object).check()
			or	boost::python::extract<std::string>(object).check()
			or	PyDate_Check(object);
			// no check for datetime necessary, included in PyDate_Check
	}

	static nullable_field convert(PyObject * object)
	{
		boost::python::object python_value{boost::python::handle<>{boost::python::borrowed(object)}};

		if (object == Py_None) {
			return {};
		}

		{
			boost::python::extract<long> extractor(object);
			if (extractor.check()) {
				return turbodbc::field(extractor());
			}
		}

		{
			boost::python::extract<double> extractor(object);
			if (extractor.check()) {
				return turbodbc::field(extractor());
			}
		}

		{
			boost::python::extract<std::string> extractor(object);
			if (extractor.check()) {
				return turbodbc::field(extractor());
			}
		}

		if (PyDateTime_Check(object)) {
			auto const year = static_cast<short unsigned int>(PyDateTime_GET_YEAR(object));
			auto const month = static_cast<short unsigned int>(PyDateTime_GET_MONTH(object));
			auto const day = static_cast<short unsigned int>(PyDateTime_GET_DAY(object));
			int const hours = PyDateTime_DATE_GET_HOUR(object);
			int const minutes = PyDateTime_DATE_GET_MINUTE(object);
			int const seconds = PyDateTime_DATE_GET_SECOND(object);
			int const fractional = PyDateTime_DATE_GET_MICROSECOND(object);
			return turbodbc::field(boost::posix_time::ptime({year, month, day},
															{hours, minutes, seconds, fractional}));
		}

		if (PyDate_Check(object)) {
			int const year = PyDateTime_GET_YEAR(object);
			int const month = PyDateTime_GET_MONTH(object);
			int const day = PyDateTime_GET_DAY(object);
			return turbodbc::field(boost::gregorian::date(year, month, day));
		}

		throw std::runtime_error("Could not convert python value to C++");
	}
};

struct vector_nullable_field_from_object{
	static bool is_convertible (PyObject * object)
	{
		return PyList_Check(object);
	}

	static std::vector<nullable_field> convert(PyObject * object)
	{
		auto const size = PyList_Size(object);
		std::vector<nullable_field> result;
		for (unsigned int i = 0; i != size; ++i) {
			result.push_back(boost::python::extract<nullable_field>(PyList_GetItem(object, i)));
		}
		return result;
	}
};

template<typename Converter> struct boost_python_converter
{
	using target = decltype(Converter::convert(std::declval<PyObject*>()));

	static void * is_convertible(PyObject* object)
	{
		if(Converter::is_convertible(object)){
			return object;
		} else {
			return nullptr;
		}
	}

	static void convert(PyObject* object, boost::python::converter::rvalue_from_python_stage1_data* data)
	{
		void* storage = (reinterpret_cast<boost::python::converter::rvalue_from_python_storage<target>*>(data))->storage.bytes;
		new (storage) target(Converter::convert(object));
		data->convertible = storage;
	}
};



void for_field()
{
	PyDateTime_IMPORT;

	boost::python::converter::registry::push_back(
		& boost_python_converter<utf8_from_unicode_object>::is_convertible,
		& boost_python_converter<utf8_from_unicode_object>::convert,
		boost::python::type_id<typename boost_python_converter<utf8_from_unicode_object>::target>()
	);

	boost::python::converter::registry::push_back(
		& boost_python_converter<nullable_field_from_object>::is_convertible,
		& boost_python_converter<nullable_field_from_object>::convert,
		boost::python::type_id<typename boost_python_converter<nullable_field_from_object>::target>()
	);

	boost::python::converter::registry::push_back(
		& boost_python_converter<vector_nullable_field_from_object>::is_convertible,
		& boost_python_converter<vector_nullable_field_from_object>::convert,
		boost::python::type_id<typename boost_python_converter<vector_nullable_field_from_object>::target>()
	);

}

} }


