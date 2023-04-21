import requests
from py2neo import Graph, Node, Relationship
import py2neo
import json
import time

# Define a function to recursively process events
def process_event(graph, event):
    node_id = event['id']
    node_label = 'Event'
    node = Node(node_label, id=node_id)
    graph.merge(node, node_label, 'id')
    for key, value in event.items():
        if isinstance(value, dict):
            link = value.get('url')
            if link:
                link_label = key.title()
                link_node = Node(link_label, url=link)
                graph.merge(link_node, link_label, 'url')
                rel = Relationship(node, link_label, link_node)
                graph.merge(rel)

                r = requests.get(link)
                if r.status_code == 200:
                    link_data = r.json()
                    if isinstance(link_data, list):
                        for item in link_data:
                            if isinstance(item, dict):
                                process_event(graph, item)
                    elif isinstance(link_data, dict):
                        process_event(graph, link_data)

# Define the main function to create the graph database
def create_graph_database(uri, username, password, api_url):
    while True:
        try:
            graph = Graph(uri, auth=(username, password))
            response = requests.get(api_url)
            if response.status_code == 200:
                events = response.json()
                for event in events:
                    process_event(graph, event)
            break
        except py2neo.errors.ConnectionUnavailable:
            print("Connection failed, retrying in 10 seconds...")
            time.sleep(10)

# Call the main function to create the graph database
create_graph_database("bolt://localhost:7687", "neo4j", "password", "https://api.github.com/events")
