/**
 * Created by jaehoonlee88 on 16. 3. 3..
 */

var full_data;
d3.json("/famous_data/", function(error, data){
    if (error) throw error;
    full_data = data;
    draw_famous(data);

});


var delete_authors = []
function refresh(index){
    console.log(full_data[index]);

    delete_authors.push(full_data[index].author_id);
    console.log(full_data[index].author_id);

    for(var i in treemap_datas){
        var authors = treemap_datas[i].children[0].children;

        for(var j in authors){
            var author = authors[j];
            if(full_data[index].name == author.name){

                authors.splice(j, 1);
                break;
            }
        }


        //console.log(authors);
    }

    $.ajax({
        type : "POST",
        data : {'delete_authors':delete_authors},
        url : "/filtered_word_cloud_data/1/",
        success: function(cloud_words_data){
            eng_cloud_words = JSON.parse(cloud_words_data);

            $.ajax({
                type : "POST",
                data : {'delete_authors':delete_authors},
                url : "/filtered_word_cloud_data/0/",
                success: function(cloud_words_data){
                    not_eng_cloud_words = JSON.parse(cloud_words_data);

                    $.ajax({
                        type : "POST",
                        data : {'delete_authors':delete_authors},
                        url : "/removed_barchart_data/",
                        success: function(barchart_removed_data_raw){
                            barchart_removed_data = JSON.parse(barchart_removed_data_raw);
                            reset_infovis();
                        }

                    });
                }
            });
        }
    });


    //




    full_data.splice(index, 1);
    d3.select(".famous").html('');
    draw_famous(full_data);
}

var people_fixed = false;
var pre_node_name = null;


function draw_famous(data){
    var x = d3.scale.linear().domain([0, d3.max(data, function(d){ return d.active })]);
    data = data.slice(0, 50);

    /*
     var famous_svg = d3.select(".famous")
     var famous_tip = d3.tip().attr('class', 'd3-tip').html("HELLO WORLD");
     famous_svg.call(famous_tip);
     */

    data.forEach(function(d, i){
        var famous_sub_div = d3.select(".famous").append("div")
            .attr("class", "ui grid")
            .style("width", "100%")
            .style("padding-top", "0px")
            .style("padding-bottom", "0px")

        var famous_image_div = famous_sub_div.append("div")
            .attr("class", "two wide column")
            .style("padding-top", "0px")
            .style("padding-bottom", "0px");

        var famous_sub_sub_div = famous_sub_div.append("div")
            .attr("class", "fourteen wide column famous_sub_sub")
            .style("padding-top", "0px")
            .style("padding-bottom", "0px")

        var width = $('.famous_sub_sub').width();

        if(i == 0){
            x.range([0, width]);
        }



        famous_image_div.append("img")
            .style("top", "0px")
            .attr("width", 50 + 'px')
            .attr("height", 50 + 'px')
            .attr("src", d.profile_url)
            .on("mouseover", function(){

                reset_word_cloud();

                if(!people_fixed){
                    var nodename = d.author_id;
                    pre_node_name = nodename;
                    $("." + nodename + "_node").css("background", "black");
                }


            })
            .on("mouseout", function(){
                if(!people_fixed) {
                    var nodename = d.author_id;
                    $("." + nodename + "_node").css("background", "#D3D3D3");
                }
            })
            .on("click", function(){
                people_fixed = !people_fixed;

            });

        famous_image_div.append("div")
            .style("position", "absolute")
            .style("top", "-10px")
            .append("input")
            .attr("type", "checkbox")
            .attr("name", "famous_remove")
            .on("change", function(){

                //CheckBox Remove Refresh
                refresh(i);
            })

        famous_sub_sub_div
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
}


function reset_famous_people(){
    if(people_fixed){
        if(pre_node_name != null){



        }
        people_fixed = false;
    }
}