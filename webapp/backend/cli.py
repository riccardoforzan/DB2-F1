import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON
from utils import get_number_of_cp_wins, get_teams, get_teams_won, get_seasons_count
from utils import get_races_count, get_pole_positions_count, get_top_ten_position_by_year
from utils import get_top_five_position_by_year, get_podiums, get_percentage_of_podiums_wrt_total_races
from utils import get_percentage_of_wins_wrt_total_races, best_finish_in_qualifying_and_race
from utils import worst_finish_in_qualifying_and_race, count_times_q3_reached
from utils import count_first_in_qualifying_and_won_race
from utils import driver_dnf
from utils import driver_championship_points_year_by_year
from utils import driver_championship_positions_year_by_year


#Read env file
load_dotenv()
SPARQL_ENDPOINT_URL = os.getenv('SPARQL_ENDPOINT_URL')
EXPOSED_PORT = int(os.getenv('EXPOSED_PORT'))

# Set up the SPARQLWrapper to perform queries in GraphDB
sparql = SPARQLWrapper(SPARQL_ENDPOINT_URL)
sparql.setMethod('POST')
sparql.setReturnFormat(JSON)

if __name__ == "__main__":

    wins = get_number_of_cp_wins(sparql, 1)
    print(f"Number of wins: {wins}")

    teams = get_teams(sparql, 1)
    print(f"Teams: {teams}")

    teams_won = get_teams_won(sparql, 1)
    print(f"Teams won: {teams_won}")

    seasons = get_seasons_count(sparql, 1)
    print(f"Seasons: {seasons}")

    races = get_races_count(sparql, 1)
    print(f"Races: {races}")

    poles = get_pole_positions_count(sparql, 1)
    print(f"Poles: {poles}")

    wins = get_pole_positions_count(sparql, 1)
    print(f"Wins: {wins}")

    ttpos = get_top_ten_position_by_year(sparql, 1)
    print(f"Top 10: {ttpos}")

    tfpos = get_top_five_position_by_year(sparql, 1)
    print(f"Top 5: {tfpos}")

    pod = get_podiums(sparql, 1)
    print(f"Podiums: {pod}")

    pod_wrt_total = get_percentage_of_podiums_wrt_total_races(sparql, 1)
    print(f"Podiums wrt total: {pod_wrt_total}")

    wins_wrt_total = get_percentage_of_wins_wrt_total_races(sparql, 1)
    print(f"Wins wrt total: {wins_wrt_total}")

    best_times = best_finish_in_qualifying_and_race(sparql, 1)
    print(f"Best times: {best_times}")

    worst_times = worst_finish_in_qualifying_and_race(sparql, 1)
    print(f"Worst times: {worst_times}")

    count_q3 = count_times_q3_reached(sparql, 1)
    print(f"Count Q3: {count_q3}")

    count_fqwr = count_first_in_qualifying_and_won_race(sparql, 1)
    print(f"Count first in qualy and race: {count_fqwr}")

    final_points = driver_championship_points_year_by_year(sparql, 1)
    print(f"Final points: {final_points}")

    final_positions = driver_championship_positions_year_by_year(sparql, 1)
    print(f"Final positions year by year: {final_positions}")

    count_dnf = driver_dnf(sparql, 1)
    print(f"Count dnf: {count_dnf}")
