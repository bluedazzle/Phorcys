/**
 * Created by RaPoSpectre on 5/16/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vWeibo',
    data: {
        token: ''
    },
    methods: {
        getData: function () {
            this.$set('token', '');
            var url = generateUrlWithToken('admin/api/weibo', getCookie('token'));
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('token', data.body.token);
                    this.$set('uid', data.body.uid);
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            });
        },
        changeToken: function () {
            var url = generateUrlWithToken('admin/api/weibo', getCookie('token'));
            this.$http.post(url, null, function (data) {
                if(data.status == 1){
                    $.scojs_message('token刷新成功', $.scojs_message.TYPE_OK);
                    this.getData();
                }else {
                    $.scojs_message('token刷新失败', $.scojs_message.TYPE_ERROR);
                }
            })
        }

    },
    ready: function () {
        this.getData();
    },
    computed: {
        noData: function () {
            return this.token == '';
        }
    }
});
