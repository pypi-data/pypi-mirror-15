#include <turbodbc/column.h>

namespace turbodbc {

column::column(cpp_odbc::statement const & statement, std::size_t one_based_index, std::size_t buffered_rows, std::unique_ptr<description const> description) :
	description_(std::move(description)),
	buffer_(description_->element_size(), buffered_rows)
{
	statement.bind_column(one_based_index, description_->column_c_type(), buffer_);
}

column::~column() = default;

nullable_field column::get_field(std::size_t row_index) const
{
	auto const element = buffer_[row_index];
	if (element.indicator == SQL_NULL_DATA) {
		return {};
	} else {
		return description_->make_field(element.data_pointer);
	}
}

column_info column::get_info() const
{
	return {description_->name(), description_->get_type_code(), description_->supports_null_values()};
}

}
