## Modelling Dataset
### Background
This application is based on the **Retail North Wind Data**
[Located](https://gist.github.com/maruthiprithivi/072b526e20fe16a29f98db07f569861d)

### Use Cases
As a part of the modelling process the following use cases were designed
| Area      | Description |
| ----------- | ----------- |
| Potential account misuse      | Customers shipping outside of their registered address       |
| Potential account misuse   | Customers shipping to multiple cities/countries        |
| Fraudulent activity      | Anomalies in shipping with recipients outside of normal       |
| Potential account misuse   | Re-targetting workforce to cities with more Customers/Suppliers        |


### Data model
The json file as exported from arrows.app is located [Data Model JSON](/NorthWind%20Retail%20DataSet.json)[^4]
![Data Model](/assets/datamodel_02.png)

Historical data model's can be viewed in the assets directory, prefixed with ```data_model```
### Instructions
1. Copy the files from the data directory to the Virtual Machine and into the neo4j import directory ```/var/lib/neo4j/import``` [^5]
2. Install APOC by downloading version 4.4.0.1 from the releases page [^6] and moving to the neo4j plugins directory ```/var/lib/neo4j/plugins``` [^5][^7]
3. Start the neo4j service, once available open the Browser and login 
4. Test to ensure the import CSVs are readable. Can be read by using the following command, each table should return a count e.g.
```shell
LOAD CSV FROM "file:///northwind-categories.csv" AS line
RETURN count(*);
```
[Full script](/cypher/cypher_checkfiles.txt)

5. Create the schema using the generated Cypher [Cypher Create Model](/cypher/cypher_createmodel.txt)

6. Run the Cypher queries to create the nodes and relationships off the CSVs [Cypher Import CSV](/cypher/importcsv.txt)


### Cypher Queries
This section contains both cypher queries aiming to answer the use cases as raised earlier, plus also other potentially interesting ones.
##### Use Case - Potential account misuse
- Customers shipping outside of their registered address
![Cypher result](/assets/cypher_result_01.png)

```
MATCH (c:Customer)-[p:PURCHASED]-(o:Order), (c)-[r:REGISTERED_TO]->(ca:Address), (o)-[sl:SHIPPED_LOCATION]->(oa:Address)
WHERE oa.addressHash <> ca.addressHash
RETURN c, p, o
```
##### Use Case - Customers shipping to multiple cities/countries
![Cypher result](/assets/cypher_result_02.png)

```
MATCH (c:Customer)-[p:PURCHASED]->(o:Order), (c)-[r:REGISTERED_TO]->(ca:Address), (o)-[sl:SHIPPED_LOCATION]->(oa:Address),
(oa)-[:PHYSICAL_LOCATION]->(ct), (ct)-[:CITY_OF]-(cn)
WHERE oa.addressHash <> ca.addressHash
RETURN c.customerId AS UniqueCustomers, COUNT(DISTINCT ct.cityName) AS UniqueCities
```
##### Use Case - Anomalies in shipping with recipients outside of normal
##### Use Case - Re-targetting workforce to cities with more Customers/Suppliers
##### Identifying Customers that have Suppliers with the same product categories that might be in the same city for possible nurturing 
![Cypher result](/assets/cypher_result_03.png)

```
MATCH (c:Customer)-[:REGISTERED_TO]->(ca:Address), (ca)-[:PHYSICAL_LOCATION]->(cact), (cact)-[:CITY_OF]-(cacn),
(s:Supplier)-[:REGISTERED_TO]->(sa:Address), (sa)-[:PHYSICAL_LOCATION]->(sact), (sact)-[:CITY_OF]-(sacn),
(c)-[:PURCHASED]->(o:Order),
(o)-[:SHIPPED_LOCATION]->(oa:Address), (oa)-[:PHYSICAL_LOCATION]->(oact), (oact)-[:CITY_OF]-(oacn)
WHERE cact.cityName = sact.cityName or oact.cityName = sact.cityName
RETURN c.customerName, s.supplierName
```
There might either be an opportunity to go back and review the import data to ensure it's clean



[README.md](/README.md)

[^4]: Maybe look at restructuring the directory
[^5]: Also specified when starting the neo4j service
[^6]: https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases
[^7]: In hindsight hashing string values to make them an identifier appears to be a waste, thus APOC isn't essential
