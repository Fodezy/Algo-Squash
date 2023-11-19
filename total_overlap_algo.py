from datetime import datetime, timedelta
from itertools import combinations
import random
import json

# Function to generate time slots within a specified range
def generate_times(start_time_str, end_time_str, fmt='%I:%M %p'):
    """Generate time slots between two times."""
    times = []
    start_time = datetime.strptime(start_time_str, fmt)
    end_time = datetime.strptime(end_time_str, fmt)

    # Add each hour to the list
    while start_time <= end_time:
        times.append(start_time.strftime(fmt))
        start_time += timedelta(hours=1)

    return times

# Function to find common available time slots between two users
def find_common_availabilities(user1, user2, max_slots=14, max_daily_slots=2):
    """Find common available time slots, with weekly and daily limits."""
    common_availabilities = {}
    weekly_slots = 0

    # Check each day for overlapping times
    for day in user1['availability']:
        if day in user2['availability']:
            common_times = []
            daily_slots = 0
            for time in generate_times('8:00 AM', '8:00 PM'):
                if (user1['availability'][day].get(time, False) and
                        user2['availability'][day].get(time, False)):
                    if daily_slots < max_daily_slots and weekly_slots < max_slots:
                        common_times.append(time)
                        daily_slots += 1
                        weekly_slots += 1

            if common_times:
                common_availabilities[day] = common_times

    return common_availabilities

# Calculate the total duration of overlapping time slots
def calculate_duration(common_availabilities):
    """Calculate total duration of overlapping time slots."""
    return sum(len(times) for times in common_availabilities.values())

# Find the best matches based on the maximum overlap in availability
def find_best_matches(users):
    """Find best matches for all users."""
    overlaps = {}
    common_times_dict = {}  # Stores common available times for each match

    # Compare each pair of users
    for (id1, user1), (id2, user2) in combinations(users.items(), 2):
        common_availabilities = find_common_availabilities(user1, user2)
        total_overlap = calculate_duration(common_availabilities)
        
        if total_overlap > 0:  # Only consider pairs with a non-zero overlap
            overlaps[(id1, id2)] = total_overlap
            common_times_dict[(id1, id2)] = common_availabilities

    matches = {}
    matched_indices = set()

    # Find the best match for each user, avoiding duplicate matches
    while overlaps:
        best_match = max(overlaps, key=overlaps.get)
        matched_indices.update(best_match)
        matches[best_match] = overlaps[best_match]

        # Remove already matched users from further consideration
        overlaps = {pair: time for pair, time in overlaps.items()
                    if pair[0] not in matched_indices and pair[1] not in matched_indices}

    return matches, common_times_dict

# Generate random users with random availability
def generate_users(num_of_users, busy_schedule_ratio):
    """Generate user details and random availability."""
    user_data = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    names = ['John', 'Jane', 'Bob', 'Alice', 'Joe', 'Jill', 'Bill', 'Sally', 'Jack', 'Jenny']
    email_domain = 'gmail.com'

    # Create user entries
    for user_id in range(1, num_of_users + 1):
        name = random.choice(names)
        email = f'{name.lower()}@{email_domain}'
        availability = {day: {time: random.choices([True, False], weights=[1, busy_schedule_ratio])[0]
                              for time in generate_times('8:00 AM', '8:00 PM')} for day in days}

        user_data[user_id] = {
            'name': name,
            'email': email,
            'availability': availability
        }

    return user_data

def user_details_and_common_times(users, matched_tuple_ids, matched_schedule):
    """Construct JSON with user details and common times."""
    id1, id2 = matched_tuple_ids
    user1_details = users.get(id1, {'name': '', 'email': ''})
    user2_details = users.get(id2, {'name': '', 'email': ''})
    common_times = matched_schedule

    result = {
        id1: user1_details,
        id2: user2_details,
        'timeslot': common_times
    }

    return json.dumps(result, indent=4)


def main():
    # Generate test users and find the best matches
    test_users = generate_users(10, 1)
    best_matches, common_times_dict = find_best_matches(test_users)
    for match, overlap in best_matches.items():
        print(user_details_and_common_times(test_users, match,common_times_dict[match]))
    return
    
    # Print the results, including specific overlapping times
    for match, overlap in best_matches.items():
        print(f"Match between User {match[0]} and User {match[1]}: Overlap Duration: {overlap} hours")
        for day, times in common_times_dict[match].items():
            print(f"  - Common times on {day}: {', '.join(times)}")

    users_without_matches = set(test_users.keys()) - set(user_id for match in best_matches for user_id in match)

    for notify in users_without_matches:
        print(f"Notify User {notify} that they do not have a match") 
    return
    
# Print the results, including specific overlapping times
main()