import pytest
from neo4j import get_driver
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
      "products":[
         {
            "productId":"1",
            "quantity":1,
            "discount":0.0,
            "unitPrice":16.0
         }
      ]
   },
   {
      "orderId":"2",
      "customerId":"4",
      "totalValue":3750,
      "shippingName":"Test Recipient",
      "shippingAddressText":"Test Address 1",
      "shippingCity":"Sydney",
      "shippingCountry":"Australia",
      "products":[
         {
            "productId":"5",
            "quantity":100,
            "discount":0.0,
            "unitPrice":30.50
         },
         {
            "productId":"4",
            "quantity":100,
            "discount":0.0,
            "unitPrice":7.0
         }
      ]
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