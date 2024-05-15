import random

json = {
  "name": "Messi",
  "overall": 95,
  "team": "Barcelona",
  "position": "ST"
}

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
    self.defenseLine = [i for i in self.players if i.position == "CB" or i.position == "FB"]
    self.backMidfieldLine = [i for i in self.players if i.position == "CDM"]
    self.midfieldLine = [i for i in self.players if i.position == "CM" or i.position == "WM"]
    self.frontMidfieldLine = [i for i in self.players if i.position == "CAM" or i.position == "WAM"]
    self.attackLine = [i for i in self.players if i.position == "ST" or i.position == "CF" or i.position == "FW"]

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

barcelona = Team("Barcelona", "blue", [
  Player("Messi", 95, "Barcelona", "ST"),
  Player("Pique", 85, "Barcelona", "CB"),
  Player("Busquets", 88, "Barcelona", "CDM"),
  Player("De Jong", 86, "Barcelona", "CM"),
  Player("Dembele", 84, "Barcelona", "WM"),
  Player("Griezmann", 87, "Barcelona", "CF")
])

madrid = Team("Real Madrid", "white", [
  Player("Benzema", 89, "Real Madrid", "ST"),
  Player("Ramos", 88, "Real Madrid", "CB"),
  Player("Casemiro", 87, "Real Madrid", "CDM"),
  Player("Modric", 87, "Real Madrid", "CM"),
  Player("Vinicius", 85, "Real Madrid", "WM"),
  Player("Asensio", 84, "Real Madrid", "WAM")
])

print(barcelona.name, ": ")
print("Defensa", barcelona.defending)
print("Control", barcelona.control)
print("Ataque", barcelona.attacking)

print()

print(madrid.name, ": ")
print("Defensa", madrid.defending)
print("Control", madrid.control)
print("Ataque", madrid.attacking)

print()

game(barcelona, madrid)


# attacking es la capacidad de un equipo de marcar goles
# control es la capacidad de un equipo de crear oportunidades de gol
# defending es la capacidad de un equipo de evitar que el equipo contrario marque

# con control se va a realizar más ataques, se determina una cantidad de numeros al azar que se generan en base al valor de control de un equipo. Esos valores no se pueden repetir entre ambos equipos. Se haze un random y si sale un numero que esta en las listas, se genera un ataque.

# con attacking se determina si el ataque es exitoso o no. Se hace un random y si el numero es mayor al valor de attacking, el ataque es exitoso. La probabilidad de que un ataque sea exitoso es mayor si el valor de attacking se determina con una comparacion entre el valor de defending del equipo contrario.