from datetime import datetime, timedelta
from itertools import combinations
import random
import json

# Function to generate time slots within a specified range
def generate_times(start_time_str, end_time_str, fmt='%I:%M %p'):
    times = []
    start_time = datetime.strptime(start_time_str, fmt)
    end_time = datetime.strptime(end_time_str, fmt)
    
    # Loop through the time range and add each hour to the list
    current_time = start_time
    while current_time <= end_time:
        times.append(current_time.strftime(fmt))
        current_time += timedelta(hours=1)

    return times

# Function to find common available time slots between two users
def find_common_availabilities(user1, user2):
    common_availabilities = {}
    # Check each day for overlapping times
    for day in user1['availability']:
        if day in user2['availability']:
            common_times = []
            # Compare each time slot for both users
            for time in generate_times('8:00 AM', '8:00 PM'):
                if user1['availability'][day].get(time, False) and user2['availability'][day].get(time, False):
                    common_times.append(time)
            if common_times:
                common_availabilities[day] = common_times
    return common_availabilities

# Calculate the total duration of overlapping time slots
def calculate_duration(common_availabilities):
    return sum(len(times) for times in common_availabilities.values())

# Find the best matches based on the maximum overlap in availability
def find_best_matches(users):
    overlaps = {}
    common_times_dict = {}  # Stores common available times for each match

    # Compare each pair of users
    for (id1, user1), (id2, user2) in combinations(users.items(), 2):
        common_availabilities = find_common_availabilities(user1, user2)
        total_overlap = calculate_duration(common_availabilities)
        
        # Only consider pairs with a non-zero overlap
        if total_overlap > 0:
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
        overlaps = {pair: time for pair, time in overlaps.items() if pair[0] not in matched_indices and pair[1] not in matched_indices}

    return matches, common_times_dict  # Return both the matches and the common available times

# Generate random users with random availability
def generate_users(num_of_users, busy_schedule_ratio):
    grand_dict = {}
    # Create a user entry for each ID in the specified range
    for user_id in range(1, num_of_users + 1):
        availability = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        names = ['John', 'Jane', 'Bob', 'Alice', 'Joe', 'Jill', 'Bill', 'Sally', 'Jack', 'Jenny']
        email = 'gmail.com'
        
        # Use generate_times to create consistent time slots
        times = generate_times('8:00 AM', '8:00 PM')  
    
        # Randomly assign availability for each time slot
        for day in days:
            availability[day] = {}
            for time in times:
                availability[day][time] = random.choices([True, False], weights=[1, busy_schedule_ratio])[0]
        


        # Add the user with their availability, name, and email to the dictionary
        temp_name = random.choice(names)
        grand_dict[user_id] = {
            'name': temp_name,
            'email': temp_name + '@' + email,
            'availability': availability
            }
    
    return grand_dict


def user_details_and_common_times(users, matched_tuple_ids, matched_schedule):
    id1, id2 = matched_tuple_ids
    # Retrieve user details
    user1_details = users.get(id1, {'name', 'email'})
    user2_details = users.get(id2, {'name', 'email'})
    
    # Retrieve common availability times if they have been matched
    common_times = matched_schedule
    
    # Construct the desired JSON structure
    result = {
        id1: {
            'name': user1_details.get('name'),
            'email': user1_details.get('email')
        },
        id2: {
            'name': user2_details.get('name'),
            'email': user2_details.get('email')
        },
        'timeslot': common_times
    }
    
    # Return the JSON structure as a string
    return json.dumps(result, indent=4)


def main():
    # Generate test users and find the best matches
    test_users = generate_users(10, 1)
    best_matches, common_times_dict = find_best_matches(test_users)
    for match, overlap in best_matches.items():
        print(user_details_and_common_times(test_users, match,common_times_dict[match]))
    return
    """
    # Print the results, including specific overlapping times
    for match, overlap in best_matches.items():
        print(f"Match between User {match[0]} and User {match[1]}: Overlap Duration: {overlap} hours")
        for day, times in common_times_dict[match].items():
            print(f"  - Common times on {day}: {', '.join(times)}")

    users_without_matches = set(test_users.keys()) - set(user_id for match in best_matches for user_id in match)

    for notify in users_without_matches:
        print(f"Notify User {notify} that they do not have a match") 
    return
    """


    
  

main()