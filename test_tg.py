import requests
import json

def test():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    bot_token = config['telegram']['bot_token']
    chat_id = config['telegram']['chat_id']
    
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    print(f"Testing local bot token...")
    resp = requests.get(url)
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")

    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "Hello from testing script!"
    }
    resp2 = requests.post(send_url, json=payload)
    print(f"Send Msg Status Code: {resp2.status_code}")
    print(f"Send Msg Response: {resp2.text}")
    
if __name__ == "__main__":
    test()
