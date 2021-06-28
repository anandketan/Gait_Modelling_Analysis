import numpy as np
import open3d as o3d 
points = [
[0, 0, 0],
[1, 0, 0],
[0, 1, 0],
[1, 1, 0],
[0, 0, 1],
[1, 0, 1],
[0, 1, 1],
[1, 1, 1],
]
cloud = o3d.utility.Vector3dVector(points) # Read the point cloud
pointcloud = o3d.geometry.PointCloud()
pointcloud.points = o3d.utility.Vector3dVector(cloud)
o3d.visualization.draw_geometries([pointcloud]) # Visualize the point cloud  