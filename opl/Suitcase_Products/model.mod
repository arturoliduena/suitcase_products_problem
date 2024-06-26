int       x = ...;  // Height   of the suitcase.
int       y = ...;  // Width    of the suitcase.
int       c = ...;  // Capacity of the suitcase.

int       n = ...;  // Number  of     products.
int p[1..n] = ...;  // Prices  of the products.
int w[1..n] = ...;  // Weights of the products.
int s[1..n] = ...;  // Sides   of the boxes of the products.
 
dvar boolean x_i[i in 1..n];
dvar int point[i in 1..n, j in 1..2];
dvar int z;
 
// Objective 
maximize z; 

subject to{
 // Weight Constraint
 // Weight of all selected items must be equal or smaller to capacity
 sum(i in 1..n) x_i[i] * w[i] <= c;
     
 // Dimensional Constraints
 forall(i in 1..n) {
 	x_i[i] == 1 => 0 <= point[i, 1] <= x - s[i];
 	x_i[i] == 1 => 0 <= point[i, 2] <= y - s[i];
 	
 	x_i[i] == 0 => point[i, 1] == -1 && point[i, 2] == -1;
 }
 
 // collision detection
 forall(i in 1..n, j in i+1..n) {
     x_i[i] == 1 && x_i[j] == 1 => 
     	point[i, 1] >= point[j, 1] + s[i] || 
     	point[i, 1] + s[i] <= point[j, 1] ||
     	point[i, 2] >= point[j, 2] + s[i] || 
     	point[i, 2] + s[i] <= point[j, 2];
 }
 
 // Price time product
 // z is the sum of prices of all selected items
 sum(i in 1..n) x_i[i] * p[i] == z;
}

// Define the output function to print the results
execute {
	writeln("Optimal value (z): ", z);
	writeln("Selected items and their positions:");
	
	for (var i = 1; i <= n; i++) {
		if (x_i[i] == 1) {
			writeln("Item ", i, ":");
			writeln("  Price: ", p[i]);
			writeln("  Weight: ", w[i]);
			writeln("  Side length: ", s[i]);
			writeln("  Position: (", point[i][1], ", ", point[i][2], ")");
		}
	}
}