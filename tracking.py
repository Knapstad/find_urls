import requests
def send_tracking(event_category, event_action, event_label="", event_value="0"):
    headers={'User-Agent': 'My User Agent 1.0'}
    try:
        requests.post(f"https://www.google-analytics.com/collect?v=1&t=event&tid=UA-169894513-3&cid=555&ec={event_category}&ea={event_action}&el={event_label}&ev={event_value}", headers=headers)
    except Exception as e:
        print(f"{e} Tracking failed")




