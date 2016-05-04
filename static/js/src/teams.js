/**
 * Created by RaPoSpectre on 4/20/16.
 */
$('.dropdown').dropdown({
    on: 'hover'
});

Vue.config.delimiters = ['${', '}}'];
new Vue({
    el: '#vTeams',
    data: {
        newTeam: {
            name: '',
            abbreviation: '',
            info: '',
            country: ''
        },
        query: ''
    },
    methods: {
        getData: function (event, page) {
            if (page == undefined) {
                return 0;
            }
            this.$set('teams', null);
            var url = '';
            if (this.query == '') {
                url = generateUrl('api/v1/lol/teams') + '&add_player=1&page=' + page.toString();
            } else {
                url = generateUrl('api/v1/lol/teams') + '&add_player=1&page=' + page.toString() + '&query=' + this.query;
            }
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('teams', data.body.team_list);
                    this.$set('pageObj', data.body.page_obj)
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
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
        createNewTeam: function () {
            var url = generateUrlWithToken('admin/api/team', getCookie('token'));
            var formData = new FormData($("#form1")[0]);
            formData.append('name', this.newTeam.name);
            formData.append('abbreviation', this.newTeam.abbreviation);
            formData.append('info', this.newTeam.info);
            formData.append('country', this.newTeam.country);
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    if (data.status == 1) {
                        $.scojs_message('战队新建成功', $.scojs_message.TYPE_OK);
                        this.getData(null, 1);
                    } else {
                        $.scojs_message('战队新建失败', $.scojs_message.TYPE_ERROR);
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