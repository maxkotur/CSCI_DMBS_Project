# CSCI_DBMS_Project

For this project we will be taking the dataset from the Events https://api.github.com/events dataset. This dataset contains a huge amount of jsons which we will be restructuring the dataset so it can be loaded into a SQL or Graph database. We have chosen to use a Graph database and we will be using python to this. The reason fro python is that python has several libraries for working with graph databases, such as Py2neo for Neo4j, and Graphene for ArangoDB. 

Here is our current plan to achieve our goal:
We will use a graph database library or driver that provides APIs to create nodes and relationships in the graph. First we load the JSON data into a Python object, such as a dictionary or list, using the built-in json module. Then we a graph database library or driver to connect to the graph database which depends on the type of graph.
After that, for each node in the JSON data, we will create a corresponding node in the graph database using the graph database library or driver. Therefore we can then customize the properties on the node using the properties in the JSON data. Finally for each relationship in the JSON data, we create a corresponding relationship in the graph database using the graph database library or driver. We can identify the start and end nodes of the relationship based on their IDs or properties.

Please give us any suggestions or things that we could add.
Thank you.

Here are the slides for the presentation:
# https://docs.google.com/presentation/d/1ItgLWj-AeQUp7Aw7RLaNI7VWalgrsyWA8p7I7DH9BJg/edit#slide=id.g23784840e88_0_18