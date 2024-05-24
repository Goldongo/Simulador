from fastapi import FastAPI, HTTPException, Body
import random
from fastapi.middleware.cors import CORSMiddleware
from .schemas import Team, setUpTeam, TeamID

app = FastAPI()

origins = [
    "http://lb-prod-2030613354.us-east-1.elb.amazonaws.com",
    "http://lb-prod-2030613354.us-east-1.elb.amazonaws.com:8000",
    "http://lb-prod-2030613354.us-east-1.elb.amazonaws.com:8080",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def generate_opportunities(control, cap, total_range):
  opportunities = random.sample(range(1, total_range + 1), min(control // 10, cap))
  return opportunities

@app.post("/game")
def game(team1_json: TeamID = Body(...), team2_json: TeamID = Body(...)):
  if not team1_json or not team2_json:
    raise HTTPException(status_code=404, detail="NOT FOUND")

  team1 = setUpTeam(team1_json)
  team2 = setUpTeam(team2_json)

  output = {
    "timeline": {},
    "team1_events": [],
    "team2_events": [],
    "final_score": {}
  }

  BASE_ATTACKS_NUM = 8
  regularTime = 90

  score = [0, 0]

  opportunities_cap = 50  # Maximum opportunities per team
  total_opportunities_range = 100

  team1Opportunities = generate_opportunities(team1.control, opportunities_cap, total_opportunities_range)
  team2Opportunities = generate_opportunities(team2.control, opportunities_cap, total_opportunities_range)

  max_attacks_per_team = 50
  team1_attacks_limit = min(BASE_ATTACKS_NUM + (team1.attacking - team2.defending) // 10, max_attacks_per_team)
  team2_attacks_limit = min(BASE_ATTACKS_NUM + (team2.attacking - team1.defending) // 10, max_attacks_per_team)

  team1Attacks = random.sample(range(1, total_opportunities_range + 1), team1_attacks_limit)
  team2Attacks = random.sample(range(1, total_opportunities_range + 1), team2_attacks_limit)


  time = 0

  atTeam1Lines, atTeam1Weights = check_lines(team1, "attacking")
  atTeam2Lines, atTeam2Weights = check_lines(team2, "attacking")
  crTeam1Lines, crTeam1Weights = check_lines(team1, "creative")
  crTeam2Lines, crTeam2Weights = check_lines(team2, "creative")
  deTeam1Lines, deTeam1Weights = check_lines(team1, "defensive")
  deTeam2Lines, deTeam2Weights = check_lines(team2, "defensive")

  while time < regularTime:
    randNum = random.randint(1, 100)
    events = []
    
    if randNum in team1Opportunities:
      teamEvent = []
      event = f"{team1.name} tiene la posesión"
      events.append(event)
      AssistantLine = random.choices(crTeam1Lines, crTeam1Weights)[0]
      Assistant = random.choice(team1.lines[AssistantLine])
      possibilities = [f"Que pase de {Assistant.name}!!!", f"Centro de {Assistant.name}!!!"]
      event = random.choice(possibilities)
      events.append(event)
      randNum = random.randint(1, 100)
      if randNum in team1Attacks:
        score[0] += 1
        goalscorerLine = random.choices(atTeam1Lines, atTeam1Weights)[0]
        goalscorer = random.choice(team1.lines[goalscorerLine])
        event = f"GOOOOOL del {team1.name}!!! {goalscorer.name}"
        events.append(event)
        teamEvent.append(f"Gol {goalscorer.name}, {time}")
        teamEvent.append(f"Asistencia {Assistant.name}")
        output["team1_events"].append(teamEvent)
      else:
        BlockLine = random.choices(deTeam2Lines, deTeam2Weights)[0]
        Block = random.choice(team2.lines[BlockLine])
        if Block.position == "GK":
          event = f"Gran atajada de {Block.name}!!!"
        else:
          possibilities = [f"Gran corte de {Block.name}!!!", f"Intercepción de {Block.name}!!!",
                           f"Despeje de {Block.name}!!!", f"Bloqueo de {Block.name}!!!", f"Recuperación de {Block.name}!!!"]
          event = random.choice(possibilities)
        events.append(event)

    if randNum in team2Opportunities:
      teamEvent = []
      event = f"{team2.name} tiene la posesión"
      events.append(event)
      AssistantLine = random.choices(crTeam2Lines, crTeam2Weights)[0]
      Assistant = random.choice(team2.lines[AssistantLine])
      possibilities = [f"Que pase de {Assistant.name}!!!", f"Centro de {Assistant.name}!!!"]
      event = random.choice(possibilities)
      events.append(event)
      randNum = random.randint(1, 100)
      if randNum in team2Attacks:
        score[1] += 1
        goalscorerLine = random.choices(atTeam2Lines, atTeam2Weights)[0]
        goalscorer = random.choice(team2.lines[goalscorerLine])
        event = f"GOOOOOL del {team2.name}!!! {goalscorer.name}"
        events.append(event)
        teamEvent.append(f"Gol {goalscorer.name}, {time}")
        teamEvent.append(f"Asistencia {Assistant.name}")
        output["team2_events"].append(teamEvent)
      else:
        BlockLine = random.choices(deTeam1Lines, deTeam1Weights)[0]
        Block = random.choice(team1.lines[BlockLine])
        if Block.position == "GK":
          event = f"Gran atajada de {Block.name}!!!"
        else:
          possibilities = [f"Gran corte de {Block.name}!!!", f"Intercepción de {Block.name}!!!",
                           f"Despeje de {Block.name}!!!", f"Bloqueo de {Block.name}!!!", f"Recuperación de {Block.name}!!!"]
          event = random.choice(possibilities)
        events.append(event)

    if events:
      output["timeline"][f"minuto_{time}"] = events

    time += 1

  output["final_score"] = {team1.name: score[0], team2.name: score[1]}
  return output

