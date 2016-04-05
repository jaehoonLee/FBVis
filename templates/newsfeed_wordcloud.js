function call_world_cloud(width, height, words){
    var fill = d3.scale.category20();

    var layout = d3.layout.cloud()
        .size([width, 500])
        .words(words)
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font("Impact")
        .fontSize(function(d) { return d.size; })
        .on("end", draw);
    /*

     */

    layout.start();

    function draw(words) {
        var fixed = false;
        var selected = null;
        d3.select(".infovis").append("svg")
            .attr("class", "wordcloud_svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i); })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";

            })
            .on("mouseenter", function(d){
                if(!fixed && (cur_treenode_type == 'popularity_size' || cur_treenode_type == 'nothing')){
                    var cur_color = d3.select(this).style("fill");
                    var next_color = d3.rgb(cur_color).darker(0.8);

                    d3.select(this).style("fill", next_color);

                    wordcloud_treemap_call(d.text, cur_color);
                }
            })
            .on("mouseout", function(d){
                if(!fixed && (cur_treenode_type == 'popularity_size' || cur_treenode_type == 'nothing')) {
                    var cur_color = d3.select(this).style("fill");
                    var next_color = d3.rgb(cur_color).brighter(0.8);

                    d3.select(this).style("fill", next_color);
                }
            })
            .on("click", function(d){
                if(fixed){
                    if(d3.select(this).text() != selected.text() && selected != null){
                        var cur_color = selected.style("fill");
                        var next_color = d3.rgb(cur_color).brighter(0.8);

                        selected.style("fill", next_color);
                    }
                }

                fixed = !fixed;
                selected = d3.select(this);
            })
            .text(function(d) { return d.text; });
    }

}

