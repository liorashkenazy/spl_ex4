import atexit
import sqlite3

class Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.hats = DAO(Hat, self._conn)
        self.suppliers = DAO(Supplier, self._conn)
        self.orders = DAO(Order, self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript(""""
            CREATE TABLE hats (
            id       INT         PRIMARY KEY,
            topping  STRING      NOT NULL,
            supplier INT         NOT NULL,
            quantity INT         NOT NULL,
            
            FOREIGN KEY(supplier)     REFERENCES suppliers(id)
            );
            
            CREATE TABLE suppliers (
            id       INT         PRIMARY KEY,
            name     STRING      NOT NULL,
            );
            
            CREATE TABLE orders (
            id       INT         PRIMARY KEY,
            location STRING      NOT NULL,
            hat      INT         NOT NULL,
            
            FOREIGN KEY(hat)         REFERENCES hats(id)
            );
        """)


repo = Repository()
atexit.register(repo.close)
