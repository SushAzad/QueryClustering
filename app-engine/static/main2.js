async function init() {
	await fetchAndDraw('agglomerative');
}

async function fetchAndDraw(mode, n_clusters, dist, link, embedding) {
	//const requestResult = await axios.get("getClusters?name=" + mode);
	console.log(mode, n_clusters, dist, link, embedding)

	let url = "getClusters?name=" + mode;
	if (mode == 'kmeans' && n_clusters) {
		url += "&n_clusters=" + n_clusters;
	}
	if (mode == 'agglomerative') {
		console.log(link);
		if (dist != undefined) {
			url += "&dist=" + dist;
		}
		if (link != undefined) {
			url += "&link=" + link;
		}
	}

	//@embedding changes @sush, plus i added the parameter
	if (embedding != undefined) {
		url += "&emb_type=" + embedding;
	}

	console.log(url);
	const requestResult = await axios.get(url);
	//const requestResult = await axios.get('agglomerative_0.25_ward_keyword_skipgram_clusters.json');

	console.log("Got data");
	//console.log(requestResult.data);

	drawClusterGraph(requestResult.data, mode, 600, 600);
	let opt = document.getElementById('options');
	opt.innerHTML = '';
	if (mode == 'kmeans') {
		let label = document.createElement('label');
		label.innerHTML = 'Num of Clusters: ';
		label.for = 'n_clusters';
		let input = document.createElement('input');
		input.id = 'n_clusters';
		input.name = 'n_clusters';
		input.type = "number";
		if (n_clusters) {
			input.value = n_clusters;
		}
		input.addEventListener("keyup", function(e) {
			let box = document.getElementById('n_clusters').value;
			if (e.keyCode === 13) {
				// Enter key
				e.preventDefault();
				console.log(box);
				fetchAndDraw(mode, box);
			}
		});
		opt.appendChild(label);
		opt.appendChild(input);
	} else if (mode == 'agglomerative') {
		// dist options
		let label = document.createElement('label');
		label.innerHTML = 'Distance: ';
		label.for = 'dist';
		let input = document.createElement('input');
		input.id = 'dist';
		input.name = 'dist';
		input.type = "number";
		input.min = 0;
		input.step = 'any';
		if (dist != undefined) {
			input.value = dist;
		}
		input.addEventListener("keyup", function(e) {
			let box = document.getElementById('dist').value;
			if (e.keyCode === 13) {
				// Enter key
				e.preventDefault();
				let link = document.getElementById('link').value;
				//console.log(box, link);

				//sush @embedding changes here 
				if (link != undefined) {
					fetchAndDraw(mode, undefined, box, link, embedding);
				} else {
					//fetchAndDraw(mode, undefined, box);
					fetchAndDraw(mode, undefined, box, undefined, embedding);
				}
			}
		});
		opt.appendChild(label);
		opt.appendChild(input);

		// link options
		let label2 = document.createElement('label');
		label2.innerHTML = 'Link: ';
		label2.for = 'link';
		let input2 = document.createElement('select');
		input2.id = 'link';
		input2.name = 'link';
		
		let options = ['ward', 'complete', 'single', 'average'];
		for (const val of options) {
			var option = document.createElement('option');
			option.value = val;
			option.text = val;
			if (link == val) {
				option.selected = 'true';
			}
			input2.appendChild(option);
		}

		input2.onchange = function () {
			let param = document.getElementById('link').value;
			//let param = elem.options[elem.selectedIndex].text;
			//console.log(param, dist);
			let dist = document.getElementById('dist').value;
			//sush @embedding changes here
			if (dist != undefined) {
				fetchAndDraw(mode, undefined, dist, param, embedding);
			} else {
				fetchAndDraw(mode, undefined, undefined, param, embedding);
			}
		}
		opt.appendChild(label2);
		opt.appendChild(input2);
	}
}

function drawClusterGraph(data, mode, fullWidth, fullHeight) {
	
	document.getElementById('graph').innerHTML = '';
	document.getElementById('main_menu').innerHTML = '';
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
		//console.log(data[questionid]);
		console.log("Clusters for Question " + questionid);
		updateNodes(data[questionid]);
	};

	var dropdownModeChange = function() {
		//if(currentChart) {
		//	currentChart.destroy();
		//}

		var mode = d3.select(this).property('value');
		var emb = d3.select('#embedding_dropdown').property('value');
		
		console.log(mode);

		fetchAndDraw(mode, undefined, undefined, undefined, emb);
		//console.log(data[questionid]);
		//console.log("Clusters for Question " + questionid);
		//updateNodes(data[questionid]);
	};

	var embedding_change = function() {
		//@embedding change 
		//@sush


		var emb = d3.select(this).property('value');
		var mode = d3.select('#mode_dropdown').property('value');
		console.log(emb, mode);

		// fetchAndDraw(mode);
		fetchAndDraw(mode, undefined, undefined, undefined, emb);

	}

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
		let numQueries = document.createTextNode("Cluster " + d.category + " has " + queriesByCluster[d.category].length + " querie(s)");
		sidebar.appendChild(numQueries);
		//console.log(queriesByCluster);
		for(let q of queriesByCluster[d.category]) {
			//console.log(q);
			let card = document.createElement('div');
			card.className = 'cards';
			let content = document.createTextNode(q);
			card.appendChild(content);
			sidebar.appendChild(card);
		}
	}

	let simulation = d3.forceSimulation(nodes)
	  .force('charge', d3.forceManyBody().strength(5))
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
	   		//console.log(d.radius);
	      return d.radius;
	    })
	    .style('fill', function(d) {
	      return colorScale(d.category);
	    })
	    .merge(u)
	    .attr('cx', function(d) {
	      return d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
	    })
	    .attr('cy', function(d) {
	      return Math.max(d.radius, Math.min(height - d.radius, d.y));
	    })
	    .on("mouseover", mouseover)
	    .on("mousemove", mousemove)
	    .on("mouseleave", mouseleave)
	    .on("click", mouseclick);

	    u.transition()
		    .duration(0.5)
		    .attr('r', function(d) {
		   		//console.log(d.radius);
		      return d.radius;
		    })
		    .attr('cx', function(d) {
		      return d.x = Math.max(d.radius, Math.min(width - d.radius, d.x));
		    })
		    .attr('cy', function(d) {
		      return Math.max(d.radius, Math.min(height - d.radius, d.y));
		    })
		    .style('fill', function(d) {
		      return colorScale(d.category);
		    })
	    //.on("mouseover", mouseover)
	    //.on("mousemove", mousemove)
	    //.on("mouseleave", mouseleave);

	}

	

	let updateNodes = function(data) {
		nodes = [];
		simulation.nodes(nodes);
	  	simulation.alpha(1).restart();

		queriesByCluster = {};

		for (let i in data) {
			// make list of queries
			const queryList = data[i].map(x => x['query']);
			queriesByCluster[i] = queryList;
			//console.log(i + ": " + queryList);

			nodes.push({'radius': Math.sqrt(queryList.length * 100), 'category': i, 'query': queryList[0]});
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

	updateNodes(data[firstQuestion]);
	

	var question_list = Object.keys(data);
	var dropdown_question = d3.select("#main_menu")
        .insert("select", "svg")
        .attr("id", "question_dropdown")
        .on("change", dropdownQuestionChange);

    dropdown_question.selectAll("option")
        .data(question_list)
      .enter().append("option")
        .attr("value", function (d) { return d; })
        .text(function (d) {
            return d[0].toUpperCase() + d.slice(1,d.length); // capitalize 1st letter
        });

    var dropdown_mode = d3.select("#main_menu")
        .insert("select", "svg")
        .attr("id", "mode_dropdown")
        .on("change", dropdownModeChange);

    var mode_list = ['agglomerative', 'kmeans', 'mean_shift'];
    dropdown_mode.selectAll("option")
        .data(mode_list)
      .enter().append("option")
        .attr("value", function (d) { return d; })
        .text(function (d) {
            return d[0].toUpperCase() + d.slice(1,d.length); // capitalize 1st letter
        }).each(function(d) {
        	let elem = d3.select(this).property('value');
        	if (elem == mode) {
        		d3.select(this).attr("selected", function (d) { return true; });
        	}
        });


        // @embedding changes @sush 
		    // the next two chunks 
		    var dropdown_emb = d3.select("#main_menu")
		      .insert("select", "svg")
		      .attr("id", "embedding_dropdown")
		      .on("change", embedding_change);


		    var emb_list=['embedding', 'raw_embedding', 'key_embedding']
			  dropdown_emb.selectAll("option")
			      .data(emb_list)
			    .enter().append("option")
			      .attr("value", function (d) { return d; })
			      .text(function (d) {
			          return d[0].toUpperCase() + d.slice(1,d.length); // capitalize 1st letter
			      }).each(function(d) {
			      	let elem = d3.select(this).property('value');
			      	if (elem == mode) {
			      		d3.select(this).attr("selected", function (d) { return true; });
			      	}
			      });

}

document.onload = init();
