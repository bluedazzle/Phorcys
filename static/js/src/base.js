/**
 * Created by RaPoSpectre on 4/20/16.
 */

Vue.config.delimiters = ['${', '}}'];
new Vue({
    el: '#vBase',
    data: {},
    methods: {
        logout: function (event) {
            url = generateUrl('admin/api/logout');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    delCookie('token');
                    window.location.href = '/admin/login';
                }
            });
        }
    },
    ready: function() {
        url = generateUrlWithToken('admin/api/admin', getCookie('token'));
        this.$http.get(url, function (data) {
            if (data.status == 1) {
                this.$set('admin', data.body);
            }else if(data.status == 3) {
                window.location.href = '/admin/login';
            }
        })
    },
    computed: {}
});
