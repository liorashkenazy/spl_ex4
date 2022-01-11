# DTO represents hats table
class Hat:
    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


# DTO represents suppliers table
class Supplier:
    def __init__(self, id, name):
        self.id = id
        self.name = name


# DTO represents orders table
class Order:
    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat


