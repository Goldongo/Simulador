from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
from typing import List
import httpx

app = FastAPI()

class Player(BaseModel):
  name: str
  rating: int
  team: str
  position: str

class Team(BaseModel):
  name: str
  color: str
  players: List[Player]
  goalkeeper: List[Player] = []
  defenseLine: List[Player] = []
  backMidfieldLine: List[Player] = []
  midfieldLine: List[Player] = []
  frontMidfieldLine: List[Player] = []
  attackLine: List[Player] = []
  defending: int = 0
  control: int = 0
  attacking: int = 0

  def __init__(self, **data):
    super().__init__(**data)
    self.goalkeeper = [i for i in self.players if i.position == "GK"]
    self.defenseLine = [i for i in self.players if i.position in ["CB", "FB"]]
    self.backMidfieldLine = [i for i in self.players if i.position == "CDM"]
    self.midfieldLine = [i for i in self.players if i.position in ["CM", "WM"]]
    self.frontMidfieldLine = [i for i in self.players if i.position in ["CAM", "WAM"]]
    self.attackLine = [i for i in self.players if i.position in ["ST", "CF", "FW"]]

    self.defending = round((sum([i.rating for i in self.goalkeeper]) + sum([i.rating for i in self.defenseLine]) + sum([i.rating for i in self.backMidfieldLine])) / (len(self.defenseLine) + len(self.backMidfieldLine) + len(self.goalkeeper)))
    self.control = round((sum([i.rating for i in self.frontMidfieldLine if i.position == "CAM"]) + sum([i.rating for i in self.midfieldLine]) + sum([i.rating for i in self.backMidfieldLine])) / (len([i.rating for i in self.frontMidfieldLine if i.position == "CAM"]) + len(self.midfieldLine) + len(self.backMidfieldLine)))
    self.attacking = round((sum([i.rating for i in self.midfieldLine if i.position == "WM"]) + sum([i.rating for i in self.frontMidfieldLine]) + sum([i.rating for i in self.attackLine])) / (len([i.rating for i in self.midfieldLine if i.position == "WM"]) + len(self.frontMidfieldLine) + len(self.attackLine)))

@app.get("/teams/{team_name}")
async def get_team(team_name: str):
  url = f"localhost:8000/api/teams/{team_name}"  # Remplazar con el api
  
  async with httpx.AsyncClient() as client:
    response = await client.get(url)
  if response.status_code == 200:
    team_data = response.json()
    players = [Player(**player_data) for player_data in team_data['players']]
    return Team(name=team_data['name'], color=team_data['color'], players=players)
  else:
    raise HTTPException(status_code=response.status_code, detail="Team not found")

def noRepeat(array1, array2):
  set1 = set(array1)
  set2 = set(array2)
  return not set1.intersection(set2)

def game(team1: Team, team2: Team):
  BASE_ATTACKS_NUM = 8
  regularTime = 90
  score = [0, 0]
  team1Opportunities = random.sample(range(1, 100), team1.control // 10)
  team2Opportunities = random.sample(range(1, 100), team2.control // 10)
  while noRepeat(team1Opportunities, team2Opportunities):
    team1Opportunities = random.sample(range(1, 100), team1.control // 10)
    team2Opportunities = random.sample(range(1, 100), team2.control // 10)
  team1Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10)
  team2Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10)
  while noRepeat(team1Attacks, team2Attacks):
    team1Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10)
    team2Attacks = random.sample(range(1, 100), BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10)
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

@app.post("/game/{team1}/{team2}")
async def simulate_game(team1: Team, team2: Team):
  score = game(team1, team2)
  return {"result": f"{team1.name} {score[0]} - {score[1]} {team2.name}"}