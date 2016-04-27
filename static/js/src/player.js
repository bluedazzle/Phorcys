/**
 * Created by RaPoSpectre on 4/27/16.
 */


Vue.config.delimiters = ['${', '}}'];
new Vue({
    el: '#vTeams',
    data: {
        data: {

        },
    },
    methods: {
        getData: function (event, page) {
            if(page == undefined){
                return 0;
            }
            this.$set('teams', null);
            url = generateUrl('api/v1/lol/teams') + '&add_player=1&page=' + page.toString();
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('teams', data.body.team_list);
                    this.$set('pageObj', data.body.page_obj)
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
            return this.teams == null;
        }
    }
});
