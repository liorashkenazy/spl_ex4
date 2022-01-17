import atexit
import sys

from repository import Repository
from dto import *

# parsing the configuration file
def populate_db_from_config(config_f, repo):
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

def execute_orders(order_f, repo, output_path):
    with open(order_f) as order_file, open(output_path, "w+") as output_file:
        lines = order_file.readlines()
        for line in lines:
            order(line.rstrip(), repo, output_file)

def order(line, repo, output_file):
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

def main():

    if len(sys.argv) != 5:
        print("Usage %s config_file orders_file output_file db_file" % sys.argv[0])
        return

    repo = Repository(sys.argv[4])
    atexit.register(repo.close)
    repo.create_tables()

    populate_db_from_config(sys.argv[1], repo)
    execute_orders(sys.argv[2], repo, sys.argv[3])

if __name__ == "__main__":
    main()
