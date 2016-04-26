/**
 * Created by RaPoSpectre on 4/20/16.
 */

$('.checkbox')
    .checkbox()
;


$('#start_time').datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss'
});

$('.ui.accordion')
    .accordion();

$('.dropdown.ban').dropdown({
    on: 'hover',
    maxSelections: 3
});

$('.dropdown.player').dropdown({
    on: 'hover',
});

$('#selectEquip').dropdown({
    on: 'hover',
    maxSelections: 6
});

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vMatch',
    data: {
        newGame: {
            duration: 0,
            game_time: '',
            team1_ban: [],
            team2_ban: [],
            game_id: '',
            team1_dragon: 0,
            team2_dragon: 0,
            team1_nahsor: 0,
            team2_nahsor: 0,
            team1_tower: 0,
            team2_tower: 0,
            over: false
        },
        teamId: null,
        addDetail: false,
        detail: {
            game_id: '',
            team_id: '',
            player_id: '',
            hero_id: '',
            position: '',
            summoner1: '',
            summoner2: '',
            game_player_id: '',
            equipments: [],
            guard: '',
            level: 0,
            kill: 0,
            dead: 0,
            assist: 0,
            war_rate: 0,
            damage_rate: 0,
            farming: 0,
            economic: 0

        },
        details: null
    },
    methods: {
        getData: function (event) {
            this.match = null;
            mid = window.location.href.toString().split('?')[0].split('/').pop();
            url = generateUrl('api/v1/lol/match/' + mid);
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('match', data.body.match);
                    this.$set('games', data.body.game_list);
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        getHero: function (event) {
            if (this.heros != undefined) {
                return 1;
            }
            var url = generateUrl('api/v1/lol/heros') + '&all=1';
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('heros', data.body.hero_list);
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        modifyGame: function (event) {
            this.clearFormData();
            var id = parseInt(event.target.id.toString().replace('add', ''));
            var game = this.games[id];
            this.newGame.duration = game.duration;
            this.newGame.win = game.win.id;
            this.newGame.game_id = game.game_id;
            this.newGame.over = game.over;
            this.newGame.team1_dragon = game.team1_dragon;
            this.newGame.team2_dragon = game.team2_dragon;
            this.newGame.team1_nahsor = game.team1_nahsor;
            this.newGame.team2_nahsor = game.team2_nahsor;
            this.newGame.team1_tower = game.team1_tower;
            this.newGame.team2_tower = game.team2_tower;
            if (game.team1_bans) {
                var t1b = [];
                for (var i in game.team1_bans) {
                    t1b.push(game.team1_bans[i].id.toString());
                }
                $('#mt1b').dropdown('set exactly', t1b);
                this.newGame.team1_ban = t1b;
            } else {
                this.newGame.team1_ban = [];
                $('#mt1b').dropdown('clear');
            }
            if (game.team2_bans) {
                var t2b = [];
                for (var i in game.team2_bans) {
                    t2b.push(game.team2_bans[i].id.toString());
                }
                $('#mt2b').dropdown('set exactly', t2b);
                this.newGame.team2_ban = t2b;
            } else {
                this.newGame.team2_ban = [];
                $('#mt2b').dropdown('clear');
            }
            if (game.win.id == game.team1.id) {
                $('#w1').checkbox('check');
            } else {
                $('#w2').checkbox('check');
            }
            this.getHero(null);
            //$('.dropdown.ban').dropdown('set exactly', this.newGame.team1_ban);
            //alert(JSON.stringify(this.newGame));
            Vue.nextTick(function () {
                //$('#w1').checkbox('set checked');
                $('#addModal')
                    .modal('setting', 'closable', false)
                    .modal('setting', 'transition', 'horizontal flip')
                    .modal('show');
            });
        },
        createNewGame: function (event) {
            this.newGame.game_time = $('#start_time').val();
            this.newGame.team1 = this.match.team1.id;
            this.newGame.team2 = this.match.team2.id;
            var url = generateUrlWithToken('admin/api/tournament/' + this.match.tournament_id + '/match/' + this.match.id + '/game',
                getCookie('token'));
            this.$http.post(url, this.newGame, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                }
            })
        },
        getPlayers: function (event) {
            if (this.detail.team_id) {
                url = generateUrl('api/v1/lol/team/' + this.detail.team_id) + '&add_player=1';
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('players', data.body.team.player_list);
                    }
                })
            }
        },
        getSummoner: function (event) {
            if (this.summoner) {
                return 1
            }
            url = generateUrl('api/v1/lol/summoners');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('summoners', data.body.summonerspells_list);
                }
            })
        },
        getEquipment: function (event) {
            if (this.equipments) {
                return 1
            }
            url = generateUrl('api/v1/lol/equipments') + '&all=1';
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('equipments', data.body.equipment_list);
                }
            })
        },
        createDetail: function (event) {
            this.clearDetailData();
            var id = parseInt(event.target.id.toString().replace('addDetail', ''));
            this.detail.game_id = this.games[id].game_id;
            this.addDetail = true;
        },
        modifyDetail: function (event) {
            this.clearDetailData();
            var id = event.target.id.toString().replace('dm', '').split(',');
            var game_id = id[1];
            var i = parseInt(id[2]);
            var gid = id[0];
            this.detail.game_id = game_id;
            this.detail.game_player_id = gid;
            var detail = this.details[i];
            this.detail.assist = detail.assist;
            this.detail.level = detail.level;
            this.detail.kill = detail.kill;
            this.detail.dead = detail.dead;
            this.detail.damage_rate = detail.damage_rate;
            this.detail.farming = detail.farming;
            this.detail.war_rate = detail.war_rate;
            this.detail.economic = detail.economic;
            this.detail.player_id = detail.player_id;
            this.detail.team_id = detail.team_id;
            this.detail.position = detail.position.code;
            this.detail.summoner1 = detail.summoner1_id;
            this.detail.summoner2 = detail.summoner2_id;
            this.detail.guard = detail.guard_id;
            if (detail.equipment_list) {
                var t1b = [];
                for (var i in detail.equipment_list) {
                    t1b.push(detail.equipment_list[i].id.toString());
                }
                $('#selectEquip').dropdown('set exactly', t1b);
                this.detail.equipments = t1b;
            } else {
                this.detail.equipments = null;
                $('#selectEquip').dropdown('clear');
            }
            this.getPlayers(null);
            $('#sPlayer').dropdown('set text', detail.player.nick);
            $('#sHero').dropdown('set selected', detail.hero_id);
            $('#sPosition').dropdown('set selected', detail.position.code);
            $('#sS1').dropdown('set selected', detail.summoner1_id);
            $('#sS2').dropdown('set selected', detail.summoner2_id);
            $('#sGuard').dropdown('set selected', detail.guard_id);
            this.addDetail = true;
        },
        cancelDetail: function () {
            this.clearDetailData();
            this.addDetail = false;
        },
        saveDetail: function () {
            url = generateUrlWithToken('admin/api/game', getCookie('token'));
            this.$http.post(url, this.detail, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                    this.addDetail = false;
                }
            });
        },
        getDetail: function (event) {
            this.details = null;
            var id = event.target.id.toString().replace('detail', '');
            url = generateUrl('api/v1/lol/game/' + id);
            this.$http.get(url, function(data) {
                if (data.status == 1){
                    this.$set('details', data.body.gameplayer_list);
                }
            })
        },
        deleteGame: function(id) {
            url = generateUrlWithToken('admin/api/game/' + id, getCookie('token'));
            this.$http.delete(url, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                }
            })

        },
        deleteGamePlayer: function(id) {
            url = generateUrlWithToken('admin/api/gameplayer/' + id, getCookie('token'));
            this.$http.delete(url, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                }
            })

        },
        clearFormData: function () {
            this.newGame.duration = 0;
            this.newGame.game_time = '';
            this.newGame.team1_ban = [];
            this.newGame.team2_ban = [];
            this.newGame.game_id = '';
            this.newGame.over = false;
            this.newGame.team1_dragon = 0;
            this.newGame.team2_dragon = 0;
            this.newGame.team1_nahsor = 0;
            this.newGame.team2_nahsor = 0;
            this.newGame.team1_tower = 0;
            this.newGame.team2_tower = 0;
            $('.dropdown.ban').dropdown('clear')
        },
        clearDetailData: function () {
            this.detail.assist = 0;
            this.detail.kill = 0;
            this.detail.dead = 0;
            this.detail.damage_rate = 0;
            this.detail.farming = 0;
            this.detail.war_rate = 0;
            this.detail.economic = 0;
            this.detail.equipments = [];
            this.detail.game_id = '';
            this.detail.player_id = '';
            this.detail.team_id = '';
            this.detail.level = 0;
            this.detail.position = '';
            this.detail.summoner1 = '';
            this.detail.summoner2 = '';
            this.detail.guard = '';
            this.detail.game_player_id = '';
            $('#selectEquip').dropdown('clear');
            $('#sPlayer').dropdown('clear');
            $('#sHero').dropdown('clear');
            $('#sPosition').dropdown('clear');
            $('#sS1').dropdown('clear');
            $('#sS2').dropdown('clear');
            $('#sGuard').dropdown('clear');
        }
    },
    ready: function () {
        this.getData(null);
        this.getHero(null);
        this.getSummoner(null);
        this.getEquipment(null);
    },
    computed: {
        noData: function () {
            return this.match == null;
        },
        w1Check: function () {
            return true;
        },
        noDetails: function () {
            return this.details == null;
        }
    }
});

function addPlayer() {
    $('#addModal')
        .modal('setting', 'closable', false)
        .modal('setting', 'transition', 'horizontal flip')
        .modal('show');
    vm.clearFormData();
};

function deleteGame(id) {
    var mid = '#delGModal' + id.toString();
    $(mid)
        .modal({
            closable: false,
            onDeny: function () {
            },
            onApprove: function () {
                vm.deleteGame(id.toString());
            }
        })
        .modal('show');
};

function deleteGamePlayer(id) {
    var mid = '#delGPModal' + id.toString();
    $(mid)
        .modal({
            closable: false,
            onDeny: function () {
            },
            onApprove: function () {
                vm.deleteGamePlayer(id.toString());
            }
        })
        .modal('show');
}