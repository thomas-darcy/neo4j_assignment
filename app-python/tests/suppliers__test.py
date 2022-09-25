import pytest
from neo4j import get_driver
from dao.suppliers import SupplierDAO

testdata = [
   {
      "supplierId":"1",
      "companyName":"Test Company 1",
      "contactName":"Michelle Test",
      "contactRole":"Marketing Manager",
      "addressText":"1 Test Road",
      "city":"Sydney",
      "postCode":"2000",
      "country":"Australia"
   },
   {
      "supplierId":"2",
      "companyName":"Test Company 2",
      "contactName":"Richard Test",
      "contactRole":"Owner",
      "addressText":"356 Test Street",
      "city":"Boston",
      "region":"MA",
      "country":"USA"
   },
   {
      "supplierId":"3",
      "companyName":"Test Company 3",
      "contactName":"John Test",
      "contactRole":"Purchasing Manager",
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


def test_return_positive_flag_on_all(app):
    with app.app_context():
        driver = get_driver()

        dao = SupplierDAO(driver)

        output = dao.create_suppliers(testdata)
        assert output == 3