

import os
import os.path as osp
from utils.visualization import visualize_depth_dir

# Change based on your output path.
output_dir = "/user/emyu/home/Documents/video-doodles/family_run_medium_output"

depth_midas_dir = osp.join(output_dir, "depth_midas2/depth")
depth_vis_midas_dir = osp.join(output_dir, "depth_vis_midas2")
os.makedirs(depth_vis_midas_dir, exist_ok=True)
visualize_depth_dir(depth_midas_dir, depth_vis_midas_dir, cmap=False)

depth_result_dir = osp.join(output_dir, "R_hierarchical2_midas2/StD100.0_StR1.0_SmD0_SmR0.0/depth_e0000/e0000_filtered/depth/")
depth_vis_result_dir = osp.join(output_dir,"depth_vis_result")
os.makedirs(depth_vis_result_dir, exist_ok=True)
visualize_depth_dir(depth_result_dir, depth_vis_result_dir, cmap=False)