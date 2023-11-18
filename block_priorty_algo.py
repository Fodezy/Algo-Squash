import networkx as nx
from datetime import datetime
from itertools import combinations

def time_to_minutes(time_str):
    """Convert a time string in 'HH:MM' format to minutes since midnight."""
    time_obj = datetime.strptime(time_str, '%H:%M')
    return time_obj.hour * 60 + time_obj.minute

def calculate_overlap(player1, player2):
    """Calculate the weighted overlap between two players' schedules."""
    overlap_score = 0

    for interval1 in player1:
        start1, end1 = map(time_to_minutes, interval1)
        for interval2 in player2:
            start2, end2 = map(time_to_minutes, interval2)
            # Find overlap
            overlap_start = max(start1, start2)
            overlap_end = min(end1, end2)
            if overlap_start < overlap_end:  # Check if there is an overlap
                # Square the duration of the overlap block to favor larger blocks
                overlap_duration = overlap_end - overlap_start
                overlap_score += overlap_duration ** 2

    return overlap_score

def build_graph(players):
    G = nx.Graph()
    for player1, player2 in combinations(players, 2):
        overlap_weight = calculate_overlap(players[player1], players[player2])
        G.add_edge(player1, player2, weight=overlap_weight)
    return G

def pair_players(players):
    G = build_graph(players)
    pairs = nx.max_weight_matching(G, maxcardinality=True)
    return pairs

# Example usage
players = {
    'person1': [('09:00', '11:00'), ('14:00', '16:00'), ('19:00', '21:00')],
    'person2': [('10:00', '12:00'), ('15:00', '17:00')],
    'person3': [('11:00', '13:00'), ('16:00', '18:00')],
    'person4': [('10:00', '14:00'), ('17:00', '19:00')],
    'person5': [('13:00', '15:00'), ('18:00', '22:00')],
    'person6': [('14:00', '16:00'), ('17:00', '21:00')],
    'person7': [('15:00', '17:00'), ('20:00', '22:00')],
}
paired_players = pair_players(players)

print (paired_players)


