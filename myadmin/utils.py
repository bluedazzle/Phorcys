# coding: utf-8

from __future__ import unicode_literals

def calculate_game_data(game):
    details = game.game_gameps.all()
    team1_total_economic = 0.0
    team2_total_economic = 0.0
    team1_total_kill = 0
    team2_total_kill = 0
    for detail in details:
        if detail.team == game.team1:
            team1_total_economic += detail.economic
            team1_total_kill += detail.kill
        else:
            team2_total_economic += detail.economic
            team2_total_kill += detail.kill
    game.team1_total_economic = team1_total_economic
    game.team2_total_economic = team2_total_economic
    game.team1_kill = team1_total_kill
    game.team2_kill = team2_total_kill
    game.save()
