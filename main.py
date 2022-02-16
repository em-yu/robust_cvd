#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

import os
import os.path as osp
import sys

sys.path.append(osp.abspath(__file__))
sys.path.append(osp.join(osp.dirname(__file__), "lib/build"))
print(sys.path)

from params import Video3dParamsParser
from process import DatasetProcessor

# python3 main.py --video_file /user/emyu/home/Documents/video-doodles/family_run.mov --path /user/emyu/home/Documents/video-doodles/family_run_output --save_intermediate_depth_streams_freq 1 --num_epochs 0 --post_filter --opt.adaptive_deformation_cost 10 --frame_range 0-10 --save_depth_visualization
# python3 main.py --video_file /user/emyu/home/Documents/video-doodles/family_run_medium.mov --path /user/emyu/home/Documents/video-doodles/family_run_medium_output --save_intermediate_depth_streams_freq 1 --num_epochs 0 --post_filter --opt.adaptive_deformation_cost 10 --save_depth_visualization

if __name__ == "__main__":
    parser = Video3dParamsParser()
    params = parser.parse()

    dp = DatasetProcessor(params)
    dp.process()
