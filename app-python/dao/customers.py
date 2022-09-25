class CustomerDAO:
    def __init__(self, driver):
        self.driver = driver

    def create_customers(self, customers):
        def writeCustomer(tx, customer):
            query = """
            MERGE (m:Customer { customerId: {customerId} })
            MERGE (c:Country { countryName: {country}})
            MERGE (ct:City { cityName: {city}})
            MERGE (a:Address { addressHash: apoc.util.sha512([{address}])})"""
            if customer["postCode"] != None and len(customer["postCode"]) > 0:
                query = query + """ MERGE (pc:PostCodes { postcodeHash: apoc.util.sha512([{postcode}])})
                                    MERGE (a)-[:POSTAL_LOCATION]->(pc)
                                    MERGE (PC)-[:MAILING_IDENTIFIER]->(cn)
            """
            query = query + """ 
            MERGE (ct)-[:CITY_OF]->(c)
            MERGE (a)-[:PHYSICAL_LOCATION]->(ct)     
            MERGE (m)-[:REGISTERED_TO]->(a)
            SET m.customerName = {customerName}, m.contactName = {contactName}, m.contactRole = {contactTitle}, a.addressText = {address}"""
            if customer["postCode"] != None and len(customer["postCode"]) > 0:
                query = query + """ , pc.postCode = {postCode} """
            if customer["region"] != None and len(customer["region"]) > 0:
                query = query + """ , ct.region = {region} """
            query = query + """;"""
            query = query.format(customerId=customer["customerId"], country=customer["country"], city=customer["city"], address=customer["address"], postCode=customer["postCode"], customerName=customer["customerName"], contactName=customer["contactName"], contactTitle=customer["contactTitle"])

            tx.run(query)

            return 1

        customers = 0
        with self.driver.session() as session:
            for customer in customers:  
                customers += session.run(writeCustomer, customer)    

        return customers