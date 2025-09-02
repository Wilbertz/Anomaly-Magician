from codes.Length2CodeMap import Length2CodeMap
from database.database import Database

class Reporting:

    @staticmethod
    def report():
        database = Database()
        code_map = Length2CodeMap()
        fixed_length_columns = database.get_all_fixed_length_columns()

        for column in fixed_length_columns:
            average_length = database.get_average_column_length(column)
            codes = code_map.get_code(int(average_length))
            if codes:
                for code in codes:
                    if database.check_column_values_against_code(column, code):
                        print(f"\nColumn {column.column_name} in table {column.table} with average length {average_length} could be checked against code {code.name}")


