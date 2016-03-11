/**
 * Created by jaehoonlee88 on 16. 3. 1..
 */
// ================== Tree map definition =====================
var treemap_margin = {top: 20, right: 10, bottom: 10, left: 10};
var treemap_width = total_width - treemap_margin.left - treemap_margin.right;
var treemap_height = total_height/3 -treemap_margin.top - treemap_margin.bottom;

var date_div = d3.select(".infovis").append("div")
    //.style("position", "absolute")
    .style("width", treemap_width + "px")
    .style("height", 20 + "px")
//.style("margin-left", treemap_margin.left)
//.style("left", 0 + "px")
//.style("top", 0 + "px")

var parent_div = d3.select(".infovis").append("div")
    .attr("class", "parent_div")
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
            //.style("position", "absolute")
            .attr("class", "treemap_date")
            .style("display", "inline-block")
            .style("width", (date_width - default_between_margin)+ "px")
            .style("margin-left", function(d){
                if(i != 0)
                    return default_between_margin + 'px ';
                return default_between_margin/2 + 'px';
            })
            //.style("left", treemap_width * i/7 + "px")
            .style("text-align", "center")
            .text(treemap_weekday[i]);
    }
}

date_div_add(treemap_width * 1/7);



/*
 var treemap_svg = parent_div.append("svg")
 .style("position", "absolute")
 .attr("width", (treemap_width + margin.left + margin.right) + "px")
 .attr("height", (height + margin.top + margin.bottom) + "px")
 .style("left", margin.left + "px")
 .style("top", margin.top + "px")
 .append("g")
 .attr("transform", "translate(" + 0 + "," + 0 + ")");


 var treemap_y = d3.scale.linear()
 .range([(height), 0]);
 treemap_y.domain([0, 100]);


 var treemap_yAxis = d3.svg.axis()
 .scale(treemap_y)
 .orient("left")
 .ticks(0)
 .tickSubdivide(0);


 treemap_svg.append("g")
 .attr("class", "treemap_y axis")
 .call(treemap_yAxis)
 .attr("transform", "translate(" + treemap_width/7 + ",0)")
 .append("text")
 .attr("y", 6)
 .attr("dy", ".71em")
 .style("text-anchor", "end")
 .text("HELLO WORLD");
 */
// ================== Detail definition =====================

var detail_width = $('.detail').width();
var detail_height = total_height/3;

d3.select(".detail").style("height", detail_height + "px")
    .style("overflow-y", "scroll")
    .style("overflow-x", "hidden");

var detail_info = d3.select(".detail").append("div")
    .style("width", detail_width + "px")
    .style("position", "relative");


var detail_sub_info = detail_info.append("div").style("width", $('.detail').width() + "px").style("height", 50 + 'px');

var detail_img = detail_sub_info.append("img").attr("width", 50 + 'px').attr("height", 50 + 'px').style("float", "left");

var detail_author = detail_sub_info.append("pre").style("float", "left").style("width", ($('.detail').width() - 70) + "px")
    .style("margin-left", "20px").style("margin-top", "5px").attr("class", "detail_text");

var detail_message = detail_info.append("pre")
    .attr("class", "detail_message")
    .style("width",  detail_width + "px")
    .attr("class", "detail_text");


var detail_picture = detail_info.append("img");


var date_domain = [];

var domain = {};
var nodes = [];

var max_comments = 0;
var max_likes = 0;

/* For resize */
var datas = [];

var firstrun = true;
function call_treemap(text, width, height){
    d3.selectAll(".node").remove();

    for(var i = 0 ; i < 7; i++){
        call_subtreemap(i, text, width, height);
    }
    firstrun = false;
}

function call_subtreemap(i, text, width, height){
    var treemap_width = width;
    var treemap_height = height;
    var default_between_margin = treemap_width/1000;

    var callback = function(error, root) {
        console.log("callback" + treemap_width);

        if (error) throw error;

        datas.push(root);

        //Treemap setting
        var treemap = d3.layout.treemap()
            .size([treemap_width/7 - default_between_margin, treemap_height])
            .sticky(false)
            .value(function(d) {

                return d.size;
            });



        //Add div in parent_div
        var div = parent_div.append("div")
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

        /*
         var color = d3.scale.ordinal()
         .domain(domain)
         .range(range);
         */

        var node = div.datum(root).selectAll(".node")
            .data(treemap.nodes)
            .enter().append("div")
            .attr("class", function(d){
                return "node";
            })//"node"
            .call(position)
            .style("background-color", function(d) {
                /*
                 if(d.type == 'date')
                 return color(d.name);
                 else
                 return null;
                 */
                return "#D3D3D3"
            })
            .on("mouseover", function(d){
                //Detail Information
                //console.log(d.picture_url);
                detail_picture.attr("src", d.picture_url);
                detail_img.attr("src", d.author_img_url);
                detail_author.text(d.author + "\n" + d.created_time);
                detail_message.text(d.message);


                //Color Date
                var date = new Date(d.created_time);

                for(var index in barchart_x_list){
                    var val = new Date(barchart_x_list[index]);
                    //console.log(val);
                    var day = val.getDate();
                    var time = val.getHours();
                    var class_name = '.' + day + '-' + time;


                    if(day == date.getDate() && time <= date.getHours() && date.getHours() < (time+1)){
                        $(class_name).css("fill", "brown");
                    }
                    else if(day == date.getDate() && date.getHours() == 24){
                        class_name = '.' + day + '-' + 23;
                        $(class_name).css("fill", "brown");
                    }
                    else{
                        $(class_name).css("fill", "steelblue");

                    }

                }
            }).on("mouseenter", function(d){

                //this.css("background-color", "brown");
            }).on("mouseout", function(d, i){

                //$('.' + d.text + "_text").css("fill", prev_color[d.text]);
            });

        nodes.push(node);
        //add date in div
        /*
         node.append("div")
         .attr("class", "node_text")
         .text(function(d) {

         return d.type == 'date'?  d.name : null;

         });
         */
    }

    if(firstrun){
        d3.json("/treemap_data?days=" + i + '&key_word=' + text, callback);

    }
    else{

        callback(false, datas[i])
    }

}

var color;




d3.json("/treemap_domain", function(error, domain){
    var range = domain.map(function(){  return randomColor(); })
    color = d3.scale.ordinal()
        .domain(domain)
        .range(range);
});


d3.selectAll("input").on("change", function change() {
    var popular_color = d3.scale.linear().range(['#D3D3D3','#000000']).domain([0, 500]);
    console.log(max_comments);
    var type = this.value;

    console.log(this.value);

    //check
    for(var i in nodes){
        //console.log(nodes[i]);
        nodes[i].transition()
            .duration(500).style("background-color", function(d) {
                if(d.type == type) {
                    return color(d.name);
                }
                else if('nothing' == type){
                    return "#D3D3D3";
                }
                else if('popularity' == type){
                    if(d.type == 'type'){

                        //console.log(popular_color(d.comments));
                        return popular_color(d.comments);
                    }

                    return "#D3D3D3";
                }
                else if('images' == type){

                    if(d.picture_exist == '')
                        return "#D3D3D3"


                    return "#2432F0";
                }
                else if('close' == type){
                    return "#D3D3D3";
                }
                else
                    return null;
            }).text(function(d) {
                return d.type == type?  d.name : null;
            });
    }

});