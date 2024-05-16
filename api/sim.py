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
    self.goalkeeper = [i for i in self.players if i.position == "GK"]
    self.defenseLine = [i for i in self.players if i.position in ["CB"," FB"]]
    self.backMidfieldLine = [i for i in self.players if i.position == "CDM"]
    self.midfieldLine = [i for i in self.players if i.position in ["CM", "WM"]]
    self.frontMidfieldLine = [i for i in self.players if i.position in ["CAM","WAM"]]
    self.attackLine = [i for i in self.players if i.position in ["ST", "CF", "FW"]]

    self.defending = round((sum([i.overall for i in self.goalkeeper]) + sum([i.overall for i in self.defenseLine]) + sum([i.overall for i in self.backMidfieldLine])) / (len(self.defenseLine) + len(self.backMidfieldLine) + len(self.goalkeeper)))
    self.control = round((sum([i.overall for i in self.frontMidfieldLine if i.position == "CAM"]) + sum([i.overall for i in self.midfieldLine]) + sum([i.overall for i in self.backMidfieldLine])) / (len([i.overall for i in self.frontMidfieldLine if i.position == "CAM"]) + len(self.midfieldLine) + len(self.backMidfieldLine)))
    self.attacking = round((sum([i.overall for i in self.midfieldLine if i.position == "WM"]) + sum([i.overall for i in self.frontMidfieldLine]) + sum([i.overall for i in self.attackLine])) / (len([i.overall for i in self.midfieldLine if i.position == "WM"]) + len(self.frontMidfieldLine) + len(self.attackLine)))

  def __str__(self):
    return f"Name: {self.name}, Players: [{', '.join([str(j) for j in self.players])}]"


def noRepeat(array1, array2):
  set1 = set(array1)
  set2 = set(array2)
  
  if set1.intersection(set2):
    return True
  else:
    return False

def game(team1, team2):
  BASE_ATTACKS_NUM = 8
  regularTime = 90
  
  score = [0, 0]
  
  team1Opportunities = random.sample(range(1, 100), team1.control//10)
  team2Opportunities = random.sample(range(1, 100), team2.control//10)
  
  opprotunitiesFlag = noRepeat(team1Opportunities, team2Opportunities)
  
  while not opprotunitiesFlag:
    team1Opportunities = random.sample(range(1, 100), team1.control//10)
    team2Opportunities = random.sample(range(1, 100), team2.control//10)
    opprotunitiesFlag = noRepeat(team1Opportunities, team2Opportunities)
  
  team1Attacks = random.sample(range(1,100), (BASE_ATTACKS_NUM + (team1.attacking - team2.defending)//10))
  team2Attacks = random.sample(range(1,100), (BASE_ATTACKS_NUM + (team2.attacking - team1.defending)//10))
  
  attacksFlag = noRepeat(team1Attacks, team2Attacks)
  
  while not attacksFlag:
    team1Attacks = random.sample(range(1,100), (BASE_ATTACKS_NUM + (team1.attacking - team2.defending)//10))
    team2Attacks = random.sample(range(1,100), (BASE_ATTACKS_NUM + (team2.attacking - team1.defending)//10))
    attacksFlag = noRepeat(team1Attacks, team2Attacks)
  
  time = 0
  
  while time < regularTime:
    randNum = random.randint(1, 100)
    if randNum in team1Opportunities:
      randNum = random.randint(1, 100)
      if randNum in team1Attacks:
        score[0] += 1
        print(f"GOOOOOL del {team1.name}!!!")

    if randNum in team2Opportunities:
      randNum = random.randint(1, 100)
      if randNum in team2Attacks:
        score[1] += 1
        print(f"GOOOOOL del {team2.name}!!!")

    time += 1
  print()
  print(f"Final: {team1.name} {score[0]} - {score[1]} {team2.name}")

