from itertools import permutations
from poker.target import targets

def hand_probability(target):
    freq = _frequency(target)
    combos = _draw_combinations(target)

    return 1.0 * freq / combos


def win_probability(community, pocket, players_left):
    player_expected = _expected_score(community + pocket)
    other_expected = _expected_score(community)

    return player_expected**5 / \
            (player_expected**5 + other_expected**5 * (players_left - 1))


def _generate_hit_miss_patterns(target, area):
    hits_needed = target.area_distance(area)
    yet_to_draw = 7 - target.shots

    if hits_needed > yet_to_draw:
        return []

    hits_and_misses = ['hit'] * int(hits_needed) + \
            ['miss'] * int(yet_to_draw - hits_needed)

    patterns = list(set(
            p for p in permutations(hits_and_misses, yet_to_draw)
    ))

#     for i, pattern in enumerate(patterns):
#         # what is this doing?
#         patterns[i] = list(pattern)
#         pattern = list(reversed(pattern))
#         if pattern.count('hit') > 0:
#             for __ in range(pattern.index('hit')):
#                 patterns[i].pop()

    # sorting here seems to keep straight probabilities from going wonky
    return sorted(patterns)

def _pattern_frequency(target, area, pattern):
    target = target.copy()
    frequency = 1

    hits_left = target.area_distance(area)
    misses_left = 7 - target.needed - target.area_misses(area)
    cards_left_in_deck = 52 - target.shots
    
    for hit_or_miss in pattern:
        
        if hits_left <= 0:
            frequency *= cards_left_in_deck
        elif misses_left < 0 or target.destroyed:
            frequency = 0
        elif hit_or_miss == 'hit':
            frequency *= target.areas[area]
            hits_left -= 1
            # hits also affect the target area
            target = target.hit_area(area)
        else: # miss
            frequency *= cards_left_in_deck - target.areas[area]
            misses_left -= 1

        cards_left_in_deck -= 1

    return frequency

def _frequency(target):
    frequency = 0
#     hit_cache = {}
#  
#     for area in target.areas:
#   
#         # the cache here significantly reduces execution time
#         hit_key = target.area_hits(area)
#         if hit_key not in hit_cache:
#             area_frequency = 0
#             pattern_cache = {}
#   
#             # another cache here to minimize repetition
#             hit_miss_patterns = _generate_hit_miss_patterns(target, area)
#               
#             for pattern in hit_miss_patterns:
#                 pattern_key = len(pattern)
#                   
#                 if pattern_key not in pattern_cache:
#                     pattern_cache[pattern_key] = \
#                             _pattern_frequency(target, area, pattern)
#   
#                 area_frequency += pattern_cache[pattern_key]
#   
#             hit_cache[hit_key] = area_frequency
#   
#         frequency += hit_cache[hit_key]
#   
#     return frequency

    hit_cache = {}
 
    for area in target.areas:
        area_frequency = 0
        pattern_cache = {}
        
        # another cache here to minimize repetition
        hit_miss_patterns = _generate_hit_miss_patterns(target, area)
            
        for pattern in hit_miss_patterns:
            pattern_frequency = _pattern_frequency(target, area, pattern)
              
#             pattern_key = len(pattern)
            pattern_key = 0
            for i, hit_or_miss in enumerate(pattern):
                if hit_or_miss == "hit":
                    pattern_key = i + 1
            if pattern_key not in pattern_cache:
                pattern_cache[pattern_key] = pattern_frequency
            else:
                cache_value = pattern_cache[pattern_key]
                if cache_value != pattern_frequency:
                    pass
                    # raise Exception("cache error! " + str(cache_value) + " != " + str(pattern_frequency))
        
            area_frequency += pattern_cache[pattern_key]
  
        # the cache here significantly reduces execution time
        hit_key = target.area_hits(area)

        if hit_key not in hit_cache:
            hit_cache[hit_key] = area_frequency
        else:
            cache_value = hit_cache[hit_key]
            if cache_value != area_frequency:
                pass
                # raise Exception("cache error! " + str(cache_value) + " != " + str(area_frequency))
  
        frequency += hit_cache[hit_key]
  
    return frequency

#     for area in target.areas:
#         area_frequency = 0
#  
#         hit_miss_patterns = _generate_hit_miss_patterns(target, area)
#          
#         for pattern in hit_miss_patterns:
#             area_frequency += _pattern_frequency(target, area, pattern)
#  
#         frequency += area_frequency
#  
#     return frequency

def _draw_combinations(target):
    # returns the number of possible ways the remaining cards can be drawn
    cards_left_in_deck = 52 - target.shots
    combinations = 1

    while cards_left_in_deck > 45:
        combinations *= cards_left_in_deck
        cards_left_in_deck -= 1

    return combinations

def _expected_score(cards):
        expected_score = 0
        hand_points = 104
        for target in targets:
            target = target().hit_with_cards(*cards)
            if len(cards) > 0:
                expected_score += hand_probability(target) * (hand_points + 
                        max(cards).rank_from_zero())
            else:
                expected_score += hand_probability(target) * hand_points
            hand_points -= 13
        return expected_score