import numpy as np

bonus = .1
hours_spread = 100

college_data = open("/../static/CollegeAdmissionData.tsv")

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def sat_range_from_school(school):
    read_tsv = csv.reader(college_data, delimiter="\n")
    schools = []
    scores = []
    for row in read_tsv:
        value = row.split("\t")
        schools.push(value[0])
        scores.push(value[1].split("\r")[0])
    for i in range(len(schools)):
        if school == schools[i]:
            return sat_desipher(scores[i])

def sat_desipher(raw):
    value = raw
    if len(value) == 1:
        value = '0' + raw
    if len(value) == 2:
        value = '1' + value + '0'
    return int(value)

class chancer:
    def __init__(self, school, sat, gpa, ecs, awards):
        self.school = school
        self.sat = sat
        self.gpa = gpa
        self.ecs = ecs
        self.awards = awards

    def goat_status(self):
        #ec/award substring if statements
        #check for t20 names + research (check for name then research, not a combined string)
        return 0

    def rate_sat(self):
        school_range = sat_range_from_school(self.school)
        if self.sat >= 1600:
            return 0.0
        if self.sat < 1600:
            return 1 - self.sat / school_range
        return None

    def rate_gpa(self):
        if self.gpa >= 4.0:
            return 0.0
        if self.gpa < 4.0:
            return 1 - self.gpa/4
        return None

    def ecs_bonus(self):
        commitment_rating = 1 - gaussian(sum([ec[1] for ec in self.ecs]),0,hours_spread)
        leadership_rating = 0
        for ec in self.ecs:
            if "captain" in ec[0].lower():
                leadership_rating += 1
            if "led" in ec[0].lower():
                leadership_rating += 1
            if "president" in ec[0].lower():
                leadership_rating += 1
            if "research" in ec[0].lower():
                leadership_rating += 1
        #respected_program_rating = 0
        return min((commitment_rating + leadership_rating)/2,1.0)
        #commitment computation -- tell them to average over 4 years, so if you did an ec 52 weeks per year for 2 years, input 26 weeks per year for 4
        #good but not cracked summer programs
        #look for "led" keyword

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