/*********************************************
 * OPL 22.1.1.0 Model
 * Author: DELL
 * Creation Date: 4 kwi 2024 at 10:14:03
 *********************************************/

int CITIES = ...;
int DEPS = ...;
range ID_CITY = 1..CITIES; 
range ID_DEP = 1..DEPS; 

float B[ID_CITY][ID_DEP] = ...; 
float C[ID_DEP][ID_DEP] = ...; 
float D[ID_CITY][ID_CITY] = ...; 

dvar boolean delta[ID_DEP][ID_CITY];
dvar boolean omega[ID_DEP][ID_CITY][ID_DEP][ID_CITY];


minimize
  sum( i in ID_DEP, j in ID_CITY )
  		-(B[j][i] * delta[i][j]) + 
  sum(i in ID_DEP, j in ID_CITY, k in ID_DEP, l in ID_CITY)
  		(C[k][i]*D[l][j]*omega[i,j,k,l]);

subject to {
  forall(i in ID_DEP) sum(j in ID_CITY)(delta[i][j])==1;
  forall(j in ID_CITY) sum(i in ID_DEP)(delta[i][j])<=3;
  
  forall(i in ID_DEP, j in ID_CITY, k in ID_DEP, l in ID_CITY){
    omega[i,j,k,l] - delta[i,j] <= 0;
    omega[i,j,k,l] - delta[k,l] <= 0;
  }

  forall(i in ID_DEP, j in ID_CITY, k in ID_DEP, l in ID_CITY){
    delta[i,j] + delta[k,l] - omega[i,j,k,l] <= 1;
  }
   
}




 