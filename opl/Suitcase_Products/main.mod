// In this example we will:
// * solve a model with several data files in sequence
// * measure solving time
// * dump output onto a file

main {
	// Load files
  	var src = new IloOplModelSource("model.mod");
	var def = new IloOplModelDefinition(src);
	var cplex = new IloCplex();
	cplex.epgap = 0.01;
	cplex.tilim = 60 * 20;
	
	var dataset = "uniform"
  
  	var out = new IloOplOutputFile("output.csv");
  	
  	out.writeln("instance,price,weight,time")
  	
  	//var path = "./" + dataset;
  	var path = "./instances";
    var inDir = new IloOplFile(path);
  	var inFile = inDir.getFirstFileName();
  	var i=0;
  	while ( inFile != null ) {
  	  	if (inFile == ".DS_Store") {
  	  	  inFile = inDir.getNextFileName();
  	  	  continue;
  	  	}
  	  	writeln("Processing instance: " + inFile);

		var model = new IloOplModel(def,cplex);
		var data = new IloOplDataSource("./instances/" + inFile);
		
		model.addDataSource(data);
		
		var start = new Date();
		
		model.generate();
		
		out.write(inFile, ",");
		if (cplex.solve()) {
		  out.write(cplex.getObjValue() + ",");
		  var weight = 0;
		  for (var c=1;c<=model.n;c++) {
		    if (model.x_i[c] == 1) {
		      weight += model.w[c];
		    }
		  }
		  out.write(weight + ",");
		} else {
		  out.write("timeout, timeout,");
		}
		
		var end = new Date();
		
		var startTime = start.getTime();
	  	var endTime = end.getTime();
	  	out.writeln(endTime - startTime);
		
		
      	inFile = inDir.getNextFileName();
      	i++;
    }
	
};
