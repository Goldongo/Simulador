from pydantic import BaseModel
from typing import List
import requests
from requests.exceptions import RequestException

class Player(BaseModel):
  id_ : int
  name: str
  overall: int
  position: str

class Team(BaseModel):
  name: str
  players: List[int]

  def __init__(self, **data):
    super().__init__(**data)
    self.lines = {
      "GK": [p for p in self.players if p.position == "GK"],
      "DF": [p for p in self.players if p.position in ["CB", "FB"]],
      "CDM": [p for p in self.players if p.position == "CDM"],
      "CM": [p for p in self.players if p.position in ["CM", "WM"]],
      "CAM": [p for p in self.players if p.position in ["CAM", "WAM"]],
      "AT": [p for p in self.players if p.position in ["ST", "CF", "FW"]]
    }
    self.defending = self.calculate_average(["GK", "DF", "CDM"])
    self.control = self.calculate_average(["CAM", "CM", "CDM"])
    self.attacking = self.calculate_average(["CM", "CAM", "AT"])

  def calculate_average(self, positions):
    total_overall = sum(
      [player.overall for pos in positions for player in self.lines[pos]])
    total_players = sum([len(self.lines[pos]) for pos in positions])
    return round(total_overall / total_players) if total_players else 0
  
def setUpTeam(team_json):
  name = team_json["name"]
  playersIdList = team_json["players"]
  response = requests.get("http://127.0.0.1:8000/players/") # Cambiar a la dirección de la Base de Datos de jugadores
  if response.status_code != 200:
    raise RequestException("Error fetching players")
  players = response.json()
  team = Team(name=name, players=[])
  for player in players:
    if player["id"] in playersIdList:
      team.players.append(Player(**player))
  return team
