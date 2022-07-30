import pandas as pd
import numpy as np
from pyntcloud import PyntCloud
from PIL import Image
from matplotlib import pyplot as plt
import open3d as o3d
import argparse
parser = argparse.ArgumentParser(description="Test a model on an image")
parser.add_argument('--rgbimage', '-i', dest='image_path', help="The input image", default=None)
parser.add_argument('--depthimage', '-d', dest='depth_path', help="The input image", default=None)
args = parser.parse_args()

#Get the colour image. Convert the RGB values to a DataFrame:

colourImg= Image.open(args.image_path)
colourPixels = colourImg.convert("RGB")
#Add the RGB values to the DataFrame with a little help from StackOverflow.

colourArray  = np.array(colourPixels.getdata()).reshape((colourImg.height, colourImg.width) + (3,))
indicesArray = np.moveaxis(np.indices((colourImg.height, colourImg.width)), 0, 2)
imageArray   = np.dstack((indicesArray, colourArray)).reshape((-1,5))
df = pd.DataFrame(imageArray, columns=["x", "y", "red","green","blue"])
#Open the depth-map as a greyscale image. Convert it into an array of depths. Add it to the DataFrame

depthImg = Image.open(args.depth_path).convert('P')
depthArray = np.array(depthImg.getdata())
df.insert(loc=2, column='z', value=depthArray)
#Convert it to a Point Cloud and display it:

df[['x','y','z']] = df[['x','y','z']].astype(float)
df[['red','green','blue']] = df[['red','green','blue']].astype(np.uint)
cloud = PyntCloud(df)
# Save the point cloud as .ply file to display it in meshlab.
cloud.to_file("Ptcld.ply", also_save=["mesh","points"],as_text=True)

print("Testing IO for point cloud...")
pcd=o3d.io.read_point_cloud("Ptcld.ply")
o3d.visualization.draw_geometries([pcd])
