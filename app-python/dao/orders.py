from exceptions.notfound import NotFoundException


class OrderDAO:
    def __init__(self, driver):
        self.driver = driver

    def create_orders(self, orders):
        def writeOrder(tx, order):
            query = """
            MERGE (o:Order { orderId: $orderId })
            MERGE (c:Customer { customerId: $customerId })
            MERGE (r:Recipients { recipientHash: $shippingName})
            MERGE (cn:Country { countryName: $shippingCountry})
            MERGE (ct:City { cityName: $shippingCity})
            MERGE (a:Address { addressHash: $shippingAddress})
            MERGE (p:Product { productId: $productId})
            MERGE (c)-[:PURCHASED]->(o)
            MERGE (o)-[sl:SHIPPED_LOCATION]->(a)
            MERGE (o)-[:SHIPPED_RECIPIENT]->(r)
            MERGE (ct)-[:CITY_OF]->(cn)
            MERGE (a)-[:PHYSICAL_LOCATION]->(ct)
            MERGE (o)-[cont:CONTAINS]->(p)
            SET r.recipientName = $shippingName, o.totalValue = $totalValue, cont.quantity = $quantity, 
            cont.discount = $discount, cont.unitPrice = $unitPrice;"""
            tx.run(query, orderId=order["orderId"], customerId=order["customerId"], \
                shippingName=order["shippingName"], shippingCountry=order["shippingCountry"], \
                    shippingCity=order["shippingCity"], shippingAddress=order["shippingAddressText"], \
                        totalValue=order["totalValue"], productId=order["product"]["productId"], \
                            quantity=order["product"]["quantity"], discount=order["product"]["discount"], \
                                unitPrice=order["product"]["unitPrice"])

            return 1

        count = 0
        with self.driver.session() as session:
            for order in orders:  
                count += session.write_transaction(writeOrder, order)    

        return count