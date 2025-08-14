"""
MindSync — main entry point.

Role:
- CLI that lets the user choose a calendar JSON from /data.
- Orchestrates the pipeline:
  1) load & parse calendar (calendar_parser)
  2) detect stress points (stress_predictor)
  3) find free slots and place activities (timing)
  4) print a readable schedule/recommendations (suggestions + output)

Notes:
- Designed for the JSON fallback mode per coursework brief.
- Printed gap minutes (e.g., 60.0) represent the free-slot length, not activity length.
- Future work: stagger overlapping recommendations if multiple rules trigger at once.
Author: Mayar
"""

from calendar_parser import parse_calendar, get_daily_events
from stress_predictor import predict_stress
from timing import schedule_suggestions
import json
import os

def main():
    """
    Main function to run MindSync in command-line mode.
    Prompts user to select a calendar file and displays events, stress points, and suggestions.
    Handles errors for missing or invalid calendar files.
    """
    available_calendars = ["data/calendar.json", "data/busy_calendar.json", "data/light_calendar.json"]
    print("Available calendars:")
    for i, cal in enumerate(available_calendars, 1):
        print(f"{i}. {cal}")
    
    choice = input("Select a calendar (1-3, or press Enter for default 'data/calendar.json'): ")
    if choice in ['1', '2', '3']:
        calendar_file = available_calendars[int(choice) - 1]
    else:
        calendar_file = "data/calendar.json"
    
    try:
        # Verify file exists
        if not os.path.exists(calendar_file):
            raise FileNotFoundError(f"Calendar file {calendar_file} not found")
        
        # Load and parse calendar
        try:
            events = parse_calendar(calendar_file)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in {calendar_file}")
        
        daily_events = get_daily_events(events, "2025-08-13")
        
        # Print calendar events
        print(f"\nCalendar Events for 2025-08-13 (Using {calendar_file}):")
        if daily_events:
            for event in daily_events:
                print(f"- {event['title']}: {event['start']} to {event['end']}")
        else:
            print("- No events found")
        
        # Predict stress
        stress_points = predict_stress(daily_events)
        print("\nStress Points:")
        if stress_points:
            for point in stress_points:
                print(f"- {point['time']}: {point['reason']}")
        else:
            print("- None detected")
        
        # Schedule suggestions
        suggestions = schedule_suggestions(daily_events, stress_points)
        print("\nRecommended Schedule:")
        if suggestions:
            for s in suggestions:
                print(f"- {s['start']}: {s['suggestion']} ({s['duration']} mins)")
        else:
            print("- No suggestions scheduled")
    
    except Exception as e:
        print(f"Error: {str(e)}")
 # Pause to keep console open
    input("\nPress Enter to exit...")
if __name__ == "__main__":

    main()
