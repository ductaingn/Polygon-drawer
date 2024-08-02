'''
The function to determine the convex hull of a set of points

## Use for drawing convex polygon
'''
def graham_scan(points)->list:
    # Sort the points
    points = sorted(points)
    
    # Function to calculate the cross product of two vectors
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build the lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build the upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper hull to make the full hull
    # Remove the last point of each half because it's repeated
    return lower[:-1] + upper[:-1]