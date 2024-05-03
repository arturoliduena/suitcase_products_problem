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
 //Weight Constraint
 sum(i in 1..n) x_i[i] * w[i] <= c;
     
 //Dimensional Constraints
 forall(i in 1..n) {
 	x_i[i] == 1 => 0 <= point[i, 1] <= x - s[i];
 	x_i[i] == 1 => 0 <= point[i, 2] <= y - s[i];
 	
 	x_i[i] == 0 => point[i, 1] == -1 && point[i, 2] == -1;
 }
 
 forall(i in 1..n, j in 1..n) {
   if(i != j){
     x_i[i] == 1 && x_i[j] == 1 && (point[j, 1] <= point[i, 1] + s[i] && point[j, 1] >= point[i, 1]) => (point[j, 2] >= point[i, 2] + s[i] || point[j, 2] <= point[i, 2]);
     x_i[i] == 1 && x_i[j] == 1 && (point[j, 2] <= point[i, 2] + s[i] && point[j, 2] >= point[i, 2]) => (point[j, 1] >= point[i, 1] + s[i] || point[j, 1] <= point[i, 1]);
   }
 }
 
 //price time product
 sum(i in 1..n) x_i[i] * p[i] == z;
}