var word_fixed = false;
var selected = null;

var fill = d3.scale.category20().range();
var fill_check = []
for(var i in fill){
    fill_check.push(false);
}

var selected_word = [];
var selected_color = [];

/**
 * Color Selection For Word in World Cloud.
 */
function pick_color(){
    for(var i=0; i < 20; i++){
        if(fill_check[i] == false){
            fill_check[i] = true;
            return fill[i];
        }
    }
    return fill[0];
}

function reset_color(color_code){
    for(var i=0; i < 20; i++){
        if(fill[i] == color_code){
            fill_check[i] = false;
            return;
        }
    }
}

function call_world_cloud(width, height, eng_words, not_eng_words) {
    var expand_coefficient = 3.0;
    var eng_layout = d3.layout.cloud()
        .size([width, 500])
        .words(eng_words)
        .padding(5)
        .rotate(function () {
            return ~~(Math.random() * 2) * 90;
        })
        .font("Impact")
        .fontSize(function (d) {
            return d.size*expand_coefficient;
        })
        .on("end", draw_eng);

    var non_eng_layout = d3.layout.cloud()
        .size([width, 500])
        .words(not_eng_words)
        .padding(5)
        .rotate(function () {
            return ~~(Math.random() * 2) * 90;
        })
        .font("Impact")
        .fontSize(function (d) {
            return d.size*expand_coefficient;
        })
        .on("end", non_draw_eng);

    eng_layout.start();
    non_eng_layout.start();

    function draw_eng(words) {
        draw(words)
    }

    function non_draw_eng(words) {
        draw(words)
    }

    function draw(words) {

        var word_cloud_svg = d3.select(".infovis").append("svg")
            .attr("class", "wordcloud_svg")
            .attr("width", width)
            .attr("height", height);

        word_cloud_svg.append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function (d) {
                return d.size + "px";
            })
            .style("font-family", "Impact")
            .style("fill", function (d, i) {
                return '#000000';//fill(i);
            })
            .attr("text-anchor", "middle")
            .attr("transform", function (d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";

            })
            .on("mouseenter", function (d) {
                reset_famous_people();
                if (cur_treenode_type == 'popularity_size' || cur_treenode_type == 'nothing') {
                    var cur_color = d3.select(this).style("fill");

                    //Make Color Darker
                    var next_color = d3.rgb(cur_color).darker(0.8);
                    next_color = '#DBA901';

                    d3.select(this).style("fill", next_color);
                    wordcloud_treemap_call(d.text, next_color);

                    //word_cloud_tip.show(d, word[0][d.index]);
                }
            })
            .on("mouseout", function (d) {
                if (cur_treenode_type == 'popularity_size' || cur_treenode_type == 'nothing') {
                    var next_color = '#000000';

                    if($.inArray(d.text, selected_word) == -1) {
                        d3.select(this).style("fill", next_color);
                        console.log(selected_word, selected_color);
                        reset_wordcloud_treemap(d.text, selected_word, selected_color);
                        //wordcloud_treemap_call(d.text, "#D3D3D3");

                    }
                    else {
                        var sel_color = selected_color[$.inArray(d.text, selected_word)];
                        d3.select(this).style("fill", sel_color);
                        wordcloud_treemap_call(d.text, sel_color);
                    }
                }

            })
            .on("click", function (d) {

                //UnClick
                if($.inArray(d.text, selected_word) > -1){
                    //selected_word.push(d.text);
                    reset_color($.inArray(d.text, selected_word));
                    selected_color.splice($.inArray(d.text, selected_word), 1);
                    selected_word.splice($.inArray(d.text, selected_word), 1);
                    d3.select(this).style("fill", '#000000');
                }
                else{ //Click
                    var sel_color = pick_color();
                    d3.select(this).style("fill", sel_color);
                    selected_word.push(d.text);
                    selected_color.push(sel_color);
                    wordcloud_treemap_call(d.text, sel_color);
                }

            })
            .text(function (d) {
                return d.text;
            });
    }
}





function reset_word_cloud(){
    if (word_fixed) {
        var cur_color = selected.style("fill");
        var next_color = d3.rgb(cur_color).brighter(0.8);
        selected.style("fill", next_color);

        reset_wordcloud_treemap();
    }
    word_fixed = false;

}