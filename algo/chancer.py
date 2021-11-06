bonus = .01

class chancer:
    def __init__(self, school, sat, gpa, ecs, awards):
        self.school = school
        self.sat = sat
        self.gpa = gpa
        self.ecs = ecs
        self.awards = awards

    def goat_status(self):
        #ec/award substring if statements
        return 0

    def rate_sat(self):
        #sat rating
        return 0

    def rate_gpa(self):
        return 0

    def ecs_bonus(self):
        return 0
        #commitment computation

    def awards_bonus(self):
        return 0
        #competitiveness bonus
        #substring search for things like nmsf--non goat awards

    def get_acceptance(self):
        return 0




class profile:
    def __init__(self, acceptance_rate, sat_rating, gpa_rating, ecs_sent, ecs_bonus, awards_sent, awards_bonus, goat_rating):
        self.acceptance_rate  = acceptance_rate
        self.sat_rating = sat_rating
        self.gpa_rating = gpa_rating
        self.ecs_sent = ecs_sent
        self.ecs_bonus = ecs_bonus
        self.awards_sent = awards_sent
        self.awards_bonus = awards_bonus
        self.goat_rating = goat_rating

    def chance(self):
        chance = max(self.acceptance_rate * (self.ecs_sent + self.awards_sent) - (self.sat_rating + self.gpa_rating) + bonus * (self.ecs_bonus + self.awards_bonus), self.goat_rating)
        return min(chance, 1.0)