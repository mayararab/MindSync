from datetime import timedelta

def rule_set_1(events):
    """Flag stress for >2 consecutive work meetings with breaks <15 minutes."""
    stress_points = []
    for i in range(len(events) - 2):
        if (events[i]['type'] == 'work' and 
            events[i+1]['type'] == 'work' and 
            events[i+2]['type'] == 'work'):
            gap1 = events[i+1]['start'] - events[i]['end']
            gap2 = events[i+2]['start'] - events[i+1]['end']
            if gap1 < timedelta(minutes=15) and gap2 < timedelta(minutes=15):
                stress_points.append({
                    'time': events[i]['start'],
                    'reason': "Three consecutive meetings with short breaks"
                })
    return stress_points

def rule_set_2(events):
    """Flag stress for >4 hours of meetings or gaps <30 minutes."""
    total_meeting_time = sum(
        (event['end'] - event['start']).total_seconds() / 3600 
        for event in events if event['type'] == 'work'
    )
    stress_points = []
    if total_meeting_time > 3:
        stress_points.append({
            'time': events[0]['start'],
            'reason': f"Excessive meeting time ({total_meeting_time:.1f} hours)"
        })
    
    for i in range(len(events) - 1):
        if events[i]['type'] == 'work' and events[i+1]['type'] == 'work':
            gap = events[i+1]['start'] - events[i]['end']
            if gap < timedelta(minutes=30):
                stress_points.append({
                    'time': events[i]['end'],
                    'reason': "Short gap between meetings"
                })
    return stress_points

def predict_stress(events):
    """Combine both rule sets for stress prediction."""
    stress1 = rule_set_1(events)
    stress2 = rule_set_2(events)
    return stress1 + stress2

# Test the stress prediction
if __name__ == "__main__":
    from calendar_parser import parse_calendar, get_daily_events
    events = parse_calendar("data/calendar.json")
    daily_events = get_daily_events(events, "2025-08-13")
    stress_points = predict_stress(daily_events)
    for point in stress_points:
        print(f"Stress at {point['time']}: {point['reason']}")