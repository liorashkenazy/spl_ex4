import atexit
import sys

from repository import Repository
from dto import *

output_file = open(sys.argv[3], "w+")


# parsing the configuration file
def parse_config():
    with open(sys.argv[1]) as config_file:
        first_line = config_file.readline().split(',')
        hats_num_entries = int(first_line[0])
        sup_num_entries = int(first_line[1])
        for i in range(hats_num_entries):
            line = config_file.readline().rstrip()
            params = line.split(',')
            repo.hats.insert(Hat(*params))
        for j in range(sup_num_entries):
            line = config_file.readline().rstrip()
            params = line.split(',')
            repo.suppliers.insert(Supplier(*params))


def parse_order():
    with open(sys.argv[2]) as order_file:
        lines = order_file.readlines()
        for line in lines:
            order(line.rstrip())


def order(line):
    params = line.split(',')
    # TODO: fix this: should use the inventory from the first supplier (ordered by id)
    order_hat = repo.hats.find(topping=params[1])[0]
    # update hats table
    repo.hats.update({'quantity': order_hat.quantity - 1}, {'id': order_hat.id})
    if order_hat.quantity == 0:
        repo.hats.delete({'id': order_hat.id})

    # insert the order to orders table
    repo.orders.insert(Order(params[0], order_hat.id))

    # add the order to output file
    order_sup = repo.suppliers.find(id=order_hat.supplier)[0]
    output_file.write(params[1] + "," + order_sup.name + "," + params[0])
    output_file.write('\n')


repo = Repository(sys.argv[4])
atexit.register(repo.close)
repo.create_tables()
parse_config()
parse_order()
