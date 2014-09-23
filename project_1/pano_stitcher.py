"""Project 1: Panorama stitching.

In this project, you'll stitch together images to form a panorama.

A shell of starter functions that already have tests is listed below.

TODO: Implement!
"""

import cv2
import numpy as np


def homography(image_a, image_b):
    """Returns the homography mapping image_b into alignment with image_a.

    Arguments:
      image_a: A grayscale input image.
      image_b: A second input image that overlaps with image_a.

    Returns: the 3x3 perspective transformation matrix (aka homography)
             mapping points in image_b to corresponding points in image_a.
    """

    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(image_a, None)
    kp2, des2 = sift.detectAndCompute(image_b, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test
    good = []
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in good])
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good])

    H, status = cv2.findHomography(dst_pts, src_pts, cv2.LMEDS, 1.0)

    return H


def warp_image(image, homography):
    """Warps 'image' by 'homography'

    Arguments:
      image: a 3-channel image to be warped.
      homography: a 3x3 perspective projection matrix mapping points
                  in the frame of 'image' to a target frame.

    Returns:
      - a new 4-channel image containing the warped input, resized to contain
        the new image's bounds. Translation is offset so the image fits exactly
        within the bounds of the image. The fourth channel is an alpha channel
        which is zero anywhere that the warped input image does not map in the
        output, i.e. empty pixels.
      - an (x, y) tuple containing location of the warped image's upper-left
        corner in the target space of 'homography', which accounts for any
        offset translation component of the homography.
    """

    img_alpha = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    h, w = img_alpha.shape[:2]

    img_pts = np.float32([[0, 0], [w, 0], [0, h], [w, h]]).reshape(-1, 1, 2)
    warped_pts = cv2.perspectiveTransform(img_pts, homography)

    max_0 = max(warped_pts[0][0][0], warped_pts[1][0][0],
                warped_pts[2][0][0], warped_pts[3][0][0])
    max_1 = max(warped_pts[0][0][1], warped_pts[1][0][1],
                warped_pts[2][0][1], warped_pts[3][0][1])
    min_0 = min(warped_pts[0][0][0], warped_pts[1][0][0],
                warped_pts[2][0][0], warped_pts[3][0][0])
    min_1 = min(warped_pts[0][0][1], warped_pts[1][0][1],
                warped_pts[2][0][1], warped_pts[3][0][1])

    warpedImage = cv2.warpPerspective(img_alpha,
                                      homography, (max_0-min_0, max_1-min_1))

    return warpedImage, (warped_pts[0][0][0], warped_pts[0][0][1])


def create_mosaic(images, origins):
    """Combine multiple images into a mosaic.

    Arguments:
      images: a list of 4-channel images to combine in the mosaic.
      origins: a list of the locations upper-left corner of each image in
               a common frame, e.g. the frame of a central image.

    Returns: a new 4-channel mosaic combining all of the input images. pixels
             in the mosaic not covered by any input image should have their
             alpha channel set to zero.
    """
    pass
