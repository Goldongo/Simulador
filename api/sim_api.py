from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import requests

app = FastAPI()

class Player(BaseModel):
  name: str
  rating: int
  team: str
  position: str

class Team(BaseModel):
  name: str
  color: str
  players: list[Player]
  goalkeeper: list[Player]
  defenseLine: list[Player]
  backMidfieldLine: list[Player]
  midfieldLine: list[Player]
  frontMidfieldLine: list[Player]
  attackLine: list[Player]
  defending: int
  control: int
  attacking: int

  def __init__(self, name: str, color: str, players: list[Player]):
    super().__init__(name=name, color=color, players=players)
    self.goalkeeper = [i for i in self.players if i.position == "GK"]
    self.defenseLine = [i for i in self.players if i.position in ["CB"," FB"]]
    self.backMidfieldLine = [i for i in self.players if i.position == "CDM"]
    self.midfieldLine = [i for i in self.players if i.position in ["CM", "WM"]]
    self.frontMidfieldLine = [i for i in self.players if i.position in ["CAM","WAM"]]
    self.attackLine = [i for i in self.players if i.position in ["ST", "CF", "FW"]]

    self.defending = round((sum([i.overall for i in self.goalkeeper]) + sum([i.overall for i in self.defenseLine]) + sum([i.overall for i in self.backMidfieldLine])) / (len(self.defenseLine) + len(self.backMidfieldLine) + len(self.goalkeeper)))
    self.control = round((sum([i.overall for i in self.frontMidfieldLine if i.position == "CAM"]) + sum([i.overall for i in self.midfieldLine]) + sum([i.overall for i in self.backMidfieldLine])) / (len([i.overall for i in self.frontMidfieldLine if i.position == "CAM"]) + len(self.midfieldLine) + len(self.backMidfieldLine)))
    self.attacking = round((sum([i.overall for i in self.midfieldLine if i.position == "WM"]) + sum([i.overall for i in self.frontMidfieldLine]) + sum([i.overall for i in self.attackLine])) / (len([i.overall for i in self.midfieldLine if i.position == "WM"]) + len(self.frontMidfieldLine) + len(self.attackLine)))

@app.get("/teams/{team_name}")
def get_team(team_name: str):
  url = f"localhost:8000/teams/{team_name}"
  response = requests.get(url)
  if response.status_code == 200:
    team_data = response.json()
    players = [Player(**player_data) for player_data in team_data['players']]
    return Team(name=team_data['name'], color=team_data['color'], players=players)
  else:
    raise HTTPException(status_code=response.status_code, detail="Team not found")

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
  team1Opportunities = random.sample(range(1, 100), team1.control // 10)
  team2Opportunities = random.sample(range(1, 100), team2.control // 10)
  opprotunitiesFlag = noRepeat(team1Opportunities, team2Opportunities)
  while not opprotunitiesFlag:
    team1Opportunities = random.sample(range(1, 100), team1.control // 10)
    team2Opportunities = random.sample(range(1, 100), team2.control // 10)
    opprotunitiesFlag = noRepeat(team1Opportunities, team2Opportunities)
  team1Attacks = random.sample(range(1, 100), (BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10))
  team2Attacks = random.sample(range(1, 100), (BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10))
  attacksFlag = noRepeat(team1Attacks, team2Attacks)
  while not attacksFlag:
    team1Attacks = random.sample(range(1, 100), (BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10))
    team2Attacks = random.sample(range(1, 100), (BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10))
    attacksFlag = noRepeat(team1Attacks, team2Attacks)
  time = 0
  while time < regularTime:
    randNum = random.randint(1, 100)
    if randNum in team1Opportunities:
      randNum = random.randint(1, 100)
      if randNum in team1Attacks:
        score[0] += 1
    if randNum in team2Opportunities:
      randNum = random.randint(1, 100)
      if randNum in team2Attacks:
        score[1] += 1
    time += 1
  return score

@app.post("/game")
def simualte_game(team1: Team, team2: Team):
  score = game(team1, team2)
  return {"result": f"{team1.name} {score[0]} - {score[1]} {team2.name}"}