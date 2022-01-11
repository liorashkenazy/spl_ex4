import atexit
import sqlite3
import sys

from dao import DAO
from dto import *


class Repository:
    def __init__(self, db_path):
        self._conn = sqlite3.connect(db_path)
        self.hats = DAO(Hat, self._conn)
        self.suppliers = DAO(Supplier, self._conn)
        self.orders = DAO(Order, self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE IF NOT EXISTS hats (
            id       INT         PRIMARY KEY,
            topping  STRING      NOT NULL,
            supplier INT         NOT NULL,
            quantity INT         NOT NULL,
            
            FOREIGN KEY(supplier)     REFERENCES suppliers(id)
        );
        
        CREATE TABLE IF NOT EXISTS suppliers (
            id       INT         PRIMARY KEY,
            name     STRING      NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS orders (
            id       INT         PRIMARY KEY,
            location STRING      NOT NULL,
            hat      INT         NOT NULL,
            
            FOREIGN KEY(hat)         REFERENCES hats(id)
        );
    """)
