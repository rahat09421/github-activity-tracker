import sys, json, urllib.request, urllib.error

def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    
    headers = {"User-Agent": "Python-CLI-App"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data:
                print(f"No recent activity found for user '{username}'.")
                return
            
            display_activity(data, username)
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: The username '{username}' does not exist on GitHub.")
        elif e.code == 403:
            print("Error: API rate limit exceeded. Please try again later.")
        else:
            print(f"Error: GitHub API returned an error (HTTP {e.code})")
            
    except urllib.error.URLError:
        print("Error: Could not connect to the internet.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
                
def display_activity(events,username):
    
    print(f"Output for {username}:")
    for event in events[:10]:
        repo_name = event['repo']['name']
        event_type = event['type']
        
        if event_type == "PushEvent":
            commit_count = len(event.get("payload", {}).get("commits", []))
            print(f"- Pushed {commit_count} commit(s) to {repo_name}")
        elif  event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            print(f"- {action.capitalize()} an issue in {repo_name}")
        elif event_type == "WatchEvent":
            print(f"- Starred {repo_name}")
        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type")
            print(f"- Created a new {ref_type} in {repo_name}")
        else:
            clean_name = event_type.replace("Event", "")
            print(f"- {clean_name} in {repo_name}")
            
def main():
    if len(sys.argv) <2:
        print("Usage: python github_activity.py <username>")
        return
    username = sys.argv[1]
    fetch_activity(username)

if __name__ == "__main__":
    main()