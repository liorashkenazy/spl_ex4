# Generic DAO class
import inspect


class DAO:
    def __init__(self, dto_type, con):
        self._conn = con
        self._dto_type = dto_type
        # using the assumption that DTO classes are obeying the same naming conventions
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        col_names = ",".join(ins_dict.keys())
        params = list(ins_dict.values())
        quest_marks = ", ".join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})'.format(self._table_name, col_names, quest_marks)
        self._conn.execute(stmt, params)

    def find(self, **kwargs):
        col_names = list(kwargs.keys())
        params = list(kwargs.values())

        stmt = 'SELECT * FROM {} WHERE {}'.format(self._table_name,
                                                  ' AND '.join([col + '=?' for col in col_names]))
        c = self._conn.cursor()
        c.execute(stmt, params)
        return orm(c, self._dto_type)

    def update(self, set_values, cond):
        set_col_names = set_values.keys()
        set_params = set_values.values()

        cond_col_names = cond.keys()
        cond_params = cond.values()

        params_list = list(set_params) + list(cond_params)

        stmt = 'UPDATE {} SET {} WHERE {}'.format(self._table_name, ', '.join([set + '=?' for set in set_col_names]),
               ' AND '.join([cond + '=?' for cond in cond_col_names]))
        self._conn.execute(stmt, params_list)

    def delete(self, **kwargs):
        col_names = list(kwargs.keys())
        params = list(kwargs.values())

        stmt = 'DELETE FROM {} WHERE {}'.format(self._table_name, ' AND '.join([cond + '=?' for cond in col_names]))
        self._conn.execute(stmt, params)


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


def orm(cursor, dto_type):
    args = inspect.getfullargspec(dto_type.__init__).args

    # ignore the argument self
    args = args[1:]

    col_names = [column[0] for column in cursor.description]

    col_mapping = [col_names.index(arg) for arg in args]
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]
