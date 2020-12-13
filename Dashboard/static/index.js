
function send()
{
  var rb = document.getElementById("samplingType");
  if(rb[0].checked)
        send_data_with("/sendwith/"+0.5)
  else
        send_data_without("/sendwithout/"+0.5)  
}
function send_data_with(url) {
  console.log(url)
$.ajax({
    type:"GET",
    url: url,
    dataType:'json',
    success: function(data){
      draw_scattplot_with(data);
    }
  })
}
function send_data_without(url) {
  console.log(url)
$.ajax({
    type:"GET",
    url: url,
    dataType:'json',
    success: function(data){
      draw_scattplot_without(data);
    }
  })
}

function resetEverything() {
     d3.selectAll('.svgid').remove();
}


function draw_scattplot_with(dataset)
{
    d3.selectAll(".svgid").remove();

    data = dataset["datapoints"]
    console.log(data)

    var margin = {top: 50, right: 10, bottom: 90, left: 300};
    width = 1100 - margin.left - margin.right;
    height = 700 - margin.top - margin.bottom;

    var xValue = function(d) {return d.A;}, // data -> value
    xScale = d3.scale.linear().range([0, width]) // value -> display
    xMap = function(d) { return xScale(xValue(d));}, // data -> display
    xAxis = d3.svg.axis().scale(xScale).orient("bottom");

// setup y
    var yValue = function(d) { return d.B;}, // data -> value
    yScale = d3.scale.linear().range([height, 0]) // value -> display
    yMap = function(d) { return yScale(yValue(d));}, // data -> display
    yAxis = d3.svg.axis().scale(yScale).orient("left");

// setup fill color
    xScale.domain([d3.min(data, xValue)-1.5, d3.max(data, xValue)+1.5]);
    yScale.domain([d3.min(data, yValue)-1.5, d3.max(data, yValue)+1.5]);
    
    var cValue = function(d) { return d.C;},
    color = d3.scale.category10();
// add the graph canvas to the body of the webpage
    var svg = d3.select("body").append("svg").attr('class','svgid')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // x-axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("X-axis");

  // y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Y-axis");

//console.log(reply);
  // draw dots
  svg.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", xMap)
      .attr("cy", yMap)
      .style("fill", function(d) { return color(cValue(d));});

  // draw legend

  changeDist_with()
}


function changeDist_with()
{
  d3.select("#slid").on("mousedown",function(){
  var slider = document.getElementById("der"); 
  //var bin = document.getElementById("demo"); 
  //bin.innerHTML=slider.value;
  slider.oninput = function() { 
    
    //bin.innerHTML = (parseInt(this.value)); 
    var dist=parseFloat(slider.value);
    console.log(typeof dist)
    send_data_with("/sendwith/"+dist);
} 
})
}
function updateTextInput(val) {
          document.getElementById('textInput').value=val; 
        }
function draw_scattplot_without(dataset)
{
    d3.selectAll(".svgid").remove();

    data = dataset["datapoints"]
    console.log(data)

    var margin = {top: 50, right: 10, bottom: 90, left: 300};
    width = 1100 - margin.left - margin.right;
    height = 700 - margin.top - margin.bottom;

    var xValue = function(d) {return d.A;}, // data -> value
    xScale = d3.scale.linear().range([0, width]) // value -> display
    xMap = function(d) { return xScale(xValue(d));}, // data -> display
    xAxis = d3.svg.axis().scale(xScale).orient("bottom");

// setup y
    var yValue = function(d) { return d.B;}, // data -> value
    yScale = d3.scale.linear().range([height, 0]) // value -> display
    yMap = function(d) { return yScale(yValue(d));}, // data -> display
    yAxis = d3.svg.axis().scale(yScale).orient("left");

// setup fill color
    xScale.domain([d3.min(data, xValue)-1.5, d3.max(data, xValue)+1.5]);
    yScale.domain([d3.min(data, yValue)-1.5, d3.max(data, yValue)+1.5]);
    
    var cValue = function(d) { return d.C;},
    color = d3.scale.category10();
// add the graph canvas to the body of the webpage
    var svg = d3.select("body").append("svg").attr('class','svgid')
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // x-axis
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("X-axis");

  // y-axis
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Y-axis");

//console.log(reply);
  // draw dots
  svg.selectAll(".dot")
      .data(data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", xMap)
      .attr("cy", yMap)
      .style("fill", function(d) { return color(cValue(d));});

  // draw legend

  changeDist_without()
}


function changeDist_without()
{
  d3.select("#slid").on("mousedown",function(){
  var slider = document.getElementById("der"); 
  //var bin = document.getElementById("demo"); 
  //bin.innerHTML=slider.value;
  slider.oninput = function() { 
    
    //bin.innerHTML = (parseInt(this.value)); 
    var dist=parseFloat(slider.value);
    console.log(typeof dist)
    send_data_without("/sendwithout/"+dist);
} 
})
}
