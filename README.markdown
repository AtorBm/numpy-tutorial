# Matrix Construction and Analysis Tasks

This document outlines a series of tasks involving matrix construction, statistical analysis with missing data, and column filtering. Below are the tasks as provided, followed by a detailed implementation in Python.

## Tasks

### Matrix Construction

1. Create a 50×50 matrix filled entirely with ones.
2. Fill the entries below the main diagonal with random integer values between -5 and 4.
3. Replace the entries above the main diagonal with the corresponding entries from a magic matrix of the same size (50×50). Research what a magic square is and briefly report on it. Normalize each row of this magic matrix to have a maximum value of 4. (Hint: The magic matrix values might be large; scale each row by a factor so that the largest entry in each row becomes 4.)
4. Set the secondary diagonal (the diagonal from top-right to bottom-left) to 0.
5. Set the main diagonal to 2.
6. Randomly select two elements of the matrix (that are not on the matrix borders) and set them to NaN.
   - Perform all the above steps in the given order.

### Statistics with Missing Data

1. For the resulting matrix (without any special NaN handling), calculate:
   - The mean of each row.
   - The mean of each column.
   - The mean of the entire matrix.
   - The minimum and maximum value of each row.
2. Did you encounter any problems computing these values? Note that standard operations cannot handle NaN values properly (they propagate as NaN).
3. Find the position of each NaN in the matrix and replace it with the average of its eight surrounding neighbors (the cells that immediately surround that position horizontally, vertically, and diagonally).

### Column Filtering

1. Remove any column of the matrix that contains more than four occurrences of the number 1. (The resulting matrix will naturally have different dimensions than the original.)

---

# Implementation and Explanation

Below is a detailed explanation of how to implement the tasks using Python with NumPy. Each step is broken down for clarity, and the complete code is provided at the end.

## Matrix Construction

### Step 1: Create a 50×50 Matrix Filled with Ones

We start by creating a 50×50 matrix filled with ones. Since we’ll introduce NaN values later, we use a float data type to accommodate them.

- **Method**: Use `np.ones((50, 50), dtype=float)`.

### Step 2: Fill Entries Below the Main Diagonal with Random Integers

Next, we fill the entries *below* the main diagonal with random integers between -5 and 4. In matrix terminology, "below the main diagonal" typically refers to the strictly lower triangular part (where row index &gt; column index), excluding the diagonal itself.

- **Method**: Use `np.tril_indices(50, k=-1)` to get the indices below the diagonal and `np.random.randint(-5, 5, size)` to generate random integers. Note that `randint(-5, 5)` produces values from -5 to 4 (upper bound exclusive), matching the requirement.

### Step 3: Replace Entries Above the Main Diagonal with a Normalized Magic Matrix

We need a 50×50 magic matrix (magic square) and must normalize its rows so the maximum value in each row is 4.

#### What is a Magic Square?

A magic square is an ( n \\times n ) grid of distinct integers (typically 1 to ( n^2 )) arranged such that the sum of each row, column, and both main diagonals is the same. For a 50×50 magic square:

- It contains numbers 1 to 2500 (since ( 50^2 = 2500 )).
- The magic constant (sum of each row/column/diagonal) is given by ( \\frac{n (n^2 + 1)}{2} = \\frac{50 \\cdot 2501}{2} = 62525 ).

Since NumPy doesn’t provide a built-in magic square function (unlike MATLAB), we’ll assume a custom `magic(n)` function exists to generate it. In practice, generating a magic square for even ( n ) like 50 requires specific algorithms (e.g., adapting the LUX method or partitioning methods), but for this task, we use a placeholder.

- **Normalization**: For each row, divide all elements by the row’s maximum value and multiply by 4.
- **Replacement**: Use `np.triu_indices(50, k=1)` to target entries above the main diagonal (row &lt; column) and replace them with the normalized values.

### Step 4: Set the Secondary Diagonal to 0

The secondary diagonal (anti-diagonal) runs from top-right to bottom-left (e.g., positions (0,49), (1,48), ..., (49,0)). We set these elements to 0.

- **Method**: Flip the matrix left-right with `np.fliplr()`, set the main diagonal to 0 with `np.fill_diagonal()`, then flip back.

### Step 5: Set the Main Diagonal to 2

The main diagonal (positions (0,0), (1,1), ..., (49,49)) is set to 2, overwriting any previous values.

- **Method**: Use `np.fill_diagonal(mat, 2)`.

### Step 6: Set Two Interior Elements to NaN

We select two elements not on the borders (i.e., not in rows 0 or 49, or columns 0 or 49) and set them to NaN.

- **Method**: Randomly choose row and column indices between 1 and 48. For simplicity, we accept a small chance of overlap, as the matrix is large (48×48 = 2304 interior positions).

## Statistics with Missing Data

### Computing Statistics Without NaN Handling

We calculate the means and min/max values using standard NumPy functions (`np.mean`, `np.min`, `np.max`).

- **Issue**: These functions propagate NaN. If a row, column, or the entire matrix contains a NaN, the result is NaN, making the output uninformative.

### Computing Statistics with NaN Handling

To handle NaNs properly, we use `np.nanmean`, `np.nanmin`, and `np.nanmax`, which ignore NaN values.

- **Results**:
  - Row means: Array of 50 values.
  - Column means: Array of 50 values.
  - Overall mean: Single scalar.
  - Row mins/maxs: Arrays of 50 values each.

### Replacing NaNs with Neighbor Averages

For each NaN, we compute the average of its eight neighbors (a 3×3 block centered on the NaN). Since NaNs are interior, all have eight neighbors.

- **Method**: Use `np.argwhere(np.isnan(mat))` to find NaN positions, extract each 3×3 block, and use `np.nanmean` to compute the average (ignoring the NaN).

## Column Filtering

We remove columns with more than four occurrences of 1.

- **Method**: Count 1s per column with `np.sum(mat == 1, axis=0)`, identify columns to keep (`count <= 4`), and filter the matrix.

The resulting matrix has dimensions 50 × ( m ), where ( m \\leq 50 ), depending on how many columns are removed.

---

## Complete Python Code

Below is the full implementation. Note: The `magic(n)` function is assumed to be provided; in practice, you’d need to implement or source it.

import numpy as np

# Assume magic(n) generates an n x n magic square

def magic(n): # Placeholder: In reality, implement an even-order magic square algorithm # For n=50, it should return a 50x50 array with numbers 1 to 2500 return np.arange(1, n\*n + 1).reshape(n, n).astype(float)

# Step 1: Create a 50x50 matrix of ones

mat = np.ones((50, 50), dtype=float)

# Step 2: Fill below the main diagonal with random integers between -5 and 4

lower_indices = np.tril_indices(50, k=-1) # k=-1 excludes diagonal mat\[lower_indices\] = np.random.randint(-5, 5, size=len(mat\[lower_indices\]))

# Step 3: Replace above the main diagonal with normalized magic matrix values

M = magic(50) row_maxes = np.max(M, axis=1, keepdims=True) normal = (M / row_maxes) \* 4 upper_indices = np.triu_indices(50, k=1) # k=1 excludes diagonal mat\[upper_indices\] = normal\[upper_indices\]

# Step 4: Set secondary diagonal to 0

mat = np.fliplr(mat) np.fill_diagonal(mat, 0) mat = np.fliplr(mat)

# Step 5: Set main diagonal to 2

np.fill_diagonal(mat, 2)

# Step 6: Set two interior elements to NaN

rows = np.random.randint(1, 49, size=2) cols = np.random.randint(1, 49, size=2) mat\[rows\[0\], cols\[0\]\] = np.nan mat\[rows\[1\], cols\[1\]\] = np.nan

# Statistics without NaN handling

row_means_basic = np.mean(mat, axis=1) col_means_basic = np.mean(mat, axis=0) overall_mean_basic = np.mean(mat) row_mins_basic = np.min(mat, axis=1) row_maxs_basic = np.max(mat, axis=1) print("Basic stats (with NaN propagation):") print("Row means:", row_means_basic) print("Column means:", col_means_basic) print("Overall mean:", overall_mean_basic) print("Row mins:", row_mins_basic) print("Row maxs:", row_maxs_basic) print("Note: NaNs propagate, making these stats mostly NaN.")

# Statistics with NaN handling

row_means = np.nanmean(mat, axis=1) col_means = np.nanmean(mat, axis=0) overall_mean = np.nanmean(mat) row_mins = np.nanmin(mat, axis=1) row_maxs = np.nanmax(mat, axis=1) print("\\nStats with NaN handling:") print("Row means:", row_means) print("Column means:", col_means) print("Overall mean:", overall_mean) print("Row mins:", row_mins) print("Row maxs:", row_maxs)

# Replace NaNs with average of eight neighbors

nan_positions = np.argwhere(np.isnan(mat)) for i, j in nan_positions: block = mat\[i-1:i+2, j-1:j+2\] mat\[i, j\] = np.nanmean(block)

# Column filtering: Remove columns with more than 4 ones

count_ones = np.sum(mat == 1, axis=0) columns_to_keep = count_ones &lt;= 4 mat_new = mat\[:, columns_to_keep\] print("\\nFinal matrix shape after filtering:", mat_new.shape) print("Final matrix:\\n", mat_new)