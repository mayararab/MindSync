"""
calendar_parser — loads and normalizes calendar data.

Inputs:
- JSON files in /data (e.g., calendar.json, busy_calendar.json, light_calendar.json)

Outputs:
- A list of event dicts or objects with:
  { "title": str, "start": datetime, "end": datetime, "type": Optional[str] }

Responsibilities:
- Parse ISO timestamps and sort events by start time.
- Provide simple helpers for computing gaps/durations if needed.
"""

import json
from datetime import datetime

def parse_calendar(file_path):
    """Read and parse calendar JSON file."""
    with open(file_path, 'r') as file:
        events = json.load(file)
    
    # Convert string dates to datetime objects
    for event in events:
        event['start'] = datetime.fromisoformat(event['start'])
        event['end'] = datetime.fromisoformat(event['end'])
    return events

def get_daily_events(events, date_str):
    """Filter events for a specific date (e.g., '2025-08-13')."""
    target_date = datetime.fromisoformat(date_str).date()
    return [event for event in events if event['start'].date() == target_date]

# Test the parsing
if __name__ == "__main__":
    events = parse_calendar("data/calendar.json")
    daily_events = get_daily_events(events, "2025-08-13")
    for event in daily_events:

        print(f"{event['title']}: {event['start']} to {event['end']}")
