from elosports.elo import Elo
from pathlib import Path
import lxml.html

eloLeague = Elo(k=10)

errors = 0
num_games = 0


class StupidJeopardyError(Exception):
    pass


for game in Path("jarchive_html").glob("*.html"):
    num_games += 1
    print(game)

    try:
        game_content = lxml.html.fromstring(game.read_text(encoding="utf-8"))

        contestant_names = list(map(lambda c: c.text_content().strip(), game_content.xpath("//p[@class='contestants']/a")))

        # Just missing data
        if not game_content.xpath("//h3[text()='Final scores:']/following-sibling::table"):
            continue

        final_names = game_content.xpath("//h3[text()='Final scores:']/following-sibling::table")[0].xpath(".//td[@class='score_player_nickname']/text()")
        final_scores = game_content.xpath("//h3[text()='Final scores:']/following-sibling::table")[0].xpath(".//td[@class='score_positive' or @class='score_negative']/text()")

        if len(final_names) < 3:
            raise StupidJeopardyError("Couldn't find at least 3 players")
        if len(final_scores) < 3:
            raise StupidJeopardyError("Couldn't find at least 3 scores")

        if len(final_names) is not len(final_scores):
            raise StupidJeopardyError("mismatch in num of names and scores")

        final_names_temp = []

        def find_name_for_nickname(nn):
            # What a disaster. People like adding dumb bullshit to their names
            nn = nn.lower().replace('"', "").replace(":)", "").replace("!", "")

            real_name_list = list(filter(lambda cn: nn in cn.lower(), contestant_names))
            if not real_name_list:
                raise StupidJeopardyError("Couldn't find nickname in contestant list")
            if len(real_name_list) > 1:
                # Try to remove ambiguity by adding a space, indicating a first name. Fixes problems like one player named
                # "John", and another person named "Nick Johnson"
                return find_name_for_nickname(f"{nn} ")
            return real_name_list[0]

        for nickname in final_names:
            real_name = find_name_for_nickname(nickname)
            if real_name not in eloLeague.ratingDict:
                eloLeague.addPlayer(real_name)
            final_names_temp.append(real_name)

        final_names = final_names_temp

        # Transform score into int
        final_scores = list(map(lambda s: int(s.replace("$", "").replace(",", "")), final_scores))

        final_players = list(zip(final_names, final_scores))

        winner = sorted(final_players, key=lambda f: f[1], reverse=True)[0]

        for loser in filter(lambda l: l != winner, final_players):
            eloLeague.gameOver(winner=winner[0], loser=loser[0], winnerHome=None)
    except StupidJeopardyError:
        errors += 1
        print("who cares")

print(f"{errors} errors out of {num_games}")

for r in sorted(eloLeague.ratingDict, key=lambda p: eloLeague.ratingDict[p], reverse=True):
    print(f"{r} - {eloLeague.ratingDict[r]}")



# eloLeague.addPlayer("Daniel", rating = 1600)
# eloLeague.addPlayer("Harry")
#eloLeague.expectResult(eloLeague.ratingDict['Daniel'],eloLeague.ratingDict['Harry'])
#print("ads")