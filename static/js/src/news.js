/**
 * Created by RaPoSpectre on 4/28/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
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
            url = generateUrl('api/v1/lol/news') + '&datetime=string&all=1&page=' + page.toString();
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('newsList', data.body.news_list);
                    this.$set('pageObj', data.body.page_obj);
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            })
        },
        publishNews: function (id) {
            url = generateUrlWithToken('admin/api/news/' + id, getCookie('token'));
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    $.scojs_message('文章状态更改成功', $.scojs_message.TYPE_OK);
                    this.getData(null, 1);
                } else {
                    $.scojs_message('文章状态更改失败', $.scojs_message.TYPE_ERROR);
                }
            })
        },
        deleteNews: function (id) {
            url = generateUrlWithToken('admin/api/news/' + id, getCookie('token'));
            this.$http.delete(url, function (data) {
                if (data.status == 1) {
                    $.scojs_message('资讯删除成功', $.scojs_message.TYPE_OK);
                    this.getData(null, 1);
                } else {
                    $.scojs_message('资讯删除失败', $.scojs_message.TYPE_ERROR);
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

function deleteNews(id) {
    mid = '#delModal' + id.toString();
    $(mid)
        .modal({
            closable: false,
            onDeny: function () {
            },
            onApprove: function () {
                vm.deleteNews(id.toString());
            }
        })
        .modal('show');
}
