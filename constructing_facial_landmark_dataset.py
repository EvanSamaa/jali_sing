import mediapipe as mp
import cv2
import os
import shutil
import json
import moviepy.editor as ed
import time
import numpy as np
from scipy.spatial.transform import Rotation
from matplotlib import pyplot as plt

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def split_video_to_images(file_name, video_folder_path, target_fps = 30, remove=False):
    # filename can just be the name of the file,
    # the video must be in the video folder_path

    frames = []
    for video in os.listdir(video_folder_path):
        print(video)
        if video == file_name:
            video_path = os.path.join(video_folder_path, video)
            video_folder = os.path.join(video_folder_path, video[:-4])
            try:
                print(video_folder)
                os.mkdir(video_folder)
            except:
                if remove:
                    shutil.rmtree(video_folder, ignore_errors=True)
                    os.mkdir(video_folder)
                else:
                    dir_ls = os.listdir(video_folder)
                    for i in range(0, len(dir_ls) - 2):
                        frames.append(video_folder + "/frame%d.jpg" % i)
                    return frames
            my_clip = ed.VideoFileClip(video_path)
            my_clip.audio.write_audiofile(os.path.join(video_folder, "audio.mp3"))
            vidcap = cv2.VideoCapture(video_path)
            fps = vidcap.get(cv2.CAP_PROP_FPS)
            meta_data = {}
            if fps <= target_fps:
                meta_data["fps"] = fps
            else:
                factor = fps/target_fps
            meta_data["video_path"] = video_path
            meta_data["audio_path"] = os.path.join(video_folder, "audio.mp3")
            with open(os.path.join(video_folder, "other_info.json"), 'w') as outfile:
                json.dump(meta_data, outfile)
            success, image = vidcap.read()
            count = 0
            while success:
                cv2.imwrite(video_folder + "/frame%d.jpg" % count, image)  # save frame as JPEG file
                success, image = vidcap.read()
                count += 1
                frames.append(video_folder + "/frame%d.jpg" % count)
    return frames
def normalize_facial_landmark():
    return 0
def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix
def extract_landmarks(input_video, input_dir, show_annotated_video = False, show_normalized_pts = False, tolerance = 0.01):
    IMAGE_FILES = split_video_to_images(input_video,
                                        input_dir)
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5) as face_mesh:
        imgs_arr = []
        for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(file)
            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            # Print and draw face mesh landmarks on the image.
            if not results.multi_face_landmarks:
                continue

            # https://github.com/ManuelTS/augmentedFaceMeshIndices/blob/master/Nose.jpg points of the face model

            # print(results.multi_face_landmarks)
            face_landmarks = results.multi_face_landmarks[0].landmark
            land_mark_matrix_pts = np.zeros((468, 3))
            for i in range(0, len(face_landmarks)):
                land_mark_matrix_pts[i, 0] = face_landmarks[i].x
                land_mark_matrix_pts[i, 1] = face_landmarks[i].y
                land_mark_matrix_pts[i, 2] = face_landmarks[i].z
            plane_pts = [land_mark_matrix_pts[98], land_mark_matrix_pts[327], land_mark_matrix_pts[168]]
            # rotate the projected matrix to face the camerra
            n = np.cross(plane_pts[2] - plane_pts[1], plane_pts[0] - plane_pts[1])
            n = n / np.linalg.norm(n)
            R = rotation_matrix_from_vectors(n, np.array([0, 0, 1]))
            rotated_land_marks = np.expand_dims(land_mark_matrix_pts, axis=2)
            R = np.expand_dims(R, axis=0)
            rotated_land_marks = R @ rotated_land_marks
            projected_land_marks = rotated_land_marks[:, 0:2, 0]
            projected_land_marks = projected_land_marks - projected_land_marks[4]
            # rotate the face again so eyes are parallel to the screen
            nose_ridge_vector = (projected_land_marks[6, :])
            nose_ridge_vector = nose_ridge_vector / np.linalg.norm(nose_ridge_vector)
            target_nose_ridge_direction = np.array([0, 1])
            abs_angle_diff = np.arccos(np.dot(nose_ridge_vector, target_nose_ridge_direction))
            theta = abs_angle_diff
            r = np.array(((np.cos(theta), -np.sin(theta)),
                          (np.sin(theta), np.cos(theta))))
            diff = np.linalg.norm(r @ nose_ridge_vector - target_nose_ridge_direction)
            if diff >= tolerance:
                theta = - theta
                r = np.array(((np.cos(theta), -np.sin(theta)),
                              (np.sin(theta), np.cos(theta))))
                if np.linalg.norm(r @ nose_ridge_vector - target_nose_ridge_direction) >= diff:
                    theta = - theta
                    r = np.array(((np.cos(theta), -np.sin(theta)),
                                  (np.sin(theta), np.cos(theta))))

            normalized_landmark = np.expand_dims(r, axis=0) @ np.expand_dims(projected_land_marks, axis=2)

            if show_normalized_pts:
                # plt.subplot(2,1,1)
                plt.scatter(normalized_landmark[:, 0], normalized_landmark[:, 1])
                plt.scatter(normalized_landmark[4, 0], normalized_landmark[4, 1])
                plt.scatter(normalized_landmark[98, 0], normalized_landmark[98, 1])
                plt.scatter(normalized_landmark[327, 0], normalized_landmark[327, 1])
                # plt.show()
                plt.show(block=False)
                plt.pause(0.01)
                plt.close()
                # annotate the image
            if show_annotated_video:
                annotated_image = image.copy()
                for face_landmarks in results.multi_face_landmarks:
                    # print('face_landmarks:', face_landmarks)
                    mp_drawing.draw_landmarks(
                        image=annotated_image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=annotated_image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                            .get_default_face_mesh_contours_style())
                # imgs_arr.append(annotated_image)
                # cv2.imwrite('./tmp/annotated_image' + str(idx) + '.png', annotated_image)
                cv2.imshow("k", annotated_image)
                cv2.waitKey(1)

        # size = (imgs_arr[0].shape[0], imgs_arr[0].shape[1])
        # fps = 25
        #
        # out = cv2.VideoWriter('./tmp/annotated_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        # for i in range(len(imgs_arr)):
        #     out.write(imgs_arr[i])
        # out.release()
if __name__ == "__main__":
    # IMAGE_FILES = split_video_to_images("original_clip.mov",
    #                                     "C:\\Users\\evansamaa\\Desktop\\Jali_Experiments\\zombie\\videos")
    input_video = "zombie_part.mp4"
    input_dir = "/Users/evansamaa/Desktop/jali_sing_exp/zombie/"
    show_annotated_video = False
    show_normalized_pts = False
    tolerance = 0.01

    extract_landmarks(input_video, input_dir, show_annotated_video=True)

