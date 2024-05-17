import random

class Player:
    def __init__(self, name, overall, team, position):
        self.name = name
        self.overall = overall
        self.team = team
        self.position = position

    def __str__(self):
        return f"Name: {self.name}, Overall: {self.overall}"

class Team:
    def __init__(self, name, color, players):
        self.name = name
        self.color = color
        self.players = players
        self.lines = {
            "GK": [p for p in players if p.position == "GK"],
            "DF": [p for p in players if p.position in ["CB", "FB"]],
            "CDM": [p for p in players if p.position == "CDM"],
            "CM": [p for p in players if p.position in ["CM", "WM"]],
            "CAM": [p for p in players if p.position in ["CAM", "WAM"]],
            "AT": [p for p in players if p.position in ["ST", "CF", "FW"]]
        }
        self.defending = self.calculate_average(["GK", "DF", "CDM"])
        self.control = self.calculate_average(["CAM", "CM", "CDM"])
        self.attacking = self.calculate_average(["CM", "CAM", "AT"])

    def calculate_average(self, positions):
        total_overall = sum([player.overall for pos in positions for player in self.lines[pos]])
        total_players = sum([len(self.lines[pos]) for pos in positions])
        return round(total_overall / total_players) if total_players else 0

    def __str__(self):
        return f"Name: {self.name}, Players: [{', '.join([str(p) for p in self.players])}]"

def no_repeat(array1, array2):
    return not set(array1).intersection(set(array2))

GOALKEEPER_WEIGHT = 0.1
DEFENSELINE_WEIGHT = 1.5
BACKMIDFIELDLINE_WEIGHT = 2
MIDFIELDLINE_WEIGHT = 3
FRONTMIDFIELDLINE_WEIGHT = 4
ATTACKLINE_WEIGHT = 6

WEIGHTS = {
    "GK": GOALKEEPER_WEIGHT,
    "DF": DEFENSELINE_WEIGHT,
    "CDM": BACKMIDFIELDLINE_WEIGHT,
    "CM": MIDFIELDLINE_WEIGHT,
    "CAM": FRONTMIDFIELDLINE_WEIGHT,
    "AT": ATTACKLINE_WEIGHT
}

def check_lines(team):
    lines = [line for line in team.lines if team.lines[line]]
    weights = [WEIGHTS[line] for line in lines]
    return lines, weights

def game(team1, team2):
    BASE_ATTACKS_NUM = 8
    regularTime = 90
    
    score = [0, 0]
    
    team1Opportunities = random.sample(range(1, 100), team1.control // 10)
    team2Opportunities = random.sample(range(1, 100), team2.control // 10)
    
    while no_repeat(team1Opportunities, team2Opportunities):
        team1Opportunities = random.sample(range(1, 100), team1.control // 10)
        team2Opportunities = random.sample(range(1, 100), team2.control // 10)
    
    team1Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10)
    team2Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10)
    
    while no_repeat(team1Attacks, team2Attacks):
        team1Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10)
        team2Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10)
    
    time = 0
    
    team1Lines, team1Weights = check_lines(team1)
    team2Lines, team2Weights = check_lines(team2)
    
    while time < regularTime:
        randNum = random.randint(1, 100)
        if randNum in team1Opportunities:
            randNum = random.randint(1, 100)
            if randNum in team1Attacks:
                score[0] += 1
                print(f"GOOOOOL del {team1.name}!!!")
                goalscorerLine = random.choices(team1Lines, team1Weights)[0]
                goalscorer = random.choice(team1.lines[goalscorerLine])
                print(f"  {goalscorer.name}, {time}")

        if randNum in team2Opportunities:
            randNum = random.randint(1, 100)
            if randNum in team2Attacks:
                score[1] += 1
                print(f"GOOOOOL del {team2.name}!!!")
                goalscorerLine = random.choices(team2Lines, team2Weights)[0]
                goalscorer = random.choice(team2.lines[goalscorerLine])
                print(f"  {goalscorer.name}, {time}")
                
        time += 1

    print()
    print(f"Final: {team1.name} {score[0]} - {score[1]} {team2.name}")
