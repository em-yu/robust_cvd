import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "lib/build"))

from lib_python import (
    DepthVideo,
    DepthVideoImporter,
    initLib,
    logToStdout as glogToStdOut
)

RESULTS_ROOT_FOLDER = '/user/emyu/home/Documents/video-doodles/family_run_medium_output'

initLib()
glogToStdOut()
depth_video = DepthVideo()

# DepthVideoImporter.importVideo(depth_video, "/", True)

depth_video.load(RESULTS_ROOT_FOLDER)


nb_frames = depth_video.numFrames()

print(nb_frames)

for i in range(depth_video.numDepthStreams()):
    print(depth_video.depthStream(i).name())

consistent_depth_stream = depth_video.depthStreamIndex('e0000_filtered')
print(consistent_depth_stream)

cameras = []

for i in range(nb_frames):
    depth_frame_i = depth_video.depthFrame(consistent_depth_stream, i)

    print(depth_frame_i)

    extrinsics = depth_frame_i.extrinsics
    intrinsics = depth_frame_i.intrinsics

    camera_i = {
        'pos': extrinsics.position.tolist(),
        'orientation': [extrinsics.orientation.x(), extrinsics.orientation.y(), extrinsics.orientation.z(), extrinsics.orientation.w()],
        'projection': str(intrinsics.projection),
        'vFov': intrinsics.vFov,
        'hFov': intrinsics.hFov,
        'centerPt': [intrinsics.centerLat, intrinsics.centerLon]
    }

    cameras.append(camera_i)

    print("position", extrinsics.position)
    print("orientation", extrinsics.orientation.x(), extrinsics.orientation.y(), extrinsics.orientation.z(), extrinsics.orientation.w())

    print("projection", intrinsics.projection)
    print("vFov", intrinsics.vFov)
    print("hFov", intrinsics.hFov)
    print("centerLat", intrinsics.centerLat, "centerLon", intrinsics.centerLon)

import json
with open(os.path.join(RESULTS_ROOT_FOLDER, 'cameras.json'), 'w') as fp:
    json.dump(cameras, fp)