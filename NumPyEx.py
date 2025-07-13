import numpy as np

def magic(n):
    n = int(n)
    if n < 3:
        raise ValueError("Size must be at least 3")
    if n % 2 == 1:  # Odd order
        p = np.arange(1, n+1)
        return n * np.mod(p[:, None] + p - (n+3)//2, n) + np.mod(p[:, None] + 2*p - 2, n) + 1
    elif n % 4 == 0:  # Doubly-even order (multiple of 4)
        J = np.mod(np.arange(1, n+1), 4) // 2
        K = J[:, None] == J
        M = np.arange(1, n*n+1, n)[:, None] + np.arange(n)
        M[K] = n*n + 1 - M[K]
        return M
    else:  # Singly-even order (even but not multiple of 4)
        p = n // 2
        M = magic(p)
        M = np.block([[M, M + 2*p*p],
                      [M + 3*p*p, M + p*p]])
        i = np.arange(p)
        k = (n-2) // 4
        j = np.concatenate((np.arange(k), np.arange(n-k+1, n)))
        M[np.ix_(np.concatenate((i, i+p)), j)] = M[np.ix_(np.concatenate((i+p, i)), j)]
        M[np.ix_([k, k+p], [0, k])] = M[np.ix_([k+p, k], [0, k])]
        return M

def ran(size):
    """Generate an array of given size with random integers from -5 to 4 (inclusive)."""
    return np.random.randint(-5, 5, size)

# Step 1.1: Create a 50x50 matrix of ones (dtype float for later NaN usage)
mat = np.ones((50, 50), dtype=float)
print("1)", mat)

# Step 1.2: Fill the lower triangle (including main diagonal) with random integers
mat[np.tril_indices(50)] = ran(len(mat[np.tril_indices(50)]))
print("2)", mat)

# Step 1.3: Generate a 50x50 magic square matrix and normalize each row to max=4
M = magic(50)
row_maxes = np.max(M, axis=1, keepdims=True)
normal = (M / row_maxes) * 4  # scale each row so that its maximum becomes 4
# Fill the upper triangle (including diagonal) of 'mat' with the normalized magic matrix values
mat[np.triu_indices(50)] = normal[np.triu_indices(50)]
print("3)", mat)

# Step 1.4: Set the secondary diagonal to 0 and main diagonal to 2
mat = np.fliplr(mat)             # flip matrix left-right to work on secondary diagonal as if it were main
np.fill_diagonal(mat, 0)         # set what was secondary diagonal to 0
mat = np.fliplr(mat)             # flip back to original orientation
np.fill_diagonal(mat, 2)         # set main diagonal to 2
print("4)", mat)

# Step 1.5: Introduce two random NaN values (not on the borders)
rows = np.random.randint(1, 49, size=2)
cols = np.random.randint(1, 49, size=2)
mat[rows[0], cols[0]] = np.nan
mat[rows[1], cols[1]] = np.nan
print("5)", mat)

# Step 2: Calculate statistics ignoring NaNs
print("Overall sum (ignoring NaNs):", np.nansum(mat))
print("Overall mean (ignoring NaNs):", np.nanmean(mat))
min_per_column = np.nanmin(mat, axis=0)
min_per_row    = np.nanmin(mat, axis=1)
max_per_column = np.nanmax(mat, axis=0)
max_per_row    = np.nanmax(mat, axis=1)
print("Min per column:", min_per_column)
print("Min per row:", min_per_row)
print("Max per column:", max_per_column)
print("Max per row:", max_per_row)

# Replace NaNs with the mean of their 8 neighbors
nan_positions = np.argwhere(np.isnan(mat))
for (i, j) in nan_positions:
    # extract the 3x3 block around (i, j)
    block = mat[i-1:i+2, j-1:j+2]
    mean_value = np.nanmean(block)
    mat[i, j] = mean_value
print("6)", mat)

# Step 3: Remove columns with more than four '1' values
count_ones_per_column = np.sum(mat == 1, axis=0)
columns_to_keep = count_ones_per_column <= 4
mat_new = mat[:, columns_to_keep]
print("New matrix shape:", mat_new.shape)
print("New matrix:\n", mat_new)
