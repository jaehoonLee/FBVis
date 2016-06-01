/**
 * Created by jaehoonlee88 on 16. 3. 1..
 */

var firstrun = true;
var treemap_datas = {};
var cur_profile_image = '/static/images/profile.png';
var cur_author_name = 'Name';
var cur_date = 'YYYY-MM-DD';
var cur_message = 'Text Message';
var cur_popularity = 'popularity'

var max_comments = 0;
var cur_max_comments = 500;
var max_likes = 0;
var cur_max_likes = 500;

var cur_treenode_type = "nothing";
var nodes;
var callback;
var cur_size_parameter = 1.0;

var treemap_parent_div;
var rest_treemap;


function call_treemap(text, width, height){
    /* reset treemap */

    // ================== Tree map definition =====================
    var treemap_width = width;
    var treemap_height = height;

    var date_div = d3.select(".infovis").append("div")
        .style("width", treemap_width + "px")
        .style("height", 20 + "px")

    treemap_parent_div = d3.select(".infovis").append("div")
        .attr("class", "treemap_parent_div")
        .style("position", "relative")
        .style("width", treemap_width  + "px")
        .style("height", (treemap_height + margin.top + margin.bottom) + "px")

    var treemap_weekday = new Array('Thurs', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed');

//Setting Date Div
    function date_div_add(date_width){
        d3.selectAll(".treemap_date").remove();

        var default_between_margin = date_width/1000;
        for(var i = 0; i < 7; i++){
            date_div.append("label")
                .attr("class", "treemap_date")
                .style("display", "inline-block")
                .style("width", (date_width - default_between_margin)+ "px")
                .style("margin-left", function(d){
                    if(i != 0)
                        return default_between_margin + 'px ';
                    return default_between_margin/2 + 'px';
                })
                .style("text-align", "center")
                .text(treemap_weekday[i]);
        }
    }

    date_div_add(treemap_width * 1/7);

// ================== Detail definition =====================

    var detail_width = $('.detail').width();
    var detail_height = total_height/3;

    d3.select(".detail").style("height", detail_height + "px")
        .style("overflow-y", "scroll")
        .style("overflow-x", "hidden");
    d3.select(".detail").append("h3")
        .attr("class", "ui header")
        .text("Post Detail");

    var detail_info = d3.select(".detail").append("div")
        .style("width", detail_width + "px")
        .style("position", "relative");


    var detail_sub_info = detail_info.append("div").style("width", $('.detail').width() + "px").style("height", 50 + 'px');

    var detail_img = detail_sub_info.append("img").attr("width", 50 + 'px').attr("height", 50 + 'px').style("float", "left");
    detail_img.attr("src", cur_profile_image);

    var detail_author = detail_sub_info.append("pre").style("float", "left").style("width", ($('.detail').width() - 70) + "px")
        .style("margin-left", "20px").style("margin-top", "5px").attr("class", "detail_text");
    detail_author.text(cur_author_name + '\n' + cur_date);

    var detail_message = detail_info.append("pre")
        .attr("class", "detail_message")
        .style("width",  detail_width + "px")
        .attr("class", "detail_text");
    detail_message.text(cur_message);

    var detail_picture = detail_info.append("img")
        .attr("class", "ui small image")
        .attr("src", "/static/images/content.png");

    var detail_popularity = detail_info.append("pre")
        .attr("class", "detail_popularity")
        .style("width",  detail_width + "px")
        .attr("class", "detail_text");

    var date_domain = [];

    var domain = {};
    nodes = [];

    var max_likes = 0;

    rest_treemap = function call_subtreemap(i, text, width, height){
        var treemap_width = width;
        var treemap_height = height;
        var default_between_margin = treemap_width/1000;

        callback = function(error, root) {

            if (error) throw error;

            if(firstrun) {
                treemap_datas[i] = root;

                if(Object.keys(treemap_datas).length == 7){

                    firstrun = false;
                    $('.infovis_loader').remove();
                    $('.detail_loader').remove();

                    //For slider in popularity
                    max_comments = 1000;
                    max_likes = 1000;
                    set_slider(max_comments, cur_max_comments, max_likes, cur_max_likes, nodes);

                }
            }

            //Treemap setting
            var poltype_value = d3.select("input[name=popularity_size]:checked").node().value;
            var treemap = d3.layout.treemap()
                .size([treemap_width/7 - default_between_margin, treemap_height])
                .sticky(false)
                .value(function(d) {

                    if(poltype_value == 'none')
                    {
                        return 1;
                    }
                    else if(poltype_value == 'likes'){
                        return Math.sqrt(d.likes);
                    }
                    else if(poltype_value == 'comments'){
                        return Math.sqrt(d.comments);
                    }
                    else if(poltype_value == 'postlength'){
                        return d.message.length;
                    }
                    else{
                        if(d.likes == 0)
                            return 0;
                        else
                            return Math.log(d.likes);
                    }


                });

            //Add div in treemap_parent_div
            var div = treemap_parent_div.append("div")
                .style("position", "absolute")
                .style("width", (treemap_width * 1/7 - default_between_margin)+ "px")
                .style("height", (treemap_height + margin.top + margin.bottom) + "px")
                .style("left", (treemap_width * i/7 + default_between_margin/2) + "px")
                .style("top", treemap_margin.top + "px");

            //make domain for date
            date_domain = root['children'].map(function(d){ return d['name']});

            //make domain for every attribute(because of color)
            root['children'].forEach(function(d){
                domain[d['name']] = true;
                d['children'].forEach(function(d){
                    domain[d['name']] = true;
                    d['children'].forEach(function(d){
                        domain[d['name']] = true;

                        if(max_comments < d['comments'])
                            max_comments = d['comments'];

                        if(max_comments < d['likes'])
                            max_comments = d['likes'];
                    });
                });
            });


            domain = Object.keys(domain);
            var range = domain.map(function(){  return randomColor(); })

            var node = div.datum(root).selectAll(".node")
                .data(treemap.nodes)
                .enter().append("div")
                .attr("class", function(d){

                    if(d.type == 'type'){
                        var author = d.author;
                        var str_name = author.split(" ").join("");

                        var date = new Date(d.created_time);

                        var date_index = i * 24 + date.getHours();
                        var author_id = d.fbid.split("_")[0];

                        return "node " + str_name + "_node " + date_index + "_date_node " + author_id + "_node";
                    }


                    return "node";
                })//"node"
                .call(position)
                .style("background-color", function(d) {

                    if(d.type == 'type')
                        return "#D3D3D3";
                    else
                        return null;
                })
                .on("mouseover", function(d){
                    //Detail Information
                    var date = new Date(d.created_time);

                    cur_profile_image = d.author_img_url;
                    cur_author_name = d.author;
                    cur_date = d.created_time;
                    cur_message = d.message;
                    cur_popularity = 'likes: ' + d.likes + '\ncomments: ' + d.comments;


                    detail_picture.attr("src", d.picture_url);
                    detail_img.attr("src", d.author_img_url);
                    detail_author.text(d.author + "\n" + d.created_time);
                    detail_message.text(cur_message);
                    detail_popularity.text(cur_popularity)

                    treemap_barchart_call(d.created_time, "brown");

                    //Send Signal
                    $.ajax({
                        url: 'treemap_assign/' + d.fbid + '/',
                        success: function(data){

                        }
                    });

                })
                .on("mouseout", function(d){
                    treemap_barchart_call(d.created_time, "steelblue")

                });
            nodes.push(node);
        }

        if(firstrun){
            d3.json("/treemap_data?days=" + i + '&key_word=' + text, callback);

        }
        else{
            callback(false, treemap_datas[i])
        }

    }

    /* For resize */
    for(var i = 0 ; i < 7; i++){
        rest_treemap(i, text, width, height);
    }

    var color;
    d3.json("/treemap_domain", function(error, domain){
        var range = domain.map(function(){  return randomColor(); })
        color = d3.scale.ordinal()
            .domain(domain)
            .range(range);
    });

    d3.selectAll("input[name=popularity_size]").on("change", function change() {
        treemap_parent_div.html('');

        for(var i = 0 ; i < 7; i++){
            rest_treemap(i, text, width, height);
        }

        /*
        for(var i in nodes){
            nodes[i]
                .transition()
                .duration(500)
                .style("background-color", function(d) {

                    if(d.type != 'type')
                        return null;

                    if('author' == cur_treenode_type) {
                        return "#D3D3D3";
                    }
                    else if('nothing' == cur_treenode_type){
                        return "#D3D3D3";
                    }
                    else if('images' == cur_treenode_type){

                        if(d.picture_exist == '')
                            return "#D3D3D3"

                        return "#2432F0";
                    }
                    else if('close' == cur_treenode_type){
                        return "#D3D3D3";
                    }
                    else
                        return null;
                });
        }
        */
    });


    /*
    d3.selectAll("input[name=example2]").on("change", function change() {
        var popular_color = d3.scale.linear().range(['#D3D3D3','#000000']).domain([0, cur_max_likes]);

        cur_treenode_type = this.value;

        //Author Update
        if(cur_treenode_type == 'author'){
            person_execute = true;
            executeQuery();
        }
        else{
            person_execute = false;
        }


        for(var i in nodes){
            nodes[i]
                .transition()
                .duration(500)
                .style("background-color", function(d) {

                    if(d.type != 'type')
                        return null;

                    if('author' == cur_treenode_type) {
                        return "#D3D3D3";
                    }
                    else if('nothing' == cur_treenode_type){
                        return "#D3D3D3";
                    }
                    else if('images' == cur_treenode_type){

                        if(d.picture_exist == '')
                            return "#D3D3D3"


                        return "#2432F0";
                    }
                    else if('close' == cur_treenode_type){
                        return "#D3D3D3";
                    }
                    else
                        return null;
                });
        }

    });
    */
}

function wordcloud_treemap_call(word, cur_color){
    for(var i in nodes){
        nodes[i]
            .style("background-color", function(d) {

                if(d.type == 'type'){

                    if(typeof d.message == 'undefined')
                        return "#D3D3D3";

                    var word_lst = d.message.toLowerCase().split(" ");
                    var word_exist = (word_lst.indexOf(word.toLowerCase()) > -1);


                    if(word_exist){
                        return cur_color;
                        //return '#000000';
                    }
                    else {
                        //console.log(d3.select(this).style("background-color"));
                        return d3.select(this).style("background-color");
                    }

                }

                else
                    return null;
            });
    }
}

function reset_wordcloud_treemap(word, selected_word, selected_color){
    for(var i in nodes){
        nodes[i]
            .style("background-color", function(d) {

                if(d.type == 'type'){

                    if(typeof d.message == 'undefined')
                        return "#D3D3D3";


                    var word_lst = d.message.toLowerCase().split(" ");

                    for(var sel_i in selected_word){
                        var sel_word = selected_word[sel_i];
                        if(word_lst.indexOf(sel_word.toLowerCase()) > -1){
                            return selected_color[sel_i];
                        }
                    }

                    //Finding words.

                    var word_exist = (word_lst.indexOf(word.toLowerCase()) > -1);


                    if(word_exist){
                        return '#D3D3D3';
                    }
                    else {
                        //console.log(d3.select(this).style("background-color"));
                        return d3.select(this).style("background-color");
                    }

                }

                else
                    return null;
            });
    }
}

function treemap_barchart_call(created_time, color){
    //Color Date
    var date = new Date(created_time);

    //Update Barchart
    for(var index in barchart_x_list){
        var val = new Date(barchart_x_list[index]);
        var day = val.getDate();
        var time = val.getHours();
        var class_name = '.' + day + '-' + time;

        if(day == date.getDate() && time <= date.getHours() && date.getHours() < (time+1)){
            $(class_name).css("fill", color);
        }
        else if(day == date.getDate() && date.getHours() == 24){
            class_name = '.' + day + '-' + 23;
            $(class_name).css("fill", color);
        }
        else{
            $(class_name).css("fill", "steelblue");

        }
    }
}