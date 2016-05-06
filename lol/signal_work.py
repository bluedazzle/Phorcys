# coding: utf-8

from __future__ import unicode_literals

from lol.models import Tournament, Match, TournamentTheme, PlayerInfo


def generate_player_tournament_info(tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    player_info_list = tournament.player_tournaments.all()
    match_list = Match.objects.filter(tournament=tournament).order_by('-create_time')
    for player_info in player_info_list:
        team = player_info.player.belong

        win_times = 0.0
        fail_times = 0.0
        total_kill = 0.0
        total_dead = 0.0
        total_assist = 0.0
        total_time = 0.0
        total_money = 0.0
        total_farming = 0.0
        total_melee = 0.0
        times = 0

        for match in match_list:
            game_list = match.match_games.all()
            for game in game_list:
                gps = game.game_gameps.filter(player=player_info.player)
                if gps.exists():
                    gps = gps[0]
                    if game.win == team:
                        win_times += 1
                    else:
                        fail_times += 1
                    times += 1
                    total_kill += gps.kill
                    total_dead += gps.dead
                    total_assist += gps.assist
                    total_time += game.duration
                    total_money += gps.economic
                    total_farming += gps.farming
                    total_melee += gps.war_rate
        if times == 0:
            continue
        player_info.average_kill = round(total_kill / times, 2)
        player_info.average_dead = round(total_dead / times, 2)
        player_info.average_assist = round(total_assist / times, 2)
        player_info.average_time = round(total_time / times, 2)
        player_info.average_money_pm = round(total_money / times, 2)
        player_info.average_hit_p10m = round(total_farming / total_time * 10, 2)
        player_info.average_melee_rate = round((total_melee / times), 2)
        player_info.win_rate = round(win_times / times, 2)
        if fail_times == 0.0:
            player_info.win_fail_rate = win_times / 1
        else:
            player_info.win_fail_rate = round(win_times / fail_times, 2)
        if total_dead == 0.0:
            player_info.kda = (total_kill + total_assist) / 1.0
        else:
            player_info.kda = round((total_kill + total_assist) / total_dead, 2)
        player_info.victory_times = win_times
        player_info.fail_times = fail_times
        player_info.save()
    return tournament


def generate_player_tournament_theme_info(tournament_id):
    tournament_theme = TournamentTheme.objects.get(id=tournament_id)
    tournament_list = tournament_theme.theme_tournaments.all()
    total_player_info_list = tournament_theme.player_tournament_themes.all()

    for total_player_info in total_player_info_list:
        player = total_player_info.player

        times = 0
        average_assist = 0.0
        average_dead = 0.0
        average_kill = 0.0
        average_hit_p10m = 0.0
        average_melee_rate = 0.0
        average_money_pm = 0.0
        average_time = 0.0
        win_rate = 0.0
        kda = 0.0
        victory_times = 0.0
        tied_times = 0.0
        fail_times = 0.0
        win_fail_rate = 0.0

        for tournament in tournament_list:
            player_info = PlayerInfo.objects.filter(tournament=tournament, player=player)
            if not player_info.exists():
                continue
            player_info = player_info[0]
            if player_info.average_kill != 0.0 and player_info.average_melee_rate != 0.0:
                times += 1
                average_assist += player_info.average_assist
                average_dead += player_info.average_dead
                average_kill += player_info.average_kill
                average_hit_p10m += player_info.average_hit_p10m
                average_melee_rate += player_info.average_melee_rate
                average_money_pm += player_info.average_money_pm
                average_time += player_info.average_time
                kda += player_info.kda
                win_rate += player_info.win_rate
                win_fail_rate += player_info.win_fail_rate
                victory_times += player_info.victory_times
                tied_times += player_info.tied_times
                fail_times += player_info.fail_times
        if times == 0:
            continue
        total_player_info.average_dead = round(average_dead / times, 2)
        total_player_info.average_money_pm = round(average_money_pm / times, 2)
        total_player_info.average_assist = round(average_assist / times, 2)
        total_player_info.average_hit_p10m = round(average_hit_p10m / times, 2)
        total_player_info.average_melee_rate = round(average_melee_rate / times, 2)
        total_player_info.average_kill = round(average_kill / times, 2)
        total_player_info.average_time = round(average_time / times, 2)
        total_player_info.kda = round(kda / times, 2)
        total_player_info.win_fail_rate = round(win_fail_rate / times, 2)
        total_player_info.win_rate = round(win_rate / times, 2)
        total_player_info.victory_times = round(victory_times / times, 2)
        total_player_info.fail_times = round(fail_times / times, 2)
        total_player_info.tied_times = round(times / times, 2)
        total_player_info.save()


def get_player_info(tournament_id):
    tournament = generate_player_tournament_info(tournament_id)
    generate_player_tournament_theme_info(tournament.belong_id)
    print ('联赛 {0} 数据计算成功'.format(tournament.belong.name)).encode('utf-8')

