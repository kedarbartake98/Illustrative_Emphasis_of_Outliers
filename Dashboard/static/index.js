
function setVal(){

    document.getElementById("der").value = "0";
    document.getElementById("Task2").value = "-1"

}
function selectType() {

    var dropdown = document.getElementById("Task2");
    var Value = dropdown.options[dropdown.selectedIndex].value;
    var rb = document.getElementById("samplingType");
    if(Value=="housing")
    {
      if(rb[0].checked)
        send_data_with("/sendwith?dataset_name=Housing&sub_factor=1.75")
  else
        send_data_without("/sendwithout?dataset_name=Housing&sub_factor=1.75")  
    }
          
    else if (Value=="air") 
        {
      if(rb[0].checked)
        send_data_with("/sendwith?dataset_name=Air&sub_factor=1.75")
  else
        send_data_without("/sendwithout?dataset_name=Air&sub_factor=1.75")  
    }
    else if(Value=="estate")
        {
      if(rb[0].checked)
        send_data_with("/sendwith?dataset_name=Estate&sub_factor=1.75")
  else
        send_data_without("/sendwithout?dataset_name=Estate&sub_factor=1.75")  
    }
    else if(Value=="cereal")
        {
      if(rb[0].checked)
        send_data_with("/sendwith?dataset_name=Cereal&sub_factor=1.75")
  else
        send_data_without("/sendwithout?dataset_name=Cereal&sub_factor=1.75")  
    }
    else if(Value=="fire")
      {
      if(rb[0].checked)
        send_data_with("/sendwith?dataset_name=Fire&sub_factor=1.75")
  else
        send_data_without("/sendwithout?dataset_name=Fire&sub_factor=1.75")  
    }
    else
    {

    }

}

function getDistType_with(Value,val) {

    if(Value=="housing")
    {
        send_data_with("/sendwith?dataset_name=Housing&sub_factor="+val) 
    }
          
    else if (Value=="air") 
       {
        send_data_with("/sendwith?dataset_name=Air&sub_factor="+val)
    }
    else if(Value=="estate")
        {
      
        send_data_with("/sendwith?dataset_name=Estate&sub_factor="+val)
  
    }
    else if(Value=="cereal")
        {
      
        send_data_with("/sendwith?dataset_name=Cereal&sub_factor="+val)
   
    }
    else if(Value=="fire")
      {
      
        send_data_with("/sendwith?dataset_name=Fire&sub_factor="+val)
   
    }
    else
    {

    }
}

function getDistType_without(Value,val) {

    if(Value=="housing")
    {
        send_data_without("/sendwithout?dataset_name=Housing&sub_factor="+val) 
    }
          
    else if (Value=="air") 
       {
        send_data_without("/sendwithout?dataset_name=Air&sub_factor="+val)
    }
    else if(Value=="estate")
        {
      
        send_data_without("/sendwithout?dataset_name=Estate&sub_factor="+val)
  
    }
    else if(Value=="cereal")
        {
      
        send_data_without("/sendwithout?dataset_name=Cereal&sub_factor="+val)
   
    }
    else if(Value=="fire")
      {
      
        send_data_without("/sendwithout?dataset_name=Fire&sub_factor="+val)
   
    }
    else
    {

    }
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

function draw_scattplot_with(dataset)
{
    d3.selectAll(".svgid").remove();

    data = dataset["datapoints"]
    console.log(data)

    var margin = {top: 50, right: 10, bottom: 90, left: 100};
    width = 1300 - margin.left - margin.right;
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
    xScale.domain([-30,30]);
    yScale.domain([-30,50]);
    
    var cValue = function(d) { return d.D;},
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
  var legend = svg.selectAll(".legend")
      .data(color.domain())
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  // draw legend colored rectangles
  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

  // draw legend text
  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d;})


  changeDist_with()
}


function changeDist_with()
{
  d3.select("#slid").on("mousedown",function(){
  var slider = document.getElementById("der"); 
  var dropdown = document.getElementById("Task2");
  var Value = dropdown.options[dropdown.selectedIndex].value;
  //var bin = document.getElementById("demo"); 
  //bin.innerHTML=slider.value;
  slider.oninput = function() { 
    
    //bin.innerHTML = (parseInt(this.value)); 
    var dist=parseFloat(slider.value);
    //console.log(typeof dist)
    if(dist == 1.75)
      val = 0.5
    else 
      val = parseFloat(1.75-dist)

    getDistType_with(Value,val);
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

    var margin = {top: 50, right: 10, bottom: 90, left: 100};
    width = 1300 - margin.left - margin.right;
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
    //xScale.domain([d3.min(data, xValue)-1.5, d3.max(data, xValue)+1.5]);
    //yScale.domain([d3.min(data, yValue)-1.5, d3.max(data, yValue)+1.5]);
    xScale.domain([-30,30]);
    yScale.domain([-30,50]);

    var cValue = function(d) { return d.D;},
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
  var legend = svg.selectAll(".legend")
      .data(color.domain())
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  // draw legend colored rectangles
  legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

  // draw legend text
  legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d;})

  changeDist_without()
}


function changeDist_without()
{
  d3.select("#slid").on("mousedown",function(){
  var slider = document.getElementById("der"); 
  var dropdown = document.getElementById("Task2");
  var Value = dropdown.options[dropdown.selectedIndex].value;
  //var bin = document.getElementById("demo"); 
  //bin.innerHTML=slider.value;
  slider.oninput = function() { 
    
    //bin.innerHTML = (parseInt(this.value)); 
    var dist=parseFloat(slider.value);
    //console.log(typeof dist)
    if(dist == 1.75)
      val = 0.5
    else 
      val = parseFloat(1.75-dist)

    getDistType_without(Value,val);
} 
})
}
