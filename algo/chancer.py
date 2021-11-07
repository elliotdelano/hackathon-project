import numpy as np
import csv
bonus = .1
hours_spread = 100

college_data = "static/CollegeAdmissionData.tsv"

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def sat_desipher(raw):
    value = raw
    if len(value) == 1:
        value = '0' + raw
    if len(value) == 2:
        value = '1' + value + '0'
    return int(value)

def sat_range_from_school(school):
    coll = open(college_data,'r')
    clines =  coll.readlines()
    coll.close()
    print(clines)
    schools = [c.split('\t')[0] for c in clines]
    scores = [c.split('\t')[1] for c in clines]
    for i in range(len(schools)):
        if school == schools[i]:
            print(sat_desipher(scores[i]))
            return sat_desipher(scores[i])

class chancer:
    def __init__(self, school, sat, gpa, ecs):
        self.school = school
        self.sat = sat
        self.gpa = gpa
        self.ecs = ecs

    def goat_status(self):
        goat_rating = 0.0
        for ec in self.ecs:
            print(ec[0])
            if ec[0].lower() in "IMO medalist".lower():
                goat_rating = 1.0
            if ec[0].lower() in "IChO medalist".lower():
                goat_rating = 1.0
            if ec[0].lower() in "IOI medalist".lower():
                goat_rating = 1.0
            if ec[0].lower() in "IOL medalist".lower():
                goat_rating = 1.0
            if ec[0].lower() in "IBO medalist".lower():
                goat_rating = 1.0
            if ec[0].lower() in "IPhO medalist".lower():
                goat_rating = 1.0
            if ec[0].lower() in "National Champion".lower():
                goat_rating = 1.0
            if ec[0].lower() in "State Champion".lower():
                goat_rating = 1.0
            if ec[0].lower() in "Research Science Institute".lower():
                goat_rating = 1.0
            if ec[0].lower() in "MOSTEC".lower():
                goat_rating = 1.0
            if ec[0].lower() in "MITES".lower():
                goat_rating = 1.0
            if ec[0].lower() in "ISEF".lower():
                goat_rating = 1.0
            if ec[0].lower() in "Telluride Association Summer Program (TASP)".lower():
                goat_rating = 1.0
            if ec[0].lower() in "Program in Mathematics for Young Students (PROMYS)".lower():
                goat_rating = 1.0
            if ec[0].lower() in "Questbridge Prep Scholar".lower():
                goat_rating = 1.0
            if ec[0].lower() in "Johns Hopkins Center for Talented Youth".lower():
                goat_rating = 1.0
            if ec[0].lower() in "fly-in program".lower():
                goat_rating = 1.0
        return goat_rating

    def rate_sat(self):

        school_range = sat_range_from_school(self.school)
        if int(self.sat) >= 1600:
            return 0.0
        if int(self.sat) < 1600:
            return 1 - int(self.sat) / school_range

        return 0

    def rate_gpa(self):
        if float(self.gpa) >= 4.0:
            return 0.0
        if float(self.gpa) < 4.0:
            return 1 - float(self.gpa)/4
        return 0.0

    def ecs_bonus(self):
        commitment_rating = 1 - gaussian(sum([int(ec[1]) for ec in self.ecs]),0,hours_spread)
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
            if ec[0].lower() in "founder".lower():
                leadership_rating += 1
            if ec[0].lower() in "Research".lower():
                leadership_rating += 1
            if ec[0].lower() in "national merit".lower():
                leadership_rating += 1
        return min((commitment_rating + leadership_rating)/2,1.0)

    def get_acceptance(self):
        coll = open(college_data, 'r')
        clines = coll.readlines()
        coll.close()
        schools = [c.split('\t')[0] for c in clines]
        acc = [c.split('\t')[2] for c in clines]
        return float(acc[schools.index(self.school)])/100

class profile:
    def __init__(self, acceptance_rate, sat_rating, gpa_rating, ecs_sent, ecs_bonus, goat_rating):
        self.acceptance_rate  = acceptance_rate
        self.sat_rating = sat_rating
        self.gpa_rating = gpa_rating
        self.ecs_sent = ecs_sent
        self.ecs_bonus = ecs_bonus
        self.goat_rating = goat_rating

    def chance(self):
        chance = max(self.acceptance_rate * (self.ecs_sent) - (self.sat_rating + self.gpa_rating) + bonus * (self.ecs_bonus), self.goat_rating)
        return min(chance, .9)