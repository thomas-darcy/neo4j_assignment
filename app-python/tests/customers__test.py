import pytest
from neo4jdriver import get_driver
from dao.customers import CustomerDAO

testdata = [
   {
      "customerId":"1",
      "customerName":"Test Company 1",
      "contactName":"Michelle Test",
      "contactTitle":"Marketing Manager",
      "addressText":"1 Test Road",
      "city":"Sydney",
      "postCode":"2000",
      "country":"Australia"
   },
   {
      "customerId":"2",
      "customerName":"Test Company 2",
      "contactName":"Richard Test",
      "contactTitle":"Owner",
      "addressText":"356 Test Street",
      "city":"Boston",
      "region":"MA",
      "country":"USA"
   },
   {
      "customerId":"3",
      "customerName":"Test Company 3",
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


def test_create_customers(app):
    with app.app_context():
        driver = get_driver()

        dao = CustomerDAO(driver)

        output = dao.create_customers(testdata)
        assert output == 3