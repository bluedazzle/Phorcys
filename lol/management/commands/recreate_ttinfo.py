# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from lol.models import Hero, SummonerSpells, Player, Team, Equipment, TournamentTheme, TotalTeamInfo, TotalPlayerInfo


class Command(BaseCommand):
    def handle(self, *args, **options):
        tournament_list = TournamentTheme.objects.all()
        for tournament in tournament_list:
            t = tournament.theme_tournaments.all()
            if not t.exists():
                continue
            t = t[0]
            team_list = t.tournament_teams.all()
            for team in team_list:
                try:
                    TotalTeamInfo(team=team,
                                  uuid='{0}t{1}'.format(tournament.id, team.id),
                                  tournament=tournament
                                  ).save()
                    player_list = team.team_players.all()
                    for player in player_list:
                        TotalPlayerInfo(uuid='{0}p{1}'.format(tournament.id, player.id),
                                        player=player,
                                        tournament=tournament).save()
                except Exception, e:
                    continue
