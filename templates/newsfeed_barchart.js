/**
 * Created by jaehoonlee88 on 16. 3. 1..
 */
// ================== Bar chart definition =====================

var weekday = new Array('Sun', 'Mon', 'Tue', 'Wed', 'Thurs', 'Fri', 'Sat')
var bar_margin = {top: 20, right: 20, bottom: 30, left: 20},
    bar_width = total_width - margin.left - margin.right,
    bar_height = height - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, bar_width], .1);

var y = d3.scale.linear()
    .range([bar_height, 0]);

var zero = d3.format("02d");
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(function(d, i){

        d = new Date(d);
        var day = d.getDay();
        var time = d.getHours();
        var date = d.getDate()

        /*
        if(time == 0){
            //return date + 'th ' + weekday[day];

            return weekday[day];

        }
        */

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
    .attr("width", bar_width + bar_margin.left + bar_margin.right)
    .attr("height", bar_height + bar_margin.top + bar_margin.bottom)
    .append("g")
    .attr("transform", "translate(" + bar_margin.left + "," + bar_margin.top + ")");


//=================== Bar Chart ====================
var barchart_x_list;
function call_barchart(key_word){
    d3.selectAll(".bar").remove();
    d3.selectAll(".y").remove();
    d3.selectAll(".x").remove();


    d3.json("/barchart_data?key_word=" + key_word, function(error, data) {
        if (error) throw error;

        barchart_x_list = data.map(function(d) {
            return d.date; });

        x.domain(barchart_x_list);
        y.domain([0, d3.max(data, function(d) { return +d.count; })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + bar_height + ")")
            .call(xAxis);
        /*
         svg.selectAll(".x text")  // select all the text elements for the xaxis
         .attr("transform", function(d) {
         return "translate(" + this.getBBox().height*-0.5 + "," + this.getBBox().height/2 + ")rotate(-55)";
         });
         */

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .attr("transform", "translate(" + 10 + ",0)")
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Count");

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


        svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", function(d) {
                var date = new Date(d.date);
                return "bar " + date.getDate()+ "-"+ date.getHours(); })
            .attr("x", function(d) {
                return x(d.date); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.count); })
            .attr("height", function(d) { return bar_height - y(d.count); });

    });
}

function type(d) {
    d.count = +d.count;
    return d;
}