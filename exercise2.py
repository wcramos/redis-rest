import os
import base64
import json
import requests
import urllib3
import sys

# Environment variables
BASE_URL = os.getenv("API_URL")
USERNAME = os.getenv("API_USER")
PASSWORD = os.getenv("API_PASSWORD")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_env_variables():
    if not all([BASE_URL, USERNAME, PASSWORD]):
        print("Error: API_URL, API_USER, and API_PASSWORD environment variables must be set.", file=sys.stderr)
        sys.exit(1)

def get_basic_auth():
    credentials = f"{USERNAME}:{PASSWORD}".encode("utf-8")
    return base64.b64encode(credentials).decode("utf-8")

def send_http_request(method, endpoint, payload=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Basic {get_basic_auth()}",
        "Content-Type": "application/json"
    }
    
    response = requests.request(method, url, headers=headers, json=payload, verify=False)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json()

def create_database():
    print("Creating a new database...")
    
    request_json = {
        "name": "my-redis-db",
        "memory_size": 100  # 100MB
    }
    
    response = send_http_request("POST", "/v1/bdbs", request_json)
    print(f"Database created with UID: {response['uid']}")
    return response["uid"]

def create_users():
    print("Creating users...")
    users = [
        {"email": "john.doe@example.com", "name": "John Doe", "role": "db_viewer", "password": "my-password"},
        {"email": "mike.smith@example.com", "name": "Mike Smith", "role": "db_member", "password": "my-password"},
        {"email": "cary.johnson@example.com", "name": "Cary Johnson", "role": "admin", "password": "my-password",}
    ]
    
    for user in users:
        send_http_request("POST", "/v1/users", user)
        print(f"User {user['name']} created successfully!")

def list_users():
    print("\nFetching list of users...")
    
    response = send_http_request("GET", "/v1/users")
    
    print("\nUsers in the system:")
    for user in response:
        print(f"- Name: {user['name']} | Role: {user['role']} | Email: {user['email']}")

def delete_database(db_id):
    print(f"\nDeleting database with UID: {db_id}")
    send_http_request("DELETE", f"/v1/bdbs/{db_id}")
    print("Database deleted successfully!")

def main():
    check_env_variables()
    
    if len(sys.argv) < 2:
        print("Usage: python script.py <CDB | CUSR | LUSR | DDB <db_id>>", file=sys.stderr)
        sys.exit(1)
    
    command = sys.argv[1].upper()
    
    try:
        if command == "CDB":
            create_database()
        elif command == "CUSR":
            create_users()
        elif command == "LUSR":
            list_users()
        elif command == "DDB":
            if len(sys.argv) < 3:
                print("Error: Missing database ID for deletion.", file=sys.stderr)
                sys.exit(1)
            delete_database(sys.argv[2])
        else:
            print("Invalid command. Use CDB, CUSR, LUSR, or DDB <db_id>.", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
