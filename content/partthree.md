## Graph Enabled Ingestion (Python)

An application has been developed showcasing the ability to send JSON to a Flask endpoint and write the results to the graph developed in [part two](/content/parttwo.md).
Required dependencies:
- Python 3.9.x
- neo4j Enterprise 4.4.x

### Run the app

1. Navigate to the app-python directory
2. Execute the command 
```pip install -r requirements.txt```
3. Make a copy of ```.env.example``` and rename to ```.env```
4. Update the configuration values in the new environment file

| Name      | Description |
| ----------- | ----------- |
| FLASK_APP | The entry point for application. Only change if you know what you're doing |
| FLASK_ENV | The environment the application is running in (production/development) |
| FLASK_RUN_PORT | The port the application will be listening on |
| NEO4J_URI | The connection URI for the neo4j driver |
| NEO4J_USERNAME | Username for the neo4j connection |
| NEO4J_PASSWORD | Password for the neo4j connection |
5. Execute the command 
```flask run```

### Methods

#### Create Order
```POST api/orders/create```

###### Example Payload
```
[
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
```
###### Response
```
{
    "date": The date the API was called,
    "recordsSynced": The number of records synced
}
```
#### Create Customer

```POST api/customers/create```

###### Example Payload
```
[
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
```
###### Response
```
{
    "date": The date the API was called,
    "recordsSynced": The number of records synced
}
```

#### Create Supplier

```POST api/suppliers/create```

###### Example Payload
```
[
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
```

###### Response
```
{
    "date": The date the API was called,
    "recordsSynced": The number of records synced
}
```

[README.md](/README.md)