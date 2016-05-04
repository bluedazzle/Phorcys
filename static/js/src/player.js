/**
 * Created by RaPoSpectre on 4/27/16.
 */

function deletePlayer(id) {
    mid = '#delModal' + id.toString();
    $(mid)
        .modal('setting', 'closable', false)
        .modal('show');
}
function addPlayer() {
    $('#addModal')
        .modal('setting', 'closable', false)
        .modal('setting', 'transition', 'horizontal flip')
        .modal('show');
}

$('.dropdown').dropdown({
    on: 'hover'
});


Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vPlayers',
    data: {
        data: {},
        teams: null,
        countrys: null,
        newPlayer: {
            nick: '',
            name: '',
            position: 0,
            belong: 0,
            intro: '',
            country: 0
        },
        query: ''
    },
    methods: {
        getData: function (event, page) {
            if (page == undefined) {
                return 0;
            }
            this.$set('players', null);
            var url = '';
            if (this.query == '') {
                url = generateUrl('api/v1/lol/players') + '&page=' + page.toString();
            } else {
                url = generateUrl('api/v1/lol/players') + '&page=' + page.toString() + '&query=' + this.query;
            }
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('players', data.body.player_list);
                    this.$set('pageObj', data.body.page_obj)
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        getTeams: function (event) {
            this.getCountry(null);
            if (this.noTeams) {
                url = generateUrl('api/v1/lol/teams') + '&all=1';
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('teams', data.body.team_list);
                    }
                })
            }
        },
        getCountry: function (event) {
            if (this.noCountry) {
                url = generateUrl('api/v1/lol/countries');
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('countrys', data.body.country_list);
                    }
                })
            }
        },
        deletePlayer: function (id) {
            url = generateUrlWithToken('admin/api/player/' + id);
            this.$http.delete(url, function (data) {
                if (data.status == 1) {
                    $.scojs_message('选手删除成功', $.scojs_message.TYPE_OK);
                    this.getData(null, 1);
                } else {
                    $.scojs_message('选手删除失败', $.scojs_message.TYPE_ERROR);
                }
            })
        },
        createNewPlayer: function () {
            var url = generateUrlWithToken('admin/api/player', getCookie('token'));
            var formData = new FormData($("#form1")[0]);
            formData.append('name', this.newPlayer.name);
            formData.append('nick', this.newPlayer.nick);
            formData.append('position', this.newPlayer.position);
            formData.append('belong', this.newPlayer.belong);
            formData.append('intro', this.newPlayer.intro);
            formData.append('country', this.newPlayer.country);

            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data.status == 1) {
                        $.scojs_message('选手新建成功', $.scojs_message.TYPE_OK);
                        this.getData(null, 1);
                    } else {
                        $.scojs_message('选手新建失败', $.scojs_message.TYPE_ERROR);
                    }

                },
                error: function (data) {
                    $.scojs_message('网络请求失败', $.scojs_message.TYPE_ERROR);
                }
            });
        }
    },
    ready: function () {
        this.getData(null, 1);
    },
    computed: {
        noData: function () {
            return this.players == null;
        },
        noTeams: function () {
            return this.teams == null;
        },
        noCountry: function () {
            return this.countrys == null;
        }
    }
});


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

function deletePlayer(id) {
    var mid = '#delPModal' + id.toString();
    $(mid)
        .modal({
            closable: false,
            onDeny: function () {
            },
            onApprove: function () {
                vm.deletePlayer(id.toString());
            }
        })
        .modal('show');
};