#pragma once

#include <cpp_odbc/connection.h>
#include <turbodbc/query.h>
#include <turbodbc/column_info.h>
#include <memory>


namespace turbodbc {

/**
 * TODO: Cursor needs proper unit tests
 */
class cursor {
public:
	cursor(std::shared_ptr<cpp_odbc::connection const> connection,
		   std::size_t rows_to_buffer,
		   std::size_t parameter_sets_to_buffer);

	void prepare(std::string const & sql);
	void execute();
	void add_parameter_set(std::vector<nullable_field> const & parameter_set);

	std::vector<nullable_field> fetch_one();
	long get_row_count();

	std::vector<column_info> get_result_set_info() const;

	std::shared_ptr<cpp_odbc::connection const> get_connection() const;

	~cursor();

private:
	std::shared_ptr<cpp_odbc::connection const> connection_;
	std::size_t rows_to_buffer_;
	std::size_t parameter_sets_to_buffer_;
	std::shared_ptr<turbodbc::query> query_;
};

}
