import pytest
from neo4jdriver import get_driver
from dao.suppliers import SupplierDAO

testdata = [
   {
      "supplierId":"1",
      "supplierName":"Test Company 1",
      "contactName":"Michelle Test",
      "contactTitle":"Marketing Manager",
      "addressText":"1 Test Road",
      "city":"Sydney",
      "postCode":"2000",
      "country":"Australia"
   },
   {
      "supplierId":"2",
      "supplierName":"Test Company 2",
      "contactName":"Richard Test",
      "contactTitle":"Owner",
      "addressText":"356 Test Street",
      "city":"Boston",
      "region":"MA",
      "country":"USA"
   },
   {
      "supplierId":"3",
      "supplierName":"Test Company 3",
      "contactName":"John Test",
      "contactTitle":"Purchasing Manager",
      "addressText":"Test Prominade",
      "city":"London",
      "country":"UK"
   }
]

@pytest.fixture(autouse=True)
def before_all(app):
    with app.app_context():
        driver = get_driver()

        with driver.session() as session:
            session.write_transaction(lambda tx: tx.run("""
                MATCH (n)
                DETACH DELETE n
            """))


def test_create_suppliers(app):
    with app.app_context():
        driver = get_driver()

        dao = SupplierDAO(driver)

        output = dao.create_suppliers(testdata)
        assert output == 3