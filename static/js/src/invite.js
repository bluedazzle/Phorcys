/**
 * Created by RaPoSpectre on 4/27/16.
 */

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
    el: '#vInvites',
    data: {
        invites: [],
        query: '',
        number: 0,
        used: 0,
        unuse: 0,
        total: 0
    },
    methods: {
        getData: function (event, page) {
            if (page == undefined) {
                return 0;
            }
            this.$set('invites', null);
            var url = '';
            if (this.query == '') {
                url = generateUrlWithToken('admin/api/invites', getCookie('token')) + '&page=' + page.toString();
            } else {
                url = generateUrlWithToken('admin/api/invites', getCookie('token')) + '&page=' + page.toString() + '&query=' + this.query;
            }
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('invites', data.body.invite_list);
                    this.$set('pageObj', data.body.page_obj)
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            });
            url = generateUrlWithToken('admin/api/invite', getCookie('token'));
            this.$http.get(url, function (data) {
                if (data.status == 1){
                    this.used = data.body.used;
                    this.unuse = data.body.unuse;
                    this.total = data.body.total;
                }
            })
        },
        createNewInvites: function() {
            this.$http.post('api/invite', {'number': this.number}, function (data) {
                if(data.status == 1){
                    this.getData(null, 1);
                    $.scojs_message('邀请码产生成功', $.scojs_message.TYPE_OK);
                }else {
                    $.scojs_message('邀请码产生失败', $.scojs_message.TYPE_ERROR);
                }
            })
        }
    },
    ready: function () {
        this.getData(null, 1);
    },
    computed: {
        noData: function () {
            return this.invites == null;
        }
    }
});


