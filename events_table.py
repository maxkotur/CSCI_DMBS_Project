import sqlite3
import requests

# fetch the json data
response = requests.get("https://api.github.com/events")
json_data = response.json()

# create a connection to the database
conn = sqlite3.connect('github_events.db')

# create a cursor object
cur = conn.cursor()

# create the events table
cur.execute("""CREATE TABLE actor (
                event_id INTEGER PRIMARY KEY,
                actor_id INTEGER,
                login TEXT,
                display_login TEXT,
                gravatar_id TEXT,
                url TEXT,
                avatar_url TEXT
            )""")

cur.execute("""CREATE TABLE events (
                event_id INTEGER PRIMARY KEY,
                event_type TEXT,
                actor_id INTEGER,
                repo_id INTEGER,
                payload_id INTEGER,
                public INTEGER,
                created_at TEXT,
                org_id INTEGER
            )""")

cur.execute('''CREATE TABLE IF NOT EXISTS push_payload
               (event_id INTEGER, repo_id INTEGER, commits INTEGER, ref TEXT, PRIMARY KEY(event_id),
                FOREIGN KEY(event_id) REFERENCES events(id))''')
cur.execute('''CREATE TABLE IF NOT EXISTS pull_request_payload
               (event_id INTEGER, repo_id INTEGER, action TEXT, number INTEGER, PRIMARY KEY(event_id),
                FOREIGN KEY(event_id) REFERENCES events(id))''')
cur.execute('''CREATE TABLE IF NOT EXISTS issues_payload
               (event_id INTEGER, repo_id INTEGER, action TEXT, number INTEGER, PRIMARY KEY(event_id),
                FOREIGN KEY(event_id) REFERENCES events(id))''')
cur.execute('''CREATE TABLE IF NOT EXISTS release_payload
               (event_id INTEGER, repo_id INTEGER, action TEXT, name TEXT, tag_name TEXT, PRIMARY KEY(event_id),
                FOREIGN KEY(event_id) REFERENCES events(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS org
               (event_id INTEGER PRIMARY KEY,
                org_id INTEGER,
                login TEXT,
                gravatar_id TEXT,
                url TEXT,
                avatar_url TEXT)''')

# loop through each event and extract org data
for event in json_data:
    if 'org' in event and event['org'] is not None:
        org_id = event['org'].get('id')
        login = event['org'].get('login')
        gravatar_id = event['org'].get('gravatar_id')
        url = event['org'].get('url')
        event_id = event['id']
        avatar_url = event['org'].get('avatar_url')
        
        # insert org data into org table
        cur.execute("INSERT INTO org (event_id, org_id, login, gravatar_id, url, avatar_url) VALUES (?, ?, ?, ?, ?, ?)",
                    (event_id, org_id, login, gravatar_id, url, avatar_url))

# Loop through the data and insert into the appropriate table
for event in json_data:
    event_id = event["id"]
    repo_id = event["repo"]["id"]
    event_type = event["type"]
    payload = event["payload"]
    if event_type == "PushEvent":
        commits = payload.get("size")
        ref = payload.get("ref")
        cur.execute("INSERT INTO push_payload VALUES (?, ?, ?, ?)", (event_id, repo_id, commits, ref))
    elif event_type == "PullRequestEvent":
        action = payload.get("action")
        number = payload.get("number")
        cur.execute("INSERT INTO pull_request_payload VALUES (?, ?, ?, ?)", (event_id, repo_id, action, number))
    elif event_type == "IssuesEvent":
        action = payload.get("action")
        number = payload.get("number")
        cur.execute("INSERT INTO issues_payload VALUES (?, ?, ?, ?)", (event_id, repo_id, action, number))
    elif event_type == "ReleaseEvent":
        action = payload.get("action")
        name = payload.get("name")
        tag_name = payload.get("tag_name")
        cur.execute("INSERT INTO release_payload VALUES (?, ?, ?, ?, ?)", (event_id, repo_id, action, name, tag_name))


# Insert data into the 'actor' table
for event in json_data:
    event_id = event.get('id')
    actor_id = event.get('actor', {}).get('id')
    login = event.get('actor', {}).get('login')
    display_login = event.get('actor', {}).get('display_login')
    gravatar_id = event.get('actor', {}).get('gravatar_login')
    url = event.get('actor', {}).get('url')
    avatar_url = event.get('actor', {}).get('avatar_url')
    cur.execute("""INSERT INTO actor
                    (event_id, actor_id, login, display_login, gravatar_id, url, avatar_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (event_id, actor_id, login, display_login, gravatar_id, url, avatar_url))

# populate the events table with data from the JSON
for event in json_data:
    # extract values from the JSON and handle None values
    event_id = event.get('id')
    event_type = event.get('type')
    actor_id = event.get('actor', {}).get('id')
    repo_id = event.get('repo', {}).get('id')
    payload_id = event.get('payload', {}).get('push_id')
    public = int(event.get('public', False))
    created_at = event.get('created_at')
    org_id = event.get('org', {}).get('id')

    # insert the data into the events table
    cur.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (event_id, event_type, actor_id, repo_id, payload_id, public, created_at, org_id))


# commit changes and close the connection
conn.commit()
conn.close()