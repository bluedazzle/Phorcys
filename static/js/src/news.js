/**
 * Created by RaPoSpectre on 4/28/16.
 */

Vue.config.delimiters = ['${', '}}'];
new Vue({
    el: '#vNews',
    data: {
        data: {},
    },
    methods: {
        getData: function (event, page) {
            if (page == undefined) {
                return 0;
            }
            this.$set('newsList', null);
            url = generateUrl('api/v1/lol/news') + '&page=' + page.toString();
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('newsList', data.body.news_list);
                    this.$set('pageObj', data.body.page_obj);
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        }
    },
    ready: function () {
        this.getData(null, 1);
    },
    computed: {
        noData: function () {
            return this.newsList == null;
        }
    }
});
