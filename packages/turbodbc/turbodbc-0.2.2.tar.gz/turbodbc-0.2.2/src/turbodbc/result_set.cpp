#include <turbodbc/cursor.h>
#include <turbodbc/column.h>
#include <turbodbc/make_description.h>
#include <sqlext.h>
#include <stdexcept>
#include <sstream>

namespace turbodbc {

namespace {

	std::unique_ptr<column> make_column(cpp_odbc::statement const & statement, std::size_t one_based_index, std::size_t buffered_rows)
	{
		auto const column_description = statement.describe_column(one_based_index);
		return std::unique_ptr<column>(new column(statement, one_based_index, buffered_rows, make_description(column_description)));
	}

}

result_set::result_set(std::shared_ptr<cpp_odbc::statement const> statement, std::size_t buffered_rows) :
	statement_(statement),
	rows_fetched_(0),
	current_fetched_row_(0)
{
	std::size_t const n_columns = statement_->number_of_columns();

	for (std::size_t one_based_index = 1; one_based_index <= n_columns; ++one_based_index) {
		columns_.push_back(make_column(*statement, one_based_index, buffered_rows));
	}

	statement_->set_attribute(SQL_ATTR_ROW_ARRAY_SIZE, buffered_rows);
	statement_->set_attribute(SQL_ATTR_ROWS_FETCHED_PTR, &rows_fetched_);
}

std::vector<nullable_field> result_set::fetch_one()
{
	auto const no_fetched_results_left = (current_fetched_row_ == rows_fetched_);
	if (no_fetched_results_left) {
		auto const has_more_results = statement_->fetch_next();
		current_fetched_row_ = 0;
		if (not has_more_results) {
			return {};
		}
	}

	std::vector<nullable_field> row;
	for (auto const & column : columns_) {
		row.push_back(column->get_field(current_fetched_row_));
	}
	++current_fetched_row_;
	return row;
}

std::vector<column_info> result_set::get_info() const
{
	std::vector<column_info> infos;
	for (auto const & column : columns_) {
		infos.push_back(column->get_info());
	}
	return infos;
}

}
