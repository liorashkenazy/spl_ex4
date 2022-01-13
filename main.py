import atexit
import sys

from repository import Repository
from dto import *


def main():
    output_file = open(sys.argv[3], "w+")

    # parsing the configuration file
    def generate_db(config_f):
        with open(config_f) as config_file:
            first_line = config_file.readline().split(',')
            hats_num_entries = int(first_line[0])
            sup_num_entries = int(first_line[1])
            for i in range(hats_num_entries + sup_num_entries):
                line = config_file.readline().rstrip()
                params = line.split(',')
                if i < hats_num_entries:
                    repo.hats.insert(Hat(*params))
                else:
                    repo.suppliers.insert(Supplier(*params))

    def execute_order(order_f):
        with open(order_f) as order_file:
            lines = order_file.readlines()
            for line in lines:
                order(line.rstrip())

    def order(line):
        params = line.split(',')
        order_hat = repo.hats.find_by_order("supplier", topping=params[1])[0]
        # update hats table
        if order_hat.quantity == 1:
            repo.hats.delete(id=order_hat.id)
        else:
            repo.hats.update({'quantity': order_hat.quantity - 1}, {'id': order_hat.id})

        # insert the order to orders table
        repo.orders.insert(Order(params[0], order_hat.id))

        # add the order to output file
        order_sup = repo.suppliers.find(id=order_hat.supplier)[0]
        output_file.write(params[1] + "," + order_sup.name + "," + params[0])
        output_file.write('\n')

    repo = Repository(sys.argv[4])
    atexit.register(repo.close)
    repo.create_tables()
    generate_db(sys.argv[1])
    execute_order(sys.argv[2])


if __name__ == "__main__":
    main()
