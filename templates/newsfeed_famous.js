/**
 * Created by jaehoonlee88 on 16. 3. 3..
 */


d3.json("/famous_data/", function(error, data){
    if (error) throw error;

    var x = d3.scale.linear()
        .domain([0, d3.max(data, function(d){ return d.active })]);

    data.forEach(function(d, i){

        //console.log(i);
        var famous_sub_div = d3.select(".famous").append("div")
            .attr("class", "ui grid")
            .style("width", "100%")
            .style("padding-top", "0px")
            .style("padding-bottom", "0px")

            //.style("margin-bottom", "0.2em");

        var famous_image_div = famous_sub_div.append("div")
            .attr("class", "two wide column")
            .style("padding-top", "0px")
            .style("padding-bottom", "0px")

        var famous_sub_sub_div = famous_sub_div.append("div")
            .attr("class", "fourteen wide column famous_sub_sub")
            .style("padding-top", "0px")
            .style("padding-bottom", "0px")
            //.style("margin-left", "20px")
            //.style("margin-top", "5px");

        var width = $('.famous_sub_sub').width();

        if(i == 0){
            x.range([0, width]);
        }

        var famous_img = famous_image_div.append("img")
            .attr("width", 50 + 'px')
            .attr("height", 50 + 'px')
            .attr("src", d.profile_url)

        var famous_author = famous_sub_sub_div
            .append("div")
            .attr("class", "row")
            .append("label")
            .style("width", (famous_sub_div.style("width") - 70) + "px")
            .attr("class", "detail_text")
            .text(d.name);

        famous_sub_sub_div
            .append("div")
            .attr("class", "row")
            .append("svg")
            .attr("width", width)
            .attr("height", "10")
            .append('g')
            .append("rect")
            .attr("fill", "#aec7e8")
            .attr("class", "famous_bar")
            .attr("width", x(d.active))
            .attr("height", "10");


    });



});

