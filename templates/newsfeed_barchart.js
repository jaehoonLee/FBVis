/**
 * Created by jaehoonlee88 on 16. 3. 1..
 */
// ================== Bar chart definition =====================
var weekday = new Array('Sun', 'Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat')

//=================== Bar Chart ====================
var barchart_x_list;
var firstrun_barchart = true;
var barchart_data;
var barchart_removed_data = [];
var svg = null;


function call_barchart(key_word, bar_width, bar_height){
    d3.select(".barchart_svg").remove();

    d3.selectAll(".bar").remove();
    d3.selectAll(".y").remove();
    d3.selectAll(".x").remove();

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, bar_width], .1);

    var y = d3.scale.linear()
        .range([bar_height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .tickFormat(function(d, i){

            d = new Date(d);
            var time = d.getHours();

            if(time % 3 == 0)
                return time;

            return '';
        });

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10)
        .tickSubdivide(0);


    var dateAxis = d3.svg.axis()
        .scale(y)
        .orient("right")
        .ticks(0)

    var svg = d3.select(".infovis").append("svg")
        .attr("class", "barchart_svg")
        .attr("width", bar_width + bar_margin.left + bar_margin.right)
        .attr("height", bar_height + bar_margin.top + bar_margin.bottom)
        .append("g")
        .attr("transform", "translate(" + bar_margin.left + "," + bar_margin.top + ")");


    var barchart_index = {}
    var draw_barchart_callback = function(error, data) {
        barchart_data = data;

        if (error) throw error;

        barchart_x_list = data.map(function(d) {
            return d.date; });


        for(var index in barchart_x_list){
            barchart_index[barchart_x_list[index]] = index;
        }

        x.domain(barchart_x_list);
        y.domain([0, d3.max(data, function(d) { return +d.count; })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + bar_height + ")")
            .call(xAxis);

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .attr("transform", "translate(" + 10 + ",0)")
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end");

        var weekday_y_line = new Array('Thurs', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed');
        for(var i = 0; i <= 6; i++){

            svg.append("g")
                .attr("class", "mon axis")
                .call(dateAxis)
                .attr("transform", "translate(" + (x(barchart_x_list[0]) + (x(barchart_x_list[24]) - x(barchart_x_list[0])) * i + x.rangeBand()/2) + ",0)")
                .append("text")
                .attr("y", 6)
                .attr("dy", ".71em")
                .attr("x", 5)
                .text(weekday_y_line[i]);

        }

        var bar_fixed = false;
        var total_bar = svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", function(d) {
                var date = new Date(d.date);
                return "bar " + date.getDate()+ "-"+ date.getHours(); })
            .attr("x", function(d) {
                return x(d.date); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.count); })
            .attr("height", function(d) { return bar_height - y(d.count); })
            .style("fill", "black")
            .on("click", function(d){
                bar_fixed = !bar_fixed;
            });


        if(barchart_removed_data.length == 0){
            total_bar.style("fill", "steelblue")
                .on("mouseover", function(d){
                    d3.select(this).style("fill", "brown");
                    var node_name = "." + barchart_index[d.date] + "_date_node";
                    $(node_name).css("background-color", "brown");
                })
                .on("mouseout", function(d){
                    d3.select(this).style("fill", "steelblue");
                    var node_name = "." + barchart_index[d.date] + "_date_node";
                    $(node_name).css("background-color", "#D3D3D3");

                });
        }
        else{
            svg.selectAll(".delete_people_bar")
                .data(barchart_removed_data)
                .enter().append("rect")
                .attr("class", function(d) {
                    return "delete_people_bar"; })
                .attr("x", function(d) {
                    return x(d.date); })

                .attr("width", x.rangeBand())
                .attr("y", function(d) { return y(d.count); })
                .attr("height", function(d) { return (bar_height - y(d.count)); })
                .style("fill", "steelblue")
                .style("background-color", "yellow")
                .on("mouseover", function(d) {
                    d3.select(this).style("fill", "brown");
                    var node_name = "." + barchart_index[d.date] + "_date_node";
                    $(node_name).css("background-color", "brown");
                })
                .on("mouseout", function(d) {
                    d3.select(this).style("fill", "steelblue");
                    var node_name = "." + barchart_index[d.date] + "_date_node";
                    $(node_name).css("background-color", "#D3D3D3");
                });
        }
    }

    if(firstrun_barchart){
        d3.json("/barchart_data?key_word=" + key_word, draw_barchart_callback);

        firstrun_barchart = false;

    }
    else{
        draw_barchart_callback(false, barchart_data);
    }


    function type(d) {
        d.count = +d.count;
        return d;
    }
}




