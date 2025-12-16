# Simple test file

# ERROR: Matrix rows with different sizes
A = [ [4, 5],[1, 2, 3]];

# ERROR: Out of bounds access
B = [[1, 2], [3, 4]];
x = B[5, 1];

# ERROR: Break outside loop
break;

# ERROR: Undefined variable
z = undefined_var + 5;

# ERROR: Adding scalar to matrix
C = B + 5;

# ERROR: Invalid matrix function parameter
E = eye(0);

# OK: Valid operations
H = eye(3);
I = ones(4);
J = zeros(5);

K = [[1, 2, 3], [4, 5, 6]];
L = K';

M = [[1, 2], [3, 4]];
N = [[5, 6], [7, 8]];
O = M + N;
P = M .* N;

# OK: Break inside loop with nested if
for i = 1:10 {
    if (i == 5) {
        break;
    }
}

# OK: Valid vector operations
vec1 = [1, 2, 3];
vec2 = [4, 5, 6];
vec3 = vec1 + vec2;
vec4 = vec1 .* vec2;

# OK: Matrix with two parameters
rect = zeros(3, 5);
rect2 = ones(2, 4);

# ERROR: Transpose non-matrix
scalar = 5;
result = scalar';

# ERROR: Continue outside loop
continue;

# ERROR: Matrix function with negative parameter
bad = zeros(-5);

# ERROR: Rectangular matrix multiplication
R1 = zeros(2, 3);
R2 = zeros(3,9);
R3 = R1 * R2;

Z = [[2,23,1],[2,3,4,5]];
Z1 = [[1,3,4,2],[2,3,4,5]];
Z2 = Z1 * Z;

x=0;