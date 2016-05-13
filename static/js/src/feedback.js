/**
 * Created by RaPoSpectre on 5/13/16.
 */

$('.dropdown').dropdown({
    on: 'hover'
});

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vFeedback',
    data: {
    },
    methods: {
        getData: function (event, page) {
            if (page == undefined) {
                return 0;
            }
            this.$set('feedbacks', null);
            var url = generateUrlWithToken('admin/api/feedbacks', getCookie('token')) + '&page=' + page.toString();
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('feedbacks', data.body.feedback_list);
                    this.$set('pageObj', data.body.page_obj)
                } else if (data.status == 3) {
                    window.location.href = '/admin/login';
                }
            });
        },
        handle: function (id) {
            var url = generateUrlWithToken('admin/api/feedbacks', getCookie('token'))
            this.$http.post(url, {'fid': id}, function (data) {
                if(data.status==1){
                    $.scojs_message('反馈处理成功', $.scojs_message.TYPE_OK);
                    this.getData(null, 1);
                }else{
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
            return this.feedbacks == null;
        }
    }
});