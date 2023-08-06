#include <turbodbc/cursor.h>
#include <turbodbc/make_description.h>

#include <cpp_odbc/statement.h>
#include <cpp_odbc/error.h>

#include <boost/variant/get.hpp>
#include <sqlext.h>
#include <stdexcept>

#include <cstring>
#include <sstream>


namespace turbodbc {

cursor::cursor(std::shared_ptr<cpp_odbc::connection const> connection, std::size_t rows_to_buffer, std::size_t parameter_sets_to_buffer) :
	connection_(connection),
	rows_to_buffer_(rows_to_buffer),
	parameter_sets_to_buffer_(parameter_sets_to_buffer),
	query_()
{
}

cursor::~cursor() = default;

void cursor::prepare(std::string const & sql)
{
	results_.reset();
	query_.reset();
	auto statement = connection_->make_statement();
	statement->prepare(sql);
	query_ = std::make_shared<query>(statement, rows_to_buffer_, parameter_sets_to_buffer_);
}

void cursor::execute()
{
	query_->execute();
	auto raw_result_set = query_->get_results();
	if (raw_result_set) {
		results_ = std::make_shared<result_sets::field_result_set>(*raw_result_set);
	}
}

void cursor::add_parameter_set(std::vector<nullable_field> const & parameter_set)
{
	query_->add_parameter_set(parameter_set);
}

std::vector<nullable_field> cursor::fetch_one()
{
	if (results_) {
		return results_->fetch_row();
	} else {
		throw std::runtime_error("No active result set");
	}
}

long cursor::get_row_count()
{
	return query_->get_row_count();
}

std::vector<column_info> cursor::get_result_set_info() const
{
	if (results_) {
		return results_->get_column_info();
	} else {
		return {};
	}
}

std::shared_ptr<cpp_odbc::connection const> cursor::get_connection() const
{
	return connection_;
}


}
