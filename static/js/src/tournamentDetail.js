/**
 * Created by RaPoSpectre on 4/22/16.
 */
function addPlayer() {
    $('#addModal')
        .modal('setting', 'closable', false)
        .modal('setting', 'transition', 'horizontal flip')
        .modal('show');
};

$('#start_time').datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss'
});

$('.dropdown').dropdown({
    on: 'hover',
    maxSelections: 2
});

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vTournamentDetail',
    data: {},
    methods: {
        getData: function (event) {
            tid = window.location.href.toString().split('?')[0].split('/').pop();
            url = generateUrl('api/v1/lol/tournament/' + tid) + '&ist=1';
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('tournament', data.body.tournament);
                    this.$set('matches', data.body.match_list);
                    this.$set('teams', data.body.team_list);
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        createMatch: function (event) {
            url = generateUrlWithToken('admin/api/tournament/' + this.tournament.id + '/match', getCookie('token'));
            this.newMatch.start_time = $('#start_time').val();
            this.$http.post(url, this.newMatch, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                    $.scojs_message('比赛创建成功', $.scojs_message.TYPE_OK);
                }else {
                    $.scojs_message('比赛创建失败', $.scojs_message.TYPE_ERROR);
                }
            })
        },
        deleteMatch: function (mid) {
            url = generateUrlWithToken('admin/api/tournament/' + this.tournament.id + '/match/' + mid, getCookie('token'));
            this.$http.delete(url, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                    $.scojs_message('比赛删除成功', $.scojs_message.TYPE_OK);
                }else {
                    $.scojs_message('比赛删除失败', $.scojs_message.TYPE_ERROR);
                }
            })
        },
        changeMatchStatus: function (mid, status) {
            url = generateUrlWithToken('admin/api/tournament/' + this.tournament.id + '/match/' + mid, getCookie('token'));
            this.$http.post(url, {"status": status}, function (data) {
                if (data.status == 1){
                    this.getData(null);
                    $.scojs_message('比赛状态更改成功', $.scojs_message.TYPE_OK);
                }else {
                    $.scojs_message('比赛状态更改失败', $.scojs_message.TYPE_ERROR);
                }
            })
        },
        formatType: function (type) {
            switch (type) {
                case 1:
                    return 'BO1';
                case 2:
                    return 'BO2';
                case 3:
                    return 'BO3';
                case 4:
                    return 'BO5';
                default:
                    return 'BO3';
            }
        },
        formatStatus: function (status) {
            switch (status) {
                case 1:
                    return '未进行';
                case 2:
                    return '进行中';
                case 3:
                    return '已结束';
            }
        }
    },
    ready: function () {
        this.getData(null);
    },
    computed: {
        noData: function () {
            return this.matches == undefined;
        }
    }
});

function deleteMatch(id) {
    var mid = '#delModal' + id.toString();
    $(mid)
        .modal({
            closable: false,
            onDeny: function () {
            },
            onApprove: function () {
                vm.deleteMatch(id.toString());
            }
        })
        .modal('show');
}

