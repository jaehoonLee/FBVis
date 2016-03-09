/**
 * Created by jaehoonlee88 on 16. 3. 1..
 */
// ================== Tree map definition =====================
var color = d3.scale.category20c();

var treemap = d3.layout.treemap()
    .size([width, height])
    .sticky(false)
    .value(function(d) { return d.size; });

var color_code = d3.select(".infovis").append("div")
    .style("position", "relative")
    .style("left", margin.left + "px");

var div = d3.select(".infovis").append("div")
    .style("position", "relative")
    .style("width", (width + margin.left + margin.right) + "px")
    .style("height", (height + margin.top + margin.bottom) + "px")
    .style("left", margin.left + "px")
    .style("top", margin.top + "px");


function call_treemap(text){
    d3.selectAll(".node").remove();

    var count = 0;

    d3.json("/treemap_data?key_word=" + text, function(error, root) {
        var date_domain = root['children'].map(function(d){ return d['name']});


        root['children'].forEach(function(d){
            domain[d['name']] = true;
            d['children'].forEach(function(d){
                domain[d['name']] = true;
                d['children'].forEach(function(d){
                    domain[d['name']] = true;
                    count = count + 1;
                });
            });
        });

        //console.log("count:" + count);
        domain = Object.keys(domain);
        var range = domain.map(function(){  return randomColor(); })

        var color = d3.scale.ordinal()
            .domain(domain)
            .range(range);


        if (error) throw error;

        //Color Code==========
        /*
         var color_code_div = color_code.selectAll("div")
         .data(date_domain)
         .enter()
         .append("div")
         .style("position", "relative")
         .style("width", 300 + 'px')
         .style("height", 10 + 'px')
         .style("margin-top", 5 + 'px');


         color_code_div.append("div")
         .style("position", "relative")
         .style("top", 0 + 'px')
         .style("width", 50 + 'px')
         .style("height", 10 + 'px')

         .style("background-color", function(d){
         return color(d)
         })

         color_code_div.append("div")
         .style("position", "relative")
         .style("left", 60 + 'px')
         .style("top", -15 + 'px')
         .style("width", 100 + 'px')
         .style("height", 10 + 'px')
         .text(function(d) {
         return d;
         });
         */

        //Mouse Over
        node = div.datum(root).selectAll(".node")
            .data(treemap.nodes)
            .enter().append("div")
            .attr("class", function(d){
                return "node";
            })//"node"
            .call(position)
            .style("background-color", function(d) {
                /*
                 if(d.type == 'type')
                 return color(d.name);
                 else if(d.type == 'date')
                 return color(d.name);
                 else
                 return null;
                 */

                if(d.type == 'date')
                    return color(d.name);
                else
                    return null;

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
                        console.log("data:" + day + "," + time + ":" + date.getDate() + "," + date.getHours() );
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


        /*
         .style("opacity", function(d){
         if(d.type == 'type')
         return 0.15;
         else
         return null;
         })
         */
        node.append("div")
            .attr("class", "node_text")
            .text(function(d) {

                return d.type == 'date'?  d.name : null;

            });



        d3.selectAll("input").on("change", function change() {

            var type = this.value;
            console.log(this.value == 'type');

            //check
            node.transition()
                .duration(500).style("background-color", function(d) {
                    if(d.type == type) {

                        return color(d.name);

                    }
                    else
                        return null;
                }).text(function(d) {
                    return d.type == type?  d.name : null;
                });


            /*
             var value = this.value === "count"
             ? function() { return 1; }
             : function(d) { return d.size; };


             node.data(treemap.value(value).nodes)
             .transition()
             .duration(1500)
             .call(position);
             */
        });



    });
}