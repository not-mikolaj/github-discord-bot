import json
import os
import urllib3

http = urllib3.PoolManager()

def lambda_handler(event, context):
discord_url = os.environ['DISCORD_URL']

try:
body = json.loads(event.get('body', '{}'))
headers = event.get('headers', {})
event_type = headers.get('x-github-event', 'unknown_event')
repo_name = body.get('repository', {}).get('full_name', 'Unknown repo')
sender = body.get('sender', {}).get('login', 'Unknown user')
repo_url = body.get('repository', {}).get('html_url', '')

message_detail = ""

# Obsługa push
if event_type == 'push':
commits = body.get('commits', [])
commit_messages = "\n".join([f"- {c.get('message', '')} ({c.get('url', '')})" for c in commits])
message_detail = f"\n📝 Commity:\n{commit_messages or 'Brak commitów'}"

# Obsługa Pull Request
elif event_type == 'pull_request':
action = body.get('action', '')
pr = body.get('pull_request', {})
pr_title = pr.get('title', '')
pr_user = pr.get('user', {}).get('login', '')
pr_url = pr.get('html_url', '')
message_detail = f"\n🔀 Pull Request **{action}**: [{pr_title}]({pr_url}) od **{pr_user}**"

# Obsługa Issues
elif event_type == 'issues':
action = body.get('action', '')
issue = body.get('issue', {})
issue_title = issue.get('title', '')
issue_url = issue.get('html_url', '')
message_detail = f"\n🐞 Issue **{action}**: [{issue_title}]({issue_url})"

# Obsługa Issue Comments
elif event_type == 'issue_comment':
action = body.get('action', '')
comment = body.get('comment', {}).get('body', '')
url = body.get('comment', {}).get('html_url', '')
message_detail = f"\n💬 Komentarz **{action}**: \"{comment}\" ({url})"

# Obsługa Release
elif event_type == 'release':
action = body.get('action', '')
release = body.get('release', {})
rel_name = release.get('name', '')
rel_url = release.get('html_url', '')
message_detail = f"\n📦 Release **{action}**: [{rel_name}]({rel_url})"

# Obsługa Fork
elif event_type == 'fork':
forkee = body.get('forkee', {})
fork_url = forkee.get('html_url', '')
message_detail = f"\n🍴 Repozytorium zostało sforkowane: {fork_url}"

# Obsługa Create (branch / tag)
elif event_type == 'create':
ref_type = body.get('ref_type', '')
ref_name = body.get('ref', '')
message_detail = f"\n✨ Utworzono {ref_type}: `{ref_name}`"

# Obsługa Delete (branch / tag)
elif event_type == 'delete':
ref_type = body.get('ref_type', '')
ref_name = body.get('ref', '')
message_detail = f"\n🗑️ Usunięto {ref_type}: `{ref_name}`"

# Obsługa Watch (Star)
elif event_type == 'watch':
action = body.get('action', '')
message_detail = f"\n⭐ Repozytorium zostało {action} przez {sender}"

# Domyślna obsługa
else:
message_detail = f"\nℹ️ Zdarzenie typu `{event_type}` nie ma dedykowanej obsługi.\nDane: {json.dumps(body)[:500]}..."

discord_payload = {
    "content": f"📢 **GitHub Event:** `{event_type}`",
    "embeds": [{
        "title": f"Zdarzenie w {repo_name}",
        "description": f"👤 Użytkownik **{sender}** wykonał akcję.{message_detail}",
        "url": repo_url,
        "color": 5814783
    }]
}

encoded_payload = json.dumps(discord_payload).encode('utf-8')
response = http.request(
    'POST',
    discord_url,
    body=encoded_payload,
    headers={'Content-Type': 'application/json'}
)

return {
    'statusCode': 200,
    'body': json.dumps('Wiadomość wysłana!')
}

except Exception as e:
    print(f"Błąd: {e}")
return {
    'statusCode': 500,
    'body': json.dumps(f"Błąd: {str(e)}")
}
