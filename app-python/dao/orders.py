from exceptions.notfound import NotFoundException


class OrderDAO:
    def __init__(self, driver):
        self.driver = driver

    def create_orders(self, orders):
        def writeOrder(tx, order):
            query = """
            MERGE (o:Order { orderId: {orderId} })
            MERGE (c:Customer { customerId: {customerId} })
            MERGE (r:Recipients { recipientHash: apoc.util.sha512([{shippingName}])})
            MERGE (cn:Country { countryName: {shippingCountry}})
            MERGE (ct:City { cityName: {shippingCity}})
            MERGE (a:Address { addressHash: apoc.util.sha512([{shippingAddress}])})
            """
            if 'postCode' in order and order["postCode"] != None and len(order["postCode"]) > 0:
                query = query + """ MERGE (pc:PostCodes { postcodeHash: apoc.util.sha512([{shippingPostcode}])})
                                    MERGE (a)-[:POSTAL_LOCATION]->(pc)
                                    MERGE (PC)-[:MAILING_IDENTIFIER]->(cn)
            """
            query = query + """ 
            MERGE (c)-[:PURCHASED]->(o)
            MERGE (o)-[sl:SHIPPED_LOCATION]->(a)
            MERGE (o)-[:SHIPPED_RECIPIENT]->(r)
            MERGE (ct)-[:CITY_OF]->(cn)
            MERGE (a)-[:PHYSICAL_LOCATION]->(ct)
            SET r.recipientName = {shippingName}"""
            if 'postCode' in order and order["postCode"] != None and len(order["postCode"]) > 0:
                query = query + """ , pc.postCode = {shippingPostcode} """
            query = query + """;"""

            query = query.format(orderId=order["orderId"], customerId=order["customerId"], shippingName=order["shippingName"], shippingCountry=order["shippingCountry"], shippingCity=order["shippingCity"], shippingAddress=order["shippingAddress"], shippingPostcode=order["shippingPostcode"])

            tx.run(query)

            return 1

        count = 0
        with self.driver.session() as session:
            for order in orders:  
                count += session.write_transaction(writeOrder, order)    

        return count