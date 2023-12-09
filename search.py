#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import cv2
import hashlib
import time
import sys

import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

if len(sys.argv) < 2:
    sys.exit(1)


# In[2]:


start_time = time.time()


# In[3]:


def frame_hash(frame):
    
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate mean
    mean_val = gray_frame.mean()

    # Create a hash
    hash_val = hashlib.md5(str(mean_val).encode()).hexdigest()

    return hash_val


# In[4]:


video_filename = sys.argv[1]
cap = cv2.VideoCapture(video_filename)

if not cap.isOpened():
    print(f"Could not open {video_filename}")
else:
    frame_hashes_all = []
    frame_hashes_10 = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if the video ends
    
        # Process frame to get hash
        hash_val = frame_hash(frame)
    
        # Store hash value
        frame_hashes_all.append(hash_val)
        if frame_count % 10 == 0:
            frame_hashes_10.append(hash_val)

        frame_count += 1
        
    cap.release()
    cv2.destroyAllWindows()


# In[5]:


# def is_video_contained(main_video_hashes, sub_video_hashes, similarity_threshold=0.95):
def is_video_contained(main_video_hashes, sub_video_hashes):
    len_sub = len(sub_video_hashes)
    len_main = len(main_video_hashes)

    for i in range(len_main - len_sub + 1):
        # matching_frames = 0
        # for j in range(len_sub):
        #     if main_video_hashes[i + j] == sub_video_hashes[j]:
        #         matching_frames += 1

        # similarity = matching_frames / len_sub
        # if similarity >= similarity_threshold:
        #     return True, i  # Returns True and the starting index in the main video

        if main_video_hashes[i:i+len_sub] == sub_video_hashes:
            return i

    return -1


# In[6]:


vno = 0
for i in range(1, 21):
    fno = -1
    for j in range(10):
        filename = f'vpkl/v_{i}_{j}.pkl'
        with open(filename, 'rb') as file:
            v_10 = pickle.load(file)
            
        fno = is_video_contained(v_10, frame_hashes_10)
        
        if fno != -1:
            fno = j + 10 * fno
            break

    if fno != -1:
        filename = f'vpkl/v_{i}.pkl'
        with open(filename, 'rb') as file:
            v_all = pickle.load(file)

        if v_all[fno:fno+len(frame_hashes_all)] == frame_hashes_all:
            vno = i
            print('Video:', vno)
            print('Frame #:', fno - 1)
            break


# In[7]:


print('Time elapsed:', time.time() - start_time)


# GUI:


if vno == 0:
    sys.exit()
    
import subprocess

video_path = f'file:///Users/yuchenpeng/Downloads/Videos/video{vno}.mp4'
frame_number = fno

java_command = [
    "java",
    "--module-path",
    "/Users/yuchenpeng/javafx-sdk-17.0.9/lib",
    "--add-modules",
    "javafx.controls,javafx.media",
    "CustomMediaPlayer",
    video_path,
    str(frame_number)
]

# Run the Java program
subprocess.run(java_command)
