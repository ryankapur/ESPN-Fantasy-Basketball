from bs4 import BeautifulSoup
import requests

def setup(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    tableSubHead = soup.find_all('tr', class_='tableSubHead')
    tableSubHead = tableSubHead[0]
    listCats = tableSubHead.find_all('th')
    categories = []
    for cat in listCats:
        if 'title' in cat.attrs:
            categories.append(cat.string)
    rows = soup.findAll('tr', {'class': 'linescoreTeamRow'})
    teams = []
    for row in range(len(rows)):
        team_row = []
        for column in rows[row].findAll('td')[:(2 + len(categories))]:
            team_row.append(column.getText())

        # Add each team to a teams matrix.
        teams.append(team_row)
    return teams, categories

def computeStats(teams, categories):
    matchupsList = []
    for team1 in teams:
        for team2 in teams:
            score = calculateScore(team1[2:], team2[2:], categories)
            if team1 != team2:
                matchupsList.append(team1[0] + ' vs. ' + team2[0] + ' || SCORE (W-L-T): ' + '-'.join(map(str, score)))
        matchupsList.append('*' * 100)
    return matchupsList


# Calculates the score for individual matchups.
def calculateScore(teamA, teamB, categories):
    wins = 0
    losses = 0
    ties = 0

    turnoverCol = -1
    for category in categories:
        if category == 'TO':
            turnoverCol = categories.index(category)
            break
    for i, (a, b) in enumerate(zip(teamA, teamB)):
        # Ignore empty values.
        if a != '' and b != '':
            a = float(a)
            b = float(b)
            # When comparing turnovers, having a smaller value is a "win".
            if i == turnoverCol:
                if a < b:
                    wins += 1
                elif a == b:
                    ties += 1
                else:
                    losses += 1
            else:
                if a > b:
                    wins += 1
                elif a == b:
                    ties += 1
                else:
                    losses += 1
    return wins, losses, ties

teams, categories = setup('http://games.espn.com/fba/scoreboard?leagueId=224165&seasonId=2017')
score = computeStats(teams, categories)