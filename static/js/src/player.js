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
new Vue({
    el: '#vPlayers',
    data: {
        data: {},
        teams: null,
        newPlayer: {
            nick: '',
            name: '',
            position: 0,
            belong: 0,
            intro: ''
        }
    },
    methods: {
        getData: function (event, page) {
            if (page == undefined) {
                return 0;
            }
            this.$set('players', null);
            url = generateUrl('api/v1/lol/players') + '&page=' + page.toString();
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
            if (this.noTeams) {
                url = generateUrl('api/v1/lol/teams') + '&all=1';
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('teams', data.body.team_list);
                    }
                })
            }
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