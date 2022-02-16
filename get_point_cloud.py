import math
from scipy.spatial.transform import Rotation as R
import numpy as np
import polyscope as ps
import os
import os.path as osp
import json


from utils import image_io

output_dir = "/user/emyu/home/Documents/video-doodles/family_run_medium_output"
depth_result_dir = osp.join(output_dir, "R_hierarchical2_midas2/StD100.0_StR1.0_SmD0_SmR0.0/depth_e0000/e0000_filtered/depth/")
color_images_dir = osp.join(output_dir,"color_down")

CAMERAS_DATA_FILE = osp.join(output_dir, "cameras.json")

frame_idx = 1


def rot_matrix_from_quaternion(q):
    r = R.from_quat(q)
    return r.as_matrix()

def rotate(v, q):
    # return v
    return rot_matrix_from_quaternion(q) @ v

def right(camera_orientation_quat):
    return rotate(np.array([1, 0, 0]), camera_orientation_quat)

def up(camera_orientation_quat):
    return rotate(np.array([0, 1, 0]), camera_orientation_quat)

def down(camera_orientation_quat):
    return rotate(np.array([0, -1, 0]), camera_orientation_quat)

def forward(camera_orientation_quat):
    return rotate(np.array([0, 0, -1]), camera_orientation_quat)


def worldPosition(x, y, depth, camera, width, height):
    aspect = width / height
    x_normalized = x / width
    y_normalized = y / width
    x_clip = (-1 + 2 * x_normalized) * math.tan(camera['hFov'] / 2)
    y_clip = (-1 + 2 * y_normalized * aspect) * math.tan(camera['vFov'] / 2)

    cam_orientation = camera['orientation']

    ray_dir = right(cam_orientation)[:, None]  * x_clip + down(cam_orientation)[:, None]  * y_clip + forward(cam_orientation)[:, None] 
    # ray_dir = right(cam_orientation)[:, None]  * x + down(cam_orientation)[:, None]  * y + forward(cam_orientation)[:, None] 

    # ps.register_point_cloud("camera pos", np.array([camera['pos']]).reshape((1, 3)))
    # ps_pixels = ps.register_point_cloud("pixels", np.tile(camera['pos'], len(x)).reshape((len(x), 3)))
    # ps_pixels.add_vector_quantity("ray", ray_dir.T)

    # ps.show()

    # ray_dir = np.array([0,0,1])[:, None]
    return (np.array(camera['pos'])[:, None] + ray_dir * depth).T


def get_point_cloud(depth_image_path, color_image_path, camera, name=""):
    # Open both image files
    depth = image_io.load_raw_float32_image(depth_image_path)
    # depth = np.ones(depth.shape)
    colors = image_io.load_raw_float32_image(color_image_path)

    # depth = np.sqrt(depth)
    depth = 4 + np.max(depth) - depth

    # Get width/height
    height, width = depth.shape

    ys = np.tile(np.arange(height), width)
    xs = np.repeat(np.arange(width), height)
    zs = depth.T.flatten()

    axes = np.row_stack([right(camera['orientation']), down(camera['orientation']), forward(camera['orientation'])])
    ps_cam = ps.register_point_cloud(f"camera pos {name}", np.array([camera['pos']]).reshape((1, 3)))
    # for i in range(3):
    #     ps_cam = ps.register_point_cloud(f"camera pos {name} {i}", np.array([camera['pos']]).reshape((1, 3)))
    #     ps_cam.add_vector_quantity("view dir", axes[i].reshape((1,3)))

    Vs = worldPosition(xs, ys, zs, camera, width, height)
    # Vs = np.column_stack([xs, ys, zs * 100])

    # initial_colors = colors.copy()
    # initial_colors = initial_colors.reshape((width*height, 3))

    colors = np.transpose(colors, (1, 0, 2))
    colors = colors.reshape((width*height, 3))
    colors = colors[:, ::-1]

    # Visualize
    ps_pts = ps.register_point_cloud(f"{name} - points", Vs)
    ps_pts.add_color_quantity(f"{name} - colors", colors, enabled=True)
    # ps_pts.add_color_quantity(f"{name} - initial colors", initial_colors)
    ps_pts.add_scalar_quantity(f"{name} - depth", zs)

    ps.show()

ps.init()

with open(CAMERAS_DATA_FILE, 'r') as f:
    cameras = json.load(f)

for frame_idx in range(5):
    frame_file_name = f"frame_{frame_idx:06d}.raw"

    depth_image_path = osp.join(depth_result_dir, frame_file_name)
    color_image_path = osp.join(color_images_dir, frame_file_name)



    camera = cameras[frame_idx]

    get_point_cloud(depth_image_path, color_image_path, camera, name=frame_idx)