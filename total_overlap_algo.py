from datetime import datetime, timedelta
from itertools import combinations
import random

# Function to generate time slots
def generate_times(start_time_str, end_time_str, fmt='%I:%M %p'):
    times = []
    start_time = datetime.strptime(start_time_str, fmt)
    end_time = datetime.strptime(end_time_str, fmt)
    
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time.strftime(fmt))
        current_time += timedelta(hours=1)

    return times

# Function to find common availabilities between two users
def find_common_availabilities(user1, user2):
    common_availabilities = {}
    for day in user1['availability']:
        if day in user2['availability']:
            common_times = []
            for time in generate_times('8:00 AM', '8:00 PM'):
                if user1['availability'][day].get(time, False) and user2['availability'][day].get(time, False):
                    common_times.append(time)
            if common_times:
                common_availabilities[day] = common_times
    return common_availabilities

# Calculate total overlapping hours
def calculate_duration(common_availabilities):
    return sum(len(times) for times in common_availabilities.values())

# Find the best matches
def find_best_matches(users):
    overlaps = {}

    for (id1, user1), (id2, user2) in combinations(users.items(), 2):
        common_availabilities = find_common_availabilities(user1, user2)
        total_overlap = calculate_duration(common_availabilities)
        overlaps[(id1, id2)] = total_overlap

    matches = {}
    matched_indices = set()

    while overlaps:
        best_match = max(overlaps, key=overlaps.get)
        matched_indices.update(best_match)
        matches[best_match] = overlaps[best_match]

        overlaps = {pair: time for pair, time in overlaps.items() if pair[0] not in matched_indices and pair[1] not in matched_indices}

    return matches

def generate_users(num_of_users, busy_schedule_ratio):
    grand_dict = {}
    for user_id in range(1, num_of_users + 1):  # Adjusted to include num_of_users
        availability = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        times = generate_times('8:00 AM', '8:00 PM')  # Using the generate_times function for consistency
        
        skill = ['Beginner', 'Intermediate', 'Advanced']
        
        for day in days:
            availability[day] = {}
            for time in times:
                availability[day][time] = random.choices([True, False], weights=[1, busy_schedule_ratio])[0]
        
        grand_dict[user_id] = {'availability': availability, 'skill': random.choice(skill)}
    return grand_dict

def main():
    test_users = generate_users(120, 3)
    best_matches = find_best_matches(test_users)

    # Print Results
    for match, overlap in best_matches.items():
        print(f"Match between User {match[0]} and User {match[1]}: Overlap Duration: {overlap} hours")
