/**
 * Created by jaehoonlee88 on 16. 3. 30..
 */
function set_slider(max_comments, cur_max_comments, max_likes, cur_max_likes, nodes){
    $( "#slider" ).slider({
        min : 0,
        //max : max_comments,
        //value : cur_max_comments,
        max: max_likes,
        value : cur_max_likes,
        create : function(event, ui) {
            //$( "#amount" ).html("Comments : " + cur_max_comments);
            $( "#amount" ).html("Likes : " + cur_max_likes);
        },
        slide: function( event, ui ) {
            //$( "#amount" ).html("Comments : " + ui.value);
            $( "#amount" ).html("Likes : " + ui.value);

            //cur_max_comments = ui.value;
            cur_max_likes = ui.value;
        },
        stop: function(event, ui){
            if('popularity' == cur_treenode_type){
                var popular_color = d3.scale.linear().range(['#D3D3D3','#000000']).domain([0, ui.value]);
                for(var i in nodes){
                    nodes[i].transition()
                        .duration(500).style("background-color", function(d) {
                            if(d.type == 'type'){
                                //return popular_color(d.comments);
                                return popular_color(d.likes);
                            }
                        });
                }
            }

        }
    });


    $( "#slider_size" ).slider({
        min : 0.0,
        //max : max_comments,
        //value : cur_max_comments,
        max: 2.0,
        value : 1.0,
        step : 0.1,
        create : function(event, ui) {
            //$( "#amount" ).html("Comments : " + cur_max_comments);
            $( "#amount_size" ).html("Likes Parameter : " + cur_size_parameter);
        },
        slide: function( event, ui ) {
            //$( "#amount" ).html("Comments : " + ui.value);
            $( "#amount_size" ).html("Likes Parameter : " + ui.value);

            //cur_max_comments = ui.value;
            cur_size_parameter = ui.value;
        },
        stop: function(event, ui){
            console.log(cur_treenode_type);
            if('popularity_size' == cur_treenode_type){
                treemap_parent_div.html('');

                for(var i in treemap_datas) {
                    var root = treemap_datas[i];
                    var authors = root["children"][0]["children"];
                    for (var j in authors) {
                        var posts = authors[j]["children"];
                        for (var k in posts) {
                            posts[k].size = posts[k].likes + 1000 * (cur_size_parameter - 1);
                        }
                    }
                }

                for(var i = 0 ; i < 7; i++){
                    rest_treemap(i, '', treemap_width, treemap_height);
                }
            }

        }
    });

}
