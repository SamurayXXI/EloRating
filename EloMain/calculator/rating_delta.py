def calc_rating_delta(own_rating, rival_rating, own_score, rival_score, index):
    goals_delta = own_score - rival_score
    rating_delta = own_rating - rival_rating
    return round(index*calc_G(goals_delta)*(calc_W(goals_delta) - calc_We(rating_delta)),0)

def calc_G(goals_delta):
    goals_delta = abs(goals_delta)

    if goals_delta<2:
        return 1.0

    if goals_delta==2:
        return 1.5

    return (11+goals_delta)/8

def calc_We(rating_delta):
    power = -rating_delta/400
    return 1/(10**power + 1)

def calc_W(goals_delta):
    if goals_delta<0:
        return 0
    if goals_delta==0:
        return 0.5
    if goals_delta>0:
        return 1