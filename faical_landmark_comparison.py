import mediapipe as mp
import cv2
import os
import shutil
import json
import moviepy.editor as ed
import time
from matplotlib import pyplot as plt
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def split_video_to_images(file_name, video_folder_path, target_fps = 30, remove=False):
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
if __name__ == "__main__":

    IMAGE_FILES = split_video_to_images("original_clip.mov", "C:\\Users\\evansamaa\\Desktop\\Jali_Experiments\\zombie\\videos")
    # IMAGE_FILES = ["C:\\Users\\evansamaa\\Desktop\\frozen_elsa_png_7_copy1.png"]
    IMAGE_FILES = [IMAGE_FILES[0], IMAGE_FILES[1]]
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
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
            annotated_image = image.copy()
            # print(results.multi_face_landmarks)
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
            imgs_arr.append(annotated_image)
            # cv2.imwrite('./tmp/annotated_image' + str(idx) + '.png', annotated_image)
            # cv2.imshow("k", annotated_image)
            # cv2.waitKey(0)
            x_coord = []
            y_coord = []
            for face_landmarks in results.multi_face_landmarks:
                for landmark in face_landmarks.landmark:
                    # if len(x_coord) >= 68:
                    #     break
                    x_coord.append(landmark.x)
                    y_coord.append(landmark.y)
                    z_coord.append()
            plt.scatter(x_coord, y_coord)
            plt.show()
            plt.close(0.1)


        # size = (imgs_arr[0].shape[0], imgs_arr[0].shape[1])
        # fps = 25
        #
        # out = cv2.VideoWriter('./tmp/annotated_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
        # for i in range(len(imgs_arr)):
        #     out.write(imgs_arr[i])
        # out.release()