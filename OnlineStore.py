class StoreProduct:
    """---------- Constructor ----------"""
    def __init__(self, product_name, price, stock = 0, category = "General"):
        self.product_name = product_name
        if price <= 0:
            self.price = 1.0
            print(f"Price shouldn't be lower than 0! Price set to ... {self.price}")
        else:
            self.price = price 
        if stock < 0:
            self.stock = 0
            print(f"The number of products can't be negative! New value for 'stock' ... {self.stock}")
        else:
            self.stock = stock 

        self.totalSales = 0
 
    """---------- Methods ----------"""
    
    """ Output Method """
    def outputDetails(self):
        print(f"{self.product_name} - {self.price} RON | Stock: {self.stock}")

    """ Restock """
    def restock(self, quantity):
        if quantity > 0:
            self.stock += quantity
        else:
            print(f"Please type a positive number to be added. Stock remains: {self.stock}.")
    """ Sales """
    def calculateSales(self, quantity):
        self.totalSales += quantity * self.price 

    """ Sell """
    def sell(self, quantity):
        if quantity > 0 and (quantity < self.stock):
            self.stock -= quantity
            print(f"Succes! You sold the items. Product: {self.product_name} - New stock: {self.stock}.")
            self.calculateSales(quantity)
        elif quantity <= 0:
            print(f"Please type a positive quantity to be sold. Stock remains: {self.stock}.")
        elif quantity > self.stock:
            print(f"You cand sell more than you have. Stock remains: {self.stock}")
    
    """ Discount """
    def applyDiscount(self, percentage):
        if percentage > 0 and percentage < 100:
            self.price = self.price - self.price * percentage/100
        else:
            print(f"Discount introduced must be wrong. Please keep in mind you can't apply a discout outside 1-99. Price remains: {self.price}.")

    """ Sales Report """
    def generateSalesReport(self):
        print(f"Total sales value: {self.totalSales} RON.")

    def __repr__(self):
        return  f"({self.product_name} - {self.price} RON | Stock: {self.stock})"

if __name__ == "__main__":
    product1 = StoreProduct("Laptop Lenovo", 2500, 10)
    product2 = StoreProduct("GEFORCE RTX 3070TI", 4000, 5)
    product1.outputDetails()
    product2.outputDetails()
    product1.restock(15)
    product1.restock(-9)
    product1.sell(7)
    product2.sell(3)
    product2.sell(100)
    product1.applyDiscount(10)
    product2.applyDiscount(-10)
    print(product1)
    print(product2)
    product1.generateSalesReport()
    products = {
        "p1" : product1,
        "p2" : product2,
    }
    print(products)

        