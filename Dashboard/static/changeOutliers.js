function changeBins(da,str)
{
	d3.select("#slid").on("mousedown",function(){
	var slider = document.getElementById("der"); 
	//var bin = document.getElementById("demo"); 
	//bin.innerHTML=slider.value;
	slider.oninput = function() { 
		
 		//bin.innerHTML = (parseInt(this.value)); 
 		var num_bins=30-parseInt(slider.value);
		hist(da,str,num_bins);
} 
})
}