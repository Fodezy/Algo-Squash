from TimeTableMatcher import AvailabilityInstance
import random
from itertools import combinations
from datetime import datetime

#base_user = [('8:00', '9:03'), ('09:00', '11:00'), ('13:00', '15:00')]
#comparative_user = [('10:00', '12:00'), ('14:00', '16:00'), ('18:00', '20:00')]


def calculate_duration(overlap):
    start, end = overlap
    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')
    duration_temp = ((end_time - start_time).total_seconds() / 3600) # converting seconds to hours 
    if (1>duration_temp): #if duration)temp is less than an hour, return 0
        return 0
    else:
        return duration_temp
        

# Updated Function to find the best 1-1 match based on common availability
def find_best_matches(matchers):
    overlaps = {}

    for (i, matcher1), (j, matcher2) in combinations(enumerate(matchers), 2):
        common_availabilities = matcher1.find_common_availabilities(matcher2)
        total_overlap = sum([calculate_duration(overlap) for overlap in common_availabilities])
        overlaps[(i, j)] = total_overlap

    matches = {}
    matched_indices = set()

    # Iterate until all possible matches are made
    while overlaps:
        # Find the best match based on maximum overlap
        best_match = max(overlaps, key=overlaps.get)
        matched_indices.update(best_match)
        matches[best_match] = overlaps[best_match]

        # Remove matched users and their related pairs
        overlaps = {pair: time for pair, time in overlaps.items() if pair[0] not in matched_indices and pair[1] not in matched_indices}

    return matches


case1_user_matcher = AvailabilityInstance([('00:00', '23:59')])
case2_user_matcher = AvailabilityInstance([('08:00', '12:00')])
case3_user_matcher = AvailabilityInstance([('12:00', '18:00')])
case4_user_matcher = AvailabilityInstance([('18:00', '23:59')])
case5_user_matcher = AvailabilityInstance([('09:00', '11:00'), ('14:00', '16:00'), ('19:00', '21:00')])
case6_user_matcher = AvailabilityInstance([('08:00', '10:00'), ('13:00', '16:00')])
case7_user_matcher = AvailabilityInstance([('12:00', '15:00'), ('18:00', '22:00')])
case8_user_matcher = AvailabilityInstance([('09:30', '11:45'), ('14:15', '16:30'), ('19:00', '21:30')])
case9_user_matcher = AvailabilityInstance([('08:00', '10:30'), ('18:00', '21:00')])
case10_user_matcher = AvailabilityInstance([('11:30', '13:30'), ('15:30', '17:30')])
case11_user_matcher = AvailabilityInstance([('08:00', '09:00'), ('22:00', '23:59')])
case12_user_matcher = AvailabilityInstance([('08:00', '10:00'), ('21:00', '23:59')])
case13_user_matcher = AvailabilityInstance([('08:30', '10:00'), ('19:30', '22:00')])
case14_user_matcher = AvailabilityInstance([('08:00', '09:30'), ('21:30', '23:59')])
case15_user_matcher = AvailabilityInstance([('08:00', '10:00'), ('20:00', '23:59')])
case16_user_matcher = AvailabilityInstance([('08:00', '09:30'), ('22:30', '23:59')])
case17_user_matcher = AvailabilityInstance([('08:00', '10:00'), ('23:00', '23:59')])
case18_user_matcher = AvailabilityInstance([('08:00', '12:00'), ('18:00', '23:59')])
case19_user_matcher = AvailabilityInstance([('13:00', '15:00'), ('20:00', '23:59')])
case20_user_matcher = AvailabilityInstance([('08:00', '09:30'), ('21:30', '23:59')])

# Now, you can add these instances to a list to be used in your matching algorithm
matchers = [case1_user_matcher, case2_user_matcher, case3_user_matcher]
""", case4_user_matcher, 
            case5_user_matcher, case6_user_matcher, case7_user_matcher, case8_user_matcher, 
            case9_user_matcher, case10_user_matcher, case11_user_matcher, case12_user_matcher, 
            case13_user_matcher, case14_user_matcher, case15_user_matcher, case16_user_matcher, 
            case17_user_matcher, case18_user_matcher, case19_user_matcher, case20_user_matcher]
            """
best_matches = find_best_matches(matchers)

for match, overlap in best_matches.items():
    user1_index, user2_index = match
    user1_availability = matchers[user1_index]
    user2_availability = matchers[user2_index]

    print(f"Match between User {user1_index + 1} and User {user2_index + 1}:")
    print(f"Overlap Duration: {overlap} hours")

    # Print the common availabilities
    common_times = user1_availability.find_common_availabilities(user2_availability)
    for start, end in common_times:
        print(f"Common availability: from {start} to {end}")

    print("\n")  # Add a newline for better readability


"""
matcher = AvailabilityInstance(base_user)
matcher_2 = AvailabilityInstance(comparative_user)

common_times = matcher.find_common_availabilities(matcher_2)


for start, end in common_times:
    print(f"Common availability: from {start} to {end}")
"""