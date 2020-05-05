async function init() {
	const requestResult = await axios.get("/static/agglomerative_0.25_ward_keyword_skipgram_clusters.json");
	//const requestResult = await axios.get("{{ url_for('static', filename='agglomerative_0.25_ward_keyword_skipgram_clusters.json') }}");

	//console.log(requestResult.data);

	drawClusterGraph(requestResult.data, 600, 600);
}

function drawClusterGraph(data, fullWidth, fullHeight) {
	
	//var ctx = document.getElementById('myChart');
	//var currentChart;
	const margin = { top: 20, bottom: 40, left: 50, right: 20 };
    const width = fullWidth - margin.left - margin.right;
    const height = fullHeight - margin.top - margin.bottom;

	const svg = d3.select("#graph").append("svg")
		.attr('width', fullWidth)
		.attr('height', fullHeight)
		.append('g')
		.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	//var colorScale = ['orange', 'lightblue', '#B19CD9'];

	var firstQuestion = Object.keys(data)[0];

	console.log("First, setup the chart elements");
	console.log(data);

	//console.log("Add select menus...");
	//var select = document.createElement('select');
	//select.id = 'clusters';

	//var select_alg = document.createElement('select');
	//select_alg.id = 'algorithm';

	//for (const val in data) {
	//	var option = document.createElement('option');
	//	option.val = val;
	//	option.text = val;
	//	select.appendChild(option);
	//}

	var dropdownQuestionChange = function() {
		//if(currentChart) {
		//	currentChart.destroy();
		//}

		var questionid = d3.select(this).property('value');
		console.log(data[questionid]);
		console.log("Clusters for Question " + questionid);
		updateNodes(data[questionid]);
	};

	//select.onchange = clusterDropDownChange;

	//document.getElementById('select-area').appendChild(select);

	console.log("The first question is " + firstQuestion);

	// Process the data
	console.log("Next, process the data into data format");

	let queriesByCluster = {};
	let nodes = [];
	let colorRange = ['red', 'yellow', 'green', 'blue', 'purple'];

    let colorScale = d3.scaleLinear().domain([0, nodes.length]).range(colorRange);

    // create a tooltip
	var Tooltip = d3.select("#graph")
	    .append("div")
	    .style("opacity", 0)
	    .attr("class", "tooltip")
	    .style("padding", "5px");

	// Three function that change the tooltip when user hover / move / leave a cell
	var mouseover = function(d) {
	    Tooltip
	      .style("opacity", 1)
	    d3.select(this)
	      .style("stroke", colorScale(d.category))
	      .style("stroke-width", 5)
	      .style("opacity", 1)
	};
	var mousemove = function(d) {
	    Tooltip
	      .html(d.query)
	      .style("left", (d3.mouse(this)[0]+100) + "px")
	      .style("top", (d3.mouse(this)[1]+50) + "px")
	};
	var mouseleave = function(d) {
	    Tooltip
	      .style("opacity", 0)
	    d3.select(this)
	      .style("stroke", "none")
	      .style("opacity", 0.8)
	};
	var mouseclick = function(d) {
		console.log("Clicked " + d);
		let sidebar = document.getElementById('allcluster');
		sidebar.innerHTML = '';
		let numQueries = document.createTextNode("Cluster " + d.category + " has " + queriesByCluster[d.category].length + " queries");
		sidebar.appendChild(numQueries);
		console.log(queriesByCluster);
		for(let q of queriesByCluster[d.category]) {
			console.log(q);
			let card = document.createElement('div');
			card.className = 'cards';
			let content = document.createTextNode(q);
			card.appendChild(content);
			sidebar.appendChild(card);
		}
	}

	let simulation = d3.forceSimulation(nodes)
	  .force('charge', d3.forceManyBody().strength(2))
	  .force('center', d3.forceCenter(width/2, height/2))
	  .force('collision', d3.forceCollide().radius(function(d) {
	    return d.radius;
	  }))
	  .on('tick', ticked);

	function ticked() {
	  var u = d3.select('svg g')
	    .selectAll('circle')
	    .data(nodes);
	   console.log("Current nodes: " + nodes);

	  //u.exit().transition().attr("r", 0).remove();
	  u.exit().remove();
	  u.enter()
	    .append('circle')
	    .attr('r', function(d) {
	      return d.radius;
	    })
	    .style('fill', function(d) {
	      return colorScale(d.category);
	    })
	    .merge(u)
	    .attr('cx', function(d) {
	      return d.x;
	    })
	    .attr('cy', function(d) {
	      return d.y;
	    })
	    .on("mouseover", mouseover)
	    .on("mousemove", mousemove)
	    .on("mouseleave", mouseleave)
	    .on("click", mouseclick);

	}

	let updateNodes = function(data) {
		nodes = [];

		queriesByCluster = {};

		for (let i in data) {
			// make list of queries
			const queryList = data[i].map(x => x['query'][1]);
			queriesByCluster[i] = queryList;
			console.log(i + ": " + queryList);

			nodes.push({'radius': queryList.length * 3, 'category': i, 'query': queryList[0]});
		}
		// make color scale
		colorScale = d3.scaleLinear().domain([0, nodes.length]).range(colorRange);


		simulation.nodes(nodes);
	  	simulation.alpha(1).restart();
	}

	

	

	//var colorRange = ['#C0D9CC', '#F6F6F4', '#925D60', '#B74F55', '#969943'];
    //var colorRange = ["#5E4FA2", "#FDAE61", "#ABDDA4", "#E6F598", "#66C2A5", "#9E0142"];  
    	//console.log(nodes);
	//console.log(colorScale);
	//let nodes = data[firstQuestion];
	//console.log("Nodes: " + nodes);
	

	var question_list = Object.keys(data);
	var dropdown_question = d3.select("#graph")
        .insert("select", "svg")
        .on("change", dropdownQuestionChange);

    dropdown_question.selectAll("option")
        .data(question_list)
      .enter().append("option")
        .attr("value", function (d) { return d; })
        .text(function (d) {
            return d[0].toUpperCase() + d.slice(1,d.length); // capitalize 1st letter
        });

    updateNodes(data[firstQuestion]);

}

document.onload = init();
