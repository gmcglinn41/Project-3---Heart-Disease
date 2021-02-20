// Define SVG area dimensions
var svgWidth = 960;
var svgHeight = 500;

// Define the chart's margins as an object
var margin = {
    top: 10,
    right: 40,
    bottom: 110,
    left: 120
};

// Define dimensions of the chart area
var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;


// Select body, append SVG area to it, and set its dimensions.  //Append SVG element
var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

//svgGroup now refers to the "g" (group) element appended.
//The SVG group would normally be aligned to the top left edge of the chart
//Now it is offset to the right and down using the transform attribute
var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);  
     

//};
console.log("test2");   
//Read the data in - import csv data
//function getData() {
d3.csv("resources/heart.csv").then (function(data) {
 console.log("test");

 var item = {};
//format used data as numbers - parse data
data.forEach(function(record) {
    item.age = +record.age;
    item.target = +record.target;
    
});
   
//Create scale functions
var xLinearScale = d3.scaleLinear()
    .range([0, width])
    .domain([8, d3.max(data, item => parseFloat(item.age))]);
var yLinearScale = d3.scaleLinear()
    .range([height, 0])
    .domain([0, d3.max(data, item => parseFloat(item.target))]);

      

//Create axis functions

var bottomAxis = d3.axisBottom(xLinearScale);
var leftAxis = d3.axisLeft(yLinearScale);

//Append Axes to the chart
  chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

   chartGroup.append("g")
     .call(leftAxis);


// set up chart
chartGroup
.selectAll("circle")
.data(data)
.enter()
.append("circle")
.attr('r','10')
.attr("cx",item => xLinearScale(item.poverty))
.attr("cy",item => yLinearScale(item.healthcare))
.attr("fill","#3288bd")
.attr("stroke-width","1")
.attr("opacity",".5")
// Hover rules
.on("mouseover", function (d) {
    // Show the tooltip
    toolTip.show(d, this);
})
.on("mouseout", function (d) {
    // Remove the tooltip
    toolTip.hide(d);
});
});

// Create axes labels
chartGroup.append("text")
.attr("transform", "rotate(-90)")
.attr("y", 0 - margin.left + 40)
.attr("x", 0 - (svgHeight)/2)
.attr("dy", "1em")
.attr("class", "axisText")
.text("Lacks Healthcare (%)");

chartGroup.append("text")
.attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
.attr("class", "axisText")
.text("Poverty (%)");

//Initialize tool tip
var toolTip = d3.tip()
        .attr("class","d3-tip")
        .offset([40, -60])
        .html(function (d) {
            return `<div>${d.state}</div>`;
});

    
//Create tooltip in the chart
svg.call(toolTip);
  
  