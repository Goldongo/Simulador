from fastapi import FastAPI, HTTPException
import requests
from requests.exceptions import RequestException
import random

app = FastAPI()


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
    total_overall = sum(
      [player.overall for pos in positions for player in self.lines[pos]])
    total_players = sum([len(self.lines[pos]) for pos in positions])
    return round(total_overall / total_players) if total_players else 0

  def __str__(self):
    return f"Name: {self.name}, Players: [{', '.join([str(p) for p in self.players])}]"


def no_repeat(array1, array2):
  return not set(array1).intersection(set(array2))


ATT_WEIGHTS = {
  "GK": 0.1,
  "DF": 1.5,
  "CDM": 2,
  "CM": 3,
  "CAM": 4,
  "AT": 6
}

DEF_WEIGHTS = {
  "GK": 10,
  "DF": 12,
  "CDM": 6,
  "CM": 4,
  "CAM": 2,
  "AT": 1
}

CRE_WEIGHTS = {
  "GK": 0.5,
  "DF": 2,
  "CDM": 8,
  "CM": 10,
  "CAM": 14,
  "AT": 9
}


def check_lines(team, situation):
  weights_map = {
    "attacking": ATT_WEIGHTS,
    "defensive": DEF_WEIGHTS,
    "creative": CRE_WEIGHTS
  }
  lines = [line for line in team.lines if team.lines[line]]
  weights = [weights_map[situation][line] for line in lines]
  return lines, weights


def getTeam(team_id):
  try:
    response = requests.get(f"http://127.0.0.1:8000/team/{team_id}") # Cambiar a la dirección de la API de equipos
    response.raise_for_status()
    data = response.json()
    players = [Player(**player) for player in data['players']]
    return Team(name=data['name'], color=data['color'], players=players)
  except RequestException as e:
    print(f"Error fetching team data: {e}")
    return None


@app.get("/game/{team1ID}/{team2ID}")
def game(team1ID: int, team2ID: int):
  team1 = getTeam(team1ID)
  team2 = getTeam(team2ID)

  if not team1 or not team2:
    raise HTTPException(
      status_code=404, detail="One or both teams not found")

  output = {
    "events": [],
    "team1_events": [],
    "team2_events": [],
    "final_score": {}
  }

  BASE_ATTACKS_NUM = 8
  regularTime = 90

  score = [0, 0]

  team1Opportunities = random.sample(range(1, 100), team1.control // 10)
  team2Opportunities = random.sample(range(1, 100), team2.control // 10)

  while no_repeat(team1Opportunities, team2Opportunities):
    team1Opportunities = random.sample(range(1, 100), team1.control // 10)
    team2Opportunities = random.sample(range(1, 100), team2.control // 10)

  team1Attacks = random.sample(
    range(1, 100), BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10)
  team2Attacks = random.sample(
    range(1, 100), BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10)

  while no_repeat(team1Attacks, team2Attacks):
    team1Attacks = random.sample(
      range(1, 100), BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10)
    team2Attacks = random.sample(
      range(1, 100), BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10)

  time = 0

  atTeam1Lines, atTeam1Weights = check_lines(team1, "attacking")
  atTeam2Lines, atTeam2Weights = check_lines(team2, "attacking")
  crTeam1Lines, crTeam1Weights = check_lines(team1, "creative")
  crTeam2Lines, crTeam2Weights = check_lines(team2, "creative")
  deTeam1Lines, deTeam1Weights = check_lines(team1, "defensive")
  deTeam2Lines, deTeam2Weights = check_lines(team2, "defensive")

  while time < regularTime:
    randNum = random.randint(1, 100)
    if randNum in team1Opportunities:
      event = f"Minuto {time}: {team1.name} tiene la posesión"
      output["events"].append(event)
      AssistantLine = random.choices(crTeam1Lines, crTeam1Weights)[0]
      Assistant = random.choice(team1.lines[AssistantLine])
      possibilities = [
        f"Que pase de {Assistant.name}!!!", f"Centro de {Assistant.name}!!!"]
      event = random.choice(possibilities)
      output["events"].append(event)
      randNum = random.randint(1, 100)
      if randNum in team1Attacks:
        score[0] += 1
        goalscorerLine = random.choices(
            atTeam1Lines, atTeam1Weights)[0]
        goalscorer = random.choice(team1.lines[goalscorerLine])
        while goalscorer.name == Assistant.name:
            goalscorer = random.choice(team1.lines[goalscorerLine])
        event = f"GOOOOOL del {team1.name}!!! {goalscorer.name} a los {time} minutos"
        output["events"].append(event)
        output["team1_events"].append(f"{goalscorer.name}, {time}")
        output["team1_events"].append(f"Asist. {Assistant.name}")
      else:
        BlockLine = random.choices(deTeam2Lines, deTeam2Weights)[0]
        Block = random.choice(team2.lines[BlockLine])
        if Block.position == "GK":
          event = f"Gran atajada de {Block.name}!!!"
        else:
          possibilities = [f"Gran corte de {Block.name}!!!", f"Intercepción de {Block.name}!!!",
                            f"Despeje de {Block.name}!!!", f"Bloqueo de {Block.name}!!!", f"Recuperación de {Block.name}!!!"]
          event = random.choice(possibilities)
        output["events"].append(event)

    if randNum in team2Opportunities:
      event = f"Minuto {time}: {team2.name} tiene la posesión"
      output["events"].append(event)
      AssistantLine = random.choices(crTeam2Lines, crTeam2Weights)[0]
      Assistant = random.choice(team2.lines[AssistantLine])
      possibilities = [
        f"Que pase de {Assistant.name}!!!", f"Centro de {Assistant.name}!!!"]
      event = random.choice(possibilities)
      output["events"].append(event)
      randNum = random.randint(1, 100)
      if randNum in team2Attacks:
        score[1] += 1
        goalscorerLine = random.choices(
            atTeam2Lines, atTeam2Weights)[0]
        goalscorer = random.choice(team2.lines[goalscorerLine])
        while goalscorer.name == Assistant.name:
            goalscorer = random.choice(team1.lines[goalscorerLine])
        event = f"GOOOOOL del {team2.name}!!! {goalscorer.name} a los {time} minutos"
        output["events"].append(event)
        output["team2_events"].append(f"{goalscorer.name}, {time}")
        output["team2_events"].append(f"Asist. {Assistant.name}")
      else:
        BlockLine = random.choices(deTeam1Lines, deTeam1Weights)[0]
        Block = random.choice(team1.lines[BlockLine])
        if Block.position == "GK":
          event = f"Gran atajada de {Block.name}!!!"
        else:
          possibilities = [f"Gran corte de {Block.name}!!!", f"Intercepción de {Block.name}!!!",
                            f"Despeje de {Block.name}!!!", f"Bloqueo de {Block.name}!!!", f"Recuperación de {Block.name}!!!"]
          event = random.choice(possibilities)
        output["events"].append(event)

    time += 1

  output["final_score"] = {team1.name: score[0], team2.name: score[1]}
  return output
