int caseWidth    = ...;  // Width    of the suitcase.
int caseHeight   = ...;  // Height   of the suitcase.
int caseCapacity = ...;  // Capacity of the suitcase.

int n            = ...;  // Number  of     products.
int price[1..n]  = ...;  // Prices  of the products.
int weight[1..n] = ...;  // Weights of the products.
int side[1..n]   = ...;  // Sides   of the boxes of the products.
 
dvar boolean x_i[i in 1..n];
dvar int point[i in 1..n, j in 1..2];
dvar int z;
 
// Objective 
maximize z; 

subject to{
 // Weight Constraint
 // Weight of all selected items must be equal or smaller to capacity
 sum(i in 1..n) x_i[i] * weight[i] <= caseCapacity;
     
 // Dimensional Constraints
 forall(i in 1..n) {
 	x_i[i] == 1 => 0 <= point[i, 1] <= caseWidth - side[i];
 	x_i[i] == 1 => 0 <= point[i, 2] <= caseHeight - side[i];
 	
 	x_i[i] == 0 => point[i, 1] == -1 && point[i, 2] == -1;
 }
 
 // collision detection
 forall(i in 1..n, j in i+1..n) {
     x_i[i] == 1 && x_i[j] == 1 => 
     	point[i, 1] >= point[j, 1] + side[i] || 
     	point[i, 1] + side[i] <= point[j, 1] ||
     	point[i, 2] >= point[j, 2] + side[i] || 
     	point[i, 2] + side[i] <= point[j, 2];
 }
 
 // Price time product
 // z is the sum of prices of all selected items
 sum(i in 1..n) x_i[i] * price[i] == z;
}