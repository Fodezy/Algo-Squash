#!/usr/bin/env python3
import json
import mysql.connector
from datetime import datetime, timedelta
from itertools import combinations
import random
from JAMES_FIX import send_email
# from text import create_json_data, send_email

# Assuming 'main' and 'generate_times' are correctly defined in 'total_overlap_algo'

# Function to connect to the database and load data
def load_server():
    """Load data from the SquashNoFriends database."""
    try:
        db_connection = mysql.connector.connect(
            host="34.42.173.231",
            user="root",
            password="BIUouwbwi739372",
            database="SquashNoFriends"
        )
        cursor = db_connection.cursor()
        
        # Extract data using a helper function
        extracted_raw_data = extract_data_query(cursor)
        
        # Commit changes if any were made during data extraction
        db_connection.commit()
        return extracted_raw_data

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

    finally:
        # Ensure the database connection is closed
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("MySQL connection is closed.")

# Function to extract and process data from SQL cursor
def extract_data_query(cursor):
    """Extract and process user data from the SQL cursor."""
    cursor.execute("SELECT id, availability, email, name FROM submissions")
    result = cursor.fetchall()
    data = {}

    for row in result:
        user_id, availability, email, name = row
        
        # Process availability data if not None
        if availability is not None:
            try:
                availability_dict = json.loads(availability)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for user ID {user_id}")
                continue
        else:
            availability_dict = {}

        # Check if the email and name are not empty strings
        if (email and name) or (availability_dict != {} or availability_dict != "none"):
            data[user_id] = {
                'availability': availability_dict,
                'email': email,
                'name': name,
            }

    return data

# Function to generate time slots within a specified range
def generate_times(start_time_str, end_time_str, fmt='%I:%M %p'):
    """Generate time slots between two times."""
    times = []
    start_time = datetime.strptime(start_time_str, fmt)
    end_time = datetime.strptime(end_time_str, fmt)

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
        # Check if the day exists in both users' availability
        if day in user2['availability']:
            common_times = []
            daily_slots = 0
            for time in generate_times('8:00 AM', '8:00 PM'):
                # Check if the time slot is available for both users
                if user1['availability'][day].get(time, False) and user2['availability'][day].get(time, False):
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

    for (id1, user1), (id2, user2) in combinations(users.items(), 2):
        common_availabilities = find_common_availabilities(user1, user2)
        total_overlap = calculate_duration(common_availabilities)
        
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

        overlaps = {pair: time for pair, time in overlaps.items()
                    if pair[0] not in matched_indices and pair[1] not in matched_indices}

    return matches, common_times_dict

# Construct JSON with user details and common times
def user_details_and_common_times(users, matched_tuple_ids, matched_schedule):
    """Construct JSON with user details and common times."""
    id1, id2 = matched_tuple_ids
    excluded_key = 'availability'

# Using dictionary comprehension to exclude 'excluded_key'
    copied_dict = users.get(id1, {'name': '', 'email': ''})
    user1_details = {k: v for k, v in copied_dict.items() if k != excluded_key}

    copied_dict = users.get(id2, {'name': '', 'email': ''})
    user2_details = {k: v for k, v in copied_dict.items() if k != excluded_key}

    common_times = matched_schedule

    result = {
        'id1': user1_details,
        'id2': user2_details,
        'timeslot': common_times
    }

    # return json.dumps(result, indent=4)
    return result

# Main function to execute the matching process
def main():
    data = load_server()
    if data:
        best_matches, common_times_dict = find_best_matches(data)
        users_emailed = set()  # Track users who have been emailed
        for match, overlap in best_matches.items():
            # print(match, overlap)
            temp_data_reserve=(user_details_and_common_times(data, match, common_times_dict[match]))
            send_email(temp_data_reserve)
    return

main()
