/**
 * Created by RaPoSpectre on 4/21/16.
 */

$('#tournamentList.item.card.a.image').dimmer({
    on: 'hover'
});
$('.special.cards .image').dimmer({
    on: 'hover'
});
function addPlayer() {
    $('#addModal')
        .modal('setting', 'closable', false)
        .modal('setting', 'transition', 'horizontal flip')
        .modal('show');
};
function addTmodel() {
    $('#addTModal')
        .modal('setting', 'closable', false)
        .modal('setting', 'transition', 'horizontal flip')
        .modal('show');
};


$(document).on('change', '.btn-file :file', function () {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
    var files = input.get(0).files;
    for (var i = 0, f; f = files[i]; i++) {
        if (!f.type.match('image.*')) {
            continue;
        }
        var reader = new FileReader();
        reader.onload = (function (theFile) {
            return function (e) {
                document.getElementById('uploadPicture').src = e.target.result;

            };
        })(f);
        reader.readAsDataURL(f);
    }
});

$('#start_time').datepicker({
    format: 'yyyy-mm-dd'
});
$('#end_time').datepicker({
    format: 'yyyy-mm-dd'
});
$('.ui.accordion')
    .accordion()
;
$('.dropdown').dropdown({
    on: 'hover'
});

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vTournament',
    data: {
        newTournament: {
            name: '',
            start_time: '',
            end_time: ''
        },
        nt: {
            name: '',
            ttid: '',
            teams: []
        }
    },
    methods: {
        getData: function (event) {

            url = generateUrlWithToken('admin/api/tournaments', getCookie('token'));
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('data', data.body);
                    Vue.nextTick(function () {
                        // DOM 更新
                        $('.progress').progress();
                        $('.special.cards .image').dimmer({
                            on: 'hover'
                        });

                    });
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        getTeams: function (event) {
            this.getTT(null);
            if (this.noTeams) {
                url = generateUrl('api/v1/lol/teams') + '&all=1';
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('teams', data.body.team_list);
                    }
                })
            }
        },
        getTT: function (event) {
            url = generateUrlWithToken('admin/api/tournamenttheme', getCookie('token'));
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('tts', data.body.tournamenttheme_list)
                }
            })
        },
        getFile: function (event) {
            var file = event.target.files[0];
            this.newTournament.cover = file;
        },
        createNewTournament: function (event) {
            url = generateUrlWithToken('admin/api/tournament', getCookie('token'));
            this.$http.post(url, this.nt, function (data) {
                if (data.status == 1) {
                    this.getData(null);
                     $.scojs_message('新建联赛成功', $.scojs_message.TYPE_OK);

                }else {
                     $.scojs_message('新建联赛失败', $.scojs_message.TYPE_ERROR);
                }
            })
        },
        createNewTournamentTheme: function (event) {
            url = generateUrlWithToken('admin/api/tournamenttheme', getCookie('token'));
            var formData = new FormData($("#form1")[0]);
            formData.append('name', this.newTournament.name);
            formData.append('start_time', this.newTournament.start_time);
            formData.append('end_time', this.newTournament.end_time);
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data.status == 1){
                        $.scojs_message('新建联赛主题成功', $.scojs_message.TYPE_OK);
                    }else {
                        $.scojs_message('新建联赛主题失败', $.scojs_message.TYPE_ERROR);
                    }

                },
                error: function (data) {
                    $.scojs_message('网络请求失败', $.scojs_message.TYPE_ERROR);
                }
            });
        }
    },
    ready: function () {
        this.getData(null);
    },
    computed: {
        noData: function () {
            return this.data == undefined;
            //return true;
        },
        noTeams: function () {
            return this.teams == undefined;
        }
    }
});



