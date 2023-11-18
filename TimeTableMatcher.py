from datetime import datetime

class AvailabilityInstance:
    def __init__(self, availability_intervals):
        self.availability = self.consolidate_availabilities(availability_intervals)

    @staticmethod
    def consolidate_availabilities(availability_intervals):
        availability_intervals = sorted([(datetime.strptime(start, '%H:%M'), datetime.strptime(end, '%H:%M')) 
                                         for start, end in availability_intervals])
        consolidated_intervals = [availability_intervals[0]]

        for current_start, current_end in availability_intervals[1:]:
            prev_start, prev_end = consolidated_intervals[-1]

            if current_start <= prev_end:
                consolidated_intervals[-1] = (prev_start, max(prev_end, current_end))
            else:
                consolidated_intervals.append((current_start, current_end))

        return [(start.strftime('%H:%M'), end.strftime('%H:%M')) for start, end in consolidated_intervals]

    def find_common_availabilities(self, comparative_availability):
        i, j = 0, 0
        common_availabilities = []

        while i < len(self.availability) and j < len(comparative_availability.availability):
            start1, end1 = self.availability[i]
            start2, end2 = comparative_availability.availability[j]

            if start1 <= end2 and start2 <= end1:
                overlap_start = max(start1, start2)
                overlap_end = min(end1, end2)
                common_availabilities.append((overlap_start, overlap_end))

            if end1 < end2:
                i += 1
            else:
                j += 1

        return common_availabilities

