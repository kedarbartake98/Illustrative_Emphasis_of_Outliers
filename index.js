
function send_data_1(url,label) {
    $.ajax({
    type: 'GET',
    url: url,
      contentType: 'application/json; charset=utf-8',
    xhrFields: {
    withCredentials: false
    },
    headers: {

    },

    success: function(reply) {
        draw_scattplot(reply, label);
    },
    error: function(reply) {
    $("#chart_container").html(reply);
    }
  });
}

function resetEverything() {
     d3.selectAll('.svgid').remove();
}



function draw_scattplot(reply,label)
{
  //console.log(label)
  //console.log(reply)

  d3.selectAll('.svgid').remove();
    var data = JSON.parse(reply);
    var obj= [];
    columns = Object.keys(data);

    for(var i=0; i < Object.keys(data[0]).length; ++i){
        obj_dict = {}
        obj_dict.x = data[0][i];
        obj_dict.y = data[1][i];

        obj_dict.clusterid = data['clusterid'][i]
        obj_dict.col1 = data[columns[2]][i]
        obj_dict.col2 = data[columns[3]][i]
        obj.push(obj_dict);
        console.log(data['clusterid'][i]);

    }

    data = obj;
      //console.log(data);

    var margin = {top: 50, right: 10, bottom: 90, left: 150};
    var width = 1100 - margin.left - margin.right;
    var height = 550 - margin.top - margin.bottom;

    var xValue = function(d) { return d.x;};
    var xScale = d3.scale.linear().range([0, 800]);
    var xMap = function(d) { return xScale(xValue(d)); };
    var xAxis = d3.svg.axis().scale(xScale).orient("bottom");

    var yValue = function(d) { return d.y;};
    var yScale = d3.scale.linear().range([height, 0]);
    var yMap = function(d) { return yScale(yValue(d));};
    var yAxis = d3.svg.axis().scale(yScale).orient("left");

    var cluster_color

    if(num==0) {
        cluster_color = function(d) { return d.clusteridx;}
    } else {
        cluster_color = function(d) { return d.clusterid;}
    }
    var color = d3.scale.category10();

    var svg = d3.select("body").append("svg")
        .attr('class', 'svgid')
        .attr("width", width + margin.left + margin.right)
        .attr("height", 700)
        .append("g")
        .attr("transform", "translate(250,80)");

    var tooltip = d3.select("body").append('div').style('position','absolute');

    xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1]);
    yScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);

    xAxisLine = svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .attr("class", "x_axis")
          .call(xAxis)

    yAxisLine = svg.append("g")
          .attr("class", "y_axis")
          .call(yAxis)

    svg.append("text")
            .attr("class", "axis_label")
            .attr("text-anchor", "middle")
            .attr("transform", "translate("+ (-70) +","+(height/2)+")rotate(-90)")
            .text("Component 2");

    svg.append("text")
        .attr("class", "axis_label")
        .attr("text-anchor", "middle")
        .attr("transform", "translate("+ (880/2) +","+(620 - margin.top - margin.bottom)+")")
        .text("Component 1");

    svg.append("text")
        .attr("class", "chart_name")
        .attr("text-anchor", "middle")
        .attr("transform", "translate("+ (880/2) +","+(670 - margin.top - margin.bottom)+")")
        .text(label);

    svg.selectAll(".dot")
          .data(data)
          .enter().append("circle")
          .attr("class", "dot")
          .attr("cx", xMap)
          .attr("r", 3.5)
          .attr("cy", yMap)
          .style("fill", function(d) { return color(cluster_color(d));})
          .on("mouseover", function(d) {
              tooltip.transition().style('opacity', .9)
                .style('color','black')
                .style('font-size', '20px')
              tooltip.html(columns[2] + ":" + d.col1 + ", " + columns[3] + ":" + d.col2)
                .style("top", (d3.event.pageY - 28) + "px")
                .style("left", (d3.event.pageX + 5) + "px");
          })
          .on("mouseout", function(d) {
              tooltip.transition()
                .duration(500)
                .style("opacity", 0);
              tooltip.html('');
          });


  changeDist(sub_factor)
}


function changeDist(da,str)
{
  d3.select("#slid").on("mousedown",function(){
  var slider = document.getElementById("der"); 
  //var bin = document.getElementById("demo"); 
  //bin.innerHTML=slider.value;
  slider.oninput = function() { 
    
    //bin.innerHTML = (parseInt(this.value)); 
    var dist=parseInt(slider.value);
    send_data_1("/sendData/dist");
} 
})
}