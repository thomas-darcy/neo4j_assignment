import pytest
from neo4jdriver import get_driver
from dao.orders import OrderDAO

testdata = [
   {
      "orderId":"1",
      "customerId":"1",
      "totalValue":16,
      "shippingName":"Test Recipient",
      "shippingAddressText":"Test Address 1",
      "shippingCity":"Sydney",
      "shippingCountry":"Australia",
      "product":  {
            "productId":"1",
            "quantity":1,
            "discount":0.0,
            "unitPrice":16.0
      }
   },
   {
      "orderId":"2",
      "customerId":"4",
      "totalValue":3750,
      "shippingName":"Test Recipient",
      "shippingAddressText":"Test Address 1",
      "shippingCity":"Sydney",
      "shippingCountry":"Australia",
      "product":  {
            "productId":"3",
            "quantity":100,
            "discount":0.0,
            "unitPrice":375.0
      }
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


def test_create_orders(app):
    with app.app_context():
        driver = get_driver()

        dao = OrderDAO(driver)

        output = dao.create_orders(testdata)
        assert output == 2