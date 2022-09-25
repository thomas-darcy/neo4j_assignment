class SupplierDAO:
    def __init__(self, driver):
        self.driver = driver


    def create_suppliers(self, suppliers):
        def writeSupplier(tx, supplier):
            query = """
            MERGE (m:Supplier { supplierId: {supplierId} })
            MERGE (c:Country { countryName: {country}})
            MERGE (ct:City { cityName: {city}})
            MERGE (a:Address { addressHash: apoc.util.sha512([{address}])})"""
            if 'postCode' in supplier and supplier["postCode"] != None and len(supplier["postCode"]) > 0:
                query = query + """ MERGE (pc:PostCodes { postcodeHash: apoc.util.sha512([{postcode}])})
                                    MERGE (a)-[:POSTAL_LOCATION]->(pc)
                                    MERGE (PC)-[:MAILING_IDENTIFIER]->(cn)
            """
            query = query + """ 
            MERGE (ct)-[:CITY_OF]->(c)
            MERGE (a)-[:PHYSICAL_LOCATION]->(ct)     
            MERGE (m)-[:REGISTERED_TO]->(a)
            SET m.customerName = {customerName}, m.contactName = {contactName}, m.contactRole = {contactTitle}, a.addressText = {address}"""
            if 'postCode' in supplier and supplier["postCode"] != None and len(supplier["postCode"]) > 0:
                query = query + """ , pc.postCode = {postCode} """
            if 'region' in supplier and supplier["region"] != None and len(supplier["region"]) > 0:
                query = query + """ , ct.region = {region} """
            query = query + """;"""
            query = query.format(supplierId=supplier["supplierId"], country=supplier["country"], city=supplier["city"], address=supplier["address"], postCode=supplier["postCode"], customerName=supplier["customerName"], contactName=supplier["contactName"], contactTitle=supplier["contactTitle"])

            tx.run(query)

            return 1

        count = 0
        with self.driver.session() as session:
            for supplier in suppliers:  
                count += session.write_transaction(writeSupplier, supplier)    

        return count