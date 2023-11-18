from TimeTableMatcher import AvailabilityMatcher


base_user = [('8:00', '9:03'), ('09:00', '11:00'), ('13:00', '15:00')]
comparative_user = [('10:00', '12:00'), ('14:00', '16:00')]

matcher = AvailabilityMatcher(base_user)
matcher_2 = AvailabilityMatcher(comparative_user)

common_times = matcher.find_common_availabilities(matcher_2)

for start, end in common_times:
    print(f"Common availability: from {start} to {end}")