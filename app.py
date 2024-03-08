import gradio as gr
import cv2
from ultralytics import YOLO
import imageio
import glob
import PIL
import os
from dotenv import load_dotenv

from alert import sendAlert
load_dotenv()

import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

skip_frames = 20
start_frames_threshold = 10
end_frames_threshold = 20
total_snap = 5

def load_model(model_name):
    model_paths = {'YOLOv8n': r'models\cls_yolov8n_e30_640_95.pt',
                   'YOLOv8m': r"models\cls_yolov8m_e30_640_95.pt",
                   'YOLOv8l': r"models\cls_yolov8l_e30_640_96.pt"}
    model = YOLO(model_paths[model_name], task='classify')
    return model

def model_inference(frame, model):

    results = model(frame, conf=0.9)

    probs = results[0].probs.data
    class_names = ["Accident", "Non-Accident"]
    # predicted_class = results[0].probs.top1
    # Create a DataFrame for Plotly
    result_text = {"Class": class_names, "Probability": probs}
    
    return result_text

def calculate_timestamp(frame_number, frames_per_second):
    timestamp = frame_number / frames_per_second
    return timestamp

def describe_image(images):
    gemini_vision = genai.GenerativeModel('gemini-pro-vision')
    gemini_pro = genai.GenerativeModel('gemini-pro')

    description = ""
    for img in images:
        img_arr = PIL.Image.open(img)
        response = gemini_vision.generate_content(["Write a detailed explaination of that image. If there is any accident happend then It should include a description of the vehicles or humans that are involved.", img_arr], stream=True)
        response.resolve()
        description = description + ". " + response.text
        
    response = gemini_pro.generate_content(description + " Write a precise details about the incident within 100 words.")
    return response.text

import os

def delete_files_in_directory(directory_path):
    try:
        # List all files in the directory
        files = os.listdir(directory_path)

        # Iterate through the files and delete them
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        print("All files in the directory have been deleted.")
    except Exception as e:
        print(f"Error: {e}")

# Replace 'your_directory_path' with the actual path of the directory you want to clean


def run(video_path, model_name):

    delete_files_in_directory('AlertAccident')
    model = load_model(model_name)
    reader = imageio.get_reader(video_path)
    meta_data = reader.get_meta_data()

    frames_per_second = meta_data['fps']
    output_path = 'AlertAccident/output.mp4'
    # Create a VideoWriter object
    writer = imageio.get_writer(output_path, fps=meta_data['fps'])

    i = 0
    is_accident_detected = False
    consecutive_frames_count = 0
    accident_start_time = None
    accident_end_time = None
    take_snap = 1


    for frame in reader: # type: ignore
        # Perform inference using the model on the current frame
        result_dict = model_inference(frame, model)
        timestamp = calculate_timestamp(i+1, frames_per_second)

        if result_dict["Probability"][0] > 0.9:
            consecutive_frames_count += 1

            if not is_accident_detected and consecutive_frames_count == 1:
                # First frame of a potential accident
                accident_start_time = timestamp

            if consecutive_frames_count >= start_frames_threshold:
                # Detected accident for consecutive_frames_threshold frames
                is_accident_detected = True

        else:
            if is_accident_detected:
                consecutive_frames_count += 1

                if consecutive_frames_count >= end_frames_threshold:
                    # Detected non-accident after an accident
                    is_accident_detected = False
                    accident_end_time = timestamp

                    # Store or print accident start and end times
                    print(f"Accident Start Time: {accident_start_time:.2f}, Accident End Time: {accident_end_time:.2f}")
                    sendAlert(accident_start_time, accident_end_time)

            else:
                consecutive_frames_count = 0

        # showing accident detected images
        if is_accident_detected and i % skip_frames == 0 and take_snap < total_snap:
            filename = f"AlertAccident/time-{timestamp:.2f}s.jpg"
            imageio.imwrite(filename, frame)
            isGallaryVisible = True
            take_snap += 1

        i += 1
        # Anontate the frame with the proper label
        if result_dict["Probability"][0] > result_dict["Probability"][1]:
            top_text = f"{result_dict['Class'][0]}: {result_dict['Probability'][0]:.2f}"
            bottom_text = f"{result_dict['Class'][1]}: {result_dict['Probability'][1]:.2f}"
            cv2.putText(frame, top_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, bottom_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            top_text = f"{result_dict['Class'][1]}: {result_dict['Probability'][1]:.2f}"
            bottom_text = f"{result_dict['Class'][0]}: {result_dict['Probability'][0]:.2f}"
            cv2.putText(frame, top_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, bottom_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Append the frame to the output video
        writer.append_data(frame)

    # Release resources
    writer.close()

    if len(os.listdir('AlertAccident')) > 1:
        explaination = describe_image(glob.glob("AlertAccident/*.jpg"))
    else:
        explaination = None
    
    return output_path, glob.glob("AlertAccident/*.jpg"), explaination



inp_vid = gr.Video(label='Input Video', height=400)
dropdown = gr.Dropdown(choices=['YOLOv8n', 'YOLOv8m', 'YOLOv8l'], value='YOLOv8n')
out_vid = gr.PlayableVideo(label='Predicted Video', height=400)

gallery = gr.Gallery(label="Accident Detected images", show_label=True, columns=[3], object_fit="contain", height="auto", allow_preview=True)
text_box = gr.TextArea(label="Accident Description")

demo = gr.Interface(run,
                inputs=[inp_vid, dropdown],
                outputs=[out_vid, gallery, text_box],
                allow_flagging='never')

if __name__ == "__main__":
    demo.launch(share=True)
