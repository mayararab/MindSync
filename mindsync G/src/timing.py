from datetime import timedelta
from suggestions import get_suggestions

def find_free_slots(events, min_duration=timedelta(minutes=15)):
    """Find gaps in schedule >= min_duration."""
    free_slots = []
    for i in range(len(events) - 1):
        gap_start = events[i]['end']
        gap_end = events[i+1]['start']
        if gap_end - gap_start >= min_duration:
            free_slots.append({'start': gap_start, 'end': gap_end})
    return free_slots

def schedule_suggestions(events, stress_points):
    """Insert suggestions into free slots."""
    free_slots = find_free_slots(events)
    schedule = []
    for point in stress_points:
        for slot in free_slots:
            if slot['start'] >= point['time']:
                suggestion = get_suggestions(point)[0]  # Pick first suggestion
                schedule.append({
                    'start': slot['start'],
                    'suggestion': suggestion,
                    'duration': (slot['end'] - slot['start']).total_seconds() / 60
                })
                break  # Use the first suitable slot
    return schedule

# Test the timing optimization
if __name__ == "__main__":
    from calendar_parser import parse_calendar, get_daily_events
    from stress_predictor import predict_stress
    
    # Load calendar and predict stress
    events = parse_calendar("data/calendar.json")
    daily_events = get_daily_events(events, "2025-08-13")
    stress_points = predict_stress(daily_events)
    
    # Schedule suggestions
    suggestions = schedule_suggestions(daily_events, stress_points)
    for s in suggestions:
        print(f"At {s['start']}: {s['suggestion']} ({s['duration']} mins)")