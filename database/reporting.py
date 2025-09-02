from database.database import Database


def report():
    database = Database()
    fixed_length_columns = database.get_all_fixed_length_columns()
