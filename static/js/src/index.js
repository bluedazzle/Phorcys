/**
 * Created by RaPoSpectre on 4/20/16.
 */

Vue.config.delimiters = ['${', '}}'];
new Vue({
    el: '#vIndex',
    data: {
        data: {
            news: -1,
            topics: -1,
            users: -1
        },
        classLoading: 'ui active inline loader'
    },
    methods: {
        getData: function (event) {

            url = generateUrlWithToken('admin/api/index', getCookie('token'));
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('data', data.body);
                };
            })
        }
    },
    ready: function () {
        this.getData(null);
    },
    computed: {
        noData: function () {
            return this.data.news == -1;
            //return true;
        }
    }
});
