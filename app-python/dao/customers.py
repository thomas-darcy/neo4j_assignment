class CustomerDAO:
    def __init__(self, driver):
        self.driver = driver

    def create_customers(self, customers):
        def writeCustomer(tx, customer):
            query = """MERGE (m:Customer { customerId: $customerId })
            MERGE (c:Country { countryName: $country})
            MERGE (ct:City { cityName: $city})
            MERGE (a:Address { addressHash: $addressText})
            MERGE (ct)-[:CITY_OF]->(c)
            MERGE (a)-[:PHYSICAL_LOCATION]->(ct)     
            MERGE (m)-[:REGISTERED_TO]->(a)
            SET m.customerName = $customerName, m.contactName = $contactName, m.contactRole = $contactTitle, a.addressText = $addressText;"""

            tx.run(query, customerId=customer["customerId"], country=customer["country"], city=customer["city"], addressText=customer["addressText"], customerName=customer["customerName"], contactName=customer["contactName"], contactTitle=customer["contactTitle"]).consume()
            
            return 1

        count = 0
        with self.driver.session() as session:
            for customer in customers:  
                count += session.write_transaction(writeCustomer, customer)    

        return count