"""
This script computes the scores of a set of measures used to select a committee for a
journal special issue. 

It generates 2 selection criteria:

1. The aggregated score over a number of measures
    S = \sum_{m \in M} w*m

where M (measures) contains:
- field score: the aggregated field score, assuming IR, HCI, IIR are desired fields,
  and IR and IIR are slightly more important than HCI
- field diversity: score in range of 1, 2, 3, the higher the team is more diverse
- senority: score in [0, 1], whether the team has a senior person
- geo-diveristy: score in [0, 1], whether the team has geo diversity
- gender-diversity: score in [0, 1], whether the team has gender-diversity
- community_ext: integer, the higher the more extension to the community

2. A decomposed field score for human evaluation, e.g., 
    IR = x, IIR = y, HCI = z;
where x, y, z are the aggregated expertise

"""
import itertools as it

# Number of candidates
num_candidates = 3

# Let's consider 3 core fields, and presumably one of them is a bit more
# important than the others 
field_weights = {'IR': 2, 'IIR': 2, 'HCI': 1}

# Weights for the measures
measure_weights = {
    'field': 3,
    'field_diversity': 1,
    'seniority': 2,
    'gender_diversity': 1,
    'geo_diversity': 1,
    'community_extension': 3 
}


# The candidate profiles
profiles = {
'PH': {'field': ['HCI', 'IIR'], 
    'senior': 1,
    'geo': 'EU',
    'gender': 'm',
    'community_ext': 0},

'JG': {'field': ['HCI', 'IIR'], 
    'senior': 1,
    'geo': 'US',
    'gender': 'm',
    'community_ext': 0},

'JH': {'field': ['IR', 'IIR'], 
    'senior': 0,
    'geo': 'EU',
    'gender': 'f',
    'community_ext': 0},

'CE': {'field': ['IR', 'IIR'], 
    'senior': 0,
    'geo': 'EU',
    'gender': 'm',
    'community_ext': 1},

'KT': {'field': ['IR'], 
    'senior': 1,
    'geo': 'US',
    'gender': 'm',
    'community_ext': 1},
}

#Here we define the rules for scoring
def scoring(team):
    scores = {} 
    field_score = {}
    #Process field information
    fields = [f for sublist in [profiles[t]['field'] for t in team] for f in sublist]
    agg_field_scores = 0
    for k, g in it.groupby(sorted(fields)):
        g = list(g)
        # count number of expertise for each field
        field_score[k] = len(g)
        # add aggregated field score
        agg_field_scores += field_weights[k]*len(g) 
    # add aggregated field score
    scores['field'] = agg_field_scores
    # add field diversity score
    scores['field_diversity'] = len(set(fields))
    # add seniority check
    scores['seniority'] = int(sum([profiles[t]['senior'] for t in team])>0)
    # add gender diversity check
    scores['gender_diversity'] = int(len(set([profiles[t]['gender'] for t in team]))>1)
    # add geo-diversity check
    scores['geo_diversity'] = int(len(set([profiles[t]['geo'] for t in team]))>1)
    # add extension to community score
    scores['community_extension'] = sum([profiles[t]['community_ext'] for t in team])
    return scores, field_score 


def select_team():
    candidates = [p for p in profiles]
    teams = it.combinations(candidates, num_candidates)
    return teams

if __name__ == '__main__':
    teams = select_team()
    S = []
    for team in teams:
        scores, field_score = scoring(team)
        ws = [scores[s]*measure_weights[s] for s in scores]
        S.append((team, sum(ws), field_score, scores))
    S.sort(key=lambda x: x[1], reverse=True)
    # print result
    print 'Weights for each measure:'
    print '--------------------------'
    for w in measure_weights:
        print w, measure_weights[w]
    print

    print 'Weights for fields:'
    print '--------------------------'
    for f in field_weights:
        print f, field_weights[f]
    print

    print 'Teams ranked by total scores'
    for team, total, fs, ws in S:
        print team, total
        print '\t Field expertise distribution:', 
        for f in fs:
            print f, fs[f], 
        print
        print '\t Individual measure scoring:'
        for w in ws:
            print '\t   %s'%w, ws[w]
        print
    
