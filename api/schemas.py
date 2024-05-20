from pydantic import BaseModel
from typing import List
import requests
from fastapi import HTTPException

class Player(BaseModel):
  id_: int
  name: str
  overall: int
  position: str

class Team(BaseModel):
  name: str
  players: List[Player]

  @property
  def lines(self):
    return {
      "GK": [p for p in self.players if p.position == "GK"],
      "DF": [p for p in self.players if p.position in ["CB", "FB"]],
      "CDM": [p for p in self.players if p.position == "CDM"],
      "CM": [p for p in self.players if p.position in ["CM", "WM"]],
      "CAM": [p for p in self.players if p.position in ["CAM", "WAM"]],
      "AT": [p for p in self.players if p.position in ["ST", "CF", "FW"]]
    }

  def calculate_average(self, positions):
    total_overall = sum(player.overall for pos in positions for player in self.lines[pos])
    total_players = sum(len(self.lines[pos]) for pos in positions)
    return round(total_overall / total_players) if total_players else 0

  @property
  def defending(self):
    return self.calculate_average(["GK", "DF", "CDM"])

  @property
  def control(self):
    return self.calculate_average(["CAM", "CM", "CDM"])

  @property
  def attacking(self):
    return self.calculate_average(["CM", "CAM", "AT"])

class TeamID(BaseModel):
  name: str
  players: List[int] 

def setUpTeam(team_id: TeamID):
  try:
    response = requests.get("http://127.0.0.1:8000/players/")
    response.raise_for_status()
    all_players = response.json()
    
    team_players = [Player(**player) for player in all_players if player["id_"] in team_id.players]
    
    return Team(name=team_id.name, players=team_players)
  except requests.RequestException as e:
    raise HTTPException(status_code=500, detail=str(e))
