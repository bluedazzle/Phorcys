/**
 * Created by RaPoSpectre on 4/20/16.
 */

$('.ui.radio.checkbox')
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

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vMatch',
    data: {
        newGame: {
            duration: 0,
            game_time: '',
            team1_ban: [],
            team2_ban: [],
            game_id: ''
        }
    },
    methods: {
        getData: function (event) {
            this.match = null;
            mid = window.location.href.toString().split('?')[0].split('/').pop();
            url = generateUrl('api/v1/lol/match/' + mid);
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('match', data.body.match);
                    this.$set('games', data.body.game_list)
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        getHero: function (event) {
            if (this.heros != undefined) {
                return 1;
            }
            var url = generateUrl('api/v1/lol/hero') + '&all=1';
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
            if (game.team1_bans) {
                var t1b = [];
                for (var i in game.team1_bans) {
                    t1b.push(game.team1_bans[i].id.toString());
                }
                $('#mt1b').dropdown('set exactly', t1b);
                this.newGame.team1_ban = t1b;
            }else {
                this.newGame.team1_ban = null;
                 $('#mt1b').dropdown('clear');
            }
            if (game.team2_bans) {
                var t2b = [];
                for (var i in game.team2_bans) {
                    t2b.push(game.team2_bans[i].id.toString());
                }
                $('#mt2b').dropdown('set exactly', t2b);
                this.newGame.team2_ban = t2b;
            }else {
                this.newGame.team2_ban = null;
                $('#mt2b').dropdown('clear');
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
        clearFormData: function () {
            this.newGame.duration = 0;
            this.newGame.game_time = '';
            this.newGame.team1_ban = [];
            this.newGame.team2_ban = [];
            this.newGame.game_id = '';
            $('.dropdown.ban').dropdown('clear')
        }
    },
    ready: function () {
        this.getData(null);
        this.getHero(null);
    },
    computed: {
        noData: function () {
            return this.match == null;
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
