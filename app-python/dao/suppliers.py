class SupplierDAO:
    def __init__(self, driver):
        self.driver = driver


    def create_suppliers(self, suppliers):
        def writeSupplier(tx, supplier):
            query = """
            MERGE (m:Supplier { supplierId: $supplierId })
            MERGE (c:Country { countryName: $country})
            MERGE (ct:City { cityName: $city})
            MERGE (a:Address { addressHash: $addressText})
            MERGE (ct)-[:CITY_OF]->(c)
            MERGE (a)-[:PHYSICAL_LOCATION]->(ct)     
            MERGE (m)-[:REGISTERED_TO]->(a)
            SET m.supplierName = $supplierName, m.contactName = $contactName, m.contactRole = $contactTitle, a.addressText = $addressText;"""

            tx.run(query, supplierId=supplier["supplierId"], country=supplier["country"], city=supplier["city"], addressText=supplier["addressText"], supplierName=supplier["supplierName"], contactName=supplier["contactName"], contactTitle=supplier["contactTitle"])

            return 1

        count = 0
        with self.driver.session() as session:
            for supplier in suppliers:  
                count += session.write_transaction(writeSupplier, supplier)    

        return count