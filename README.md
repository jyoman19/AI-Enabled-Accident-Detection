# AI-Enabled-Accident-Detection
Advanced AI framework integrates YOLOv8 for real-time accident detection, Gemini-vision for image description, Gradio for user interface, ensuring efficient incident management and emergency response in road safety.
- A comprehensive framework is introduced to enhance road safety, employing advanced AI technologies.
- YOLOv8 is utilized for real-time accident detection, triggering SOS alerts and capturing relevant frames.
- Gemini-vision is employed for image text description, while Gemini-pro summarizes extracted details.
- Output, including annotated inference videos, accident-detected images, and incident summaries, is presented via a user-friendly Gradio interface.

- **Introduction:**
  - Innovative solutions are imperative for timely detection and effective management of road accidents, addressing public safety concerns.
  - Cutting-edge artificial intelligence technologies are leveraged, with YOLOv8 serving as a state-of-the-art object detection model for real-time accident identification.
  
- **Data Collection:**
  - A dual dataset strategy is adopted, utilizing both a Kaggle dataset and a meticulously curated dataset through scraping.
  - The combination of datasets ensures robust model development, enhanced diversity, and comprehensive training for optimal real-world performance.

- **Model Building:**
  - The YOLO algorithm is employed, exploring variants such as YOLO v5, v7, and v8, each with distinct weight configurations.
  - Noteworthy performance is observed with the YOLOv8 classification model, achieving an impressive accuracy of 97%.
  - Rigorous evaluation ensures the system's proficiency in detecting vehicular collisions across diverse conditions.

-Detection:

| Model Name | Weights | Epochs | Precision | Recall | mAP_0.5 | mAP_0.5:0.95 |
|------------|---------|--------|-----------|--------|---------|---------------|
| YOLOv5     | yolov5n | 30     | 0.8885    | 0.884  | 0.9340  | 0.640         |
|            | yolov5n | 50     | 0.9256    | 0.915  | 0.9559  | 0.9628        |
|            | yolov5l | 30     | 0.9543    | 0.934  | 0.9700  | 0.7724        |
| YOLOv7     | yolov7  | 20     | 0.036     | 0.0136 | 0.2645  | 0.1694        |
| YOLOv8     | yolov8n | 40     | 0.95278   | 0.9216 | 0.953   | 0.74679       |
|            | yolov8s | 40     | 0.95246   | 0.9396 | 0.953   | 0.74829       |
|            | yolov8m | 40     | 0.8463    | 0.7756 | 0.875   | 0.6961        |

-Classification:

| Model Name | Epochs | Top1_ac | Top5_acc |
|------------|--------|---------|----------|
| yolov8n-cls| 30     | 0.953   | 0.983    |
| yolov8m-cls| 30     | 0.954   | 0.994    |
| yolov8l-cls| 30     | 0.968   | 1.00     |

- **Evaluation:**
  - Real-time evaluation on CCTV footage demonstrates the system's outstanding accuracy range of 98-99% in accident detection.
  - High precision underscores the system's effectiveness in promptly identifying incidents, contributing significantly to road safety.
  - The ability to achieve such precision facilitates timely response and intervention, enhancing overall safety for road users.

- **Gradio Interface:**
  - A user-friendly interface powered by Gradio facilitates interaction with the system.
  - The interface displays output such as inference videos, accident-detected images, and incident summaries, aiding quick decision-making for emergency responders and law enforcement.

- **Conclusion:**
  - The framework presents a comprehensive solution for AI-enabled accident detection and incident summarization.
  - Integration of YOLOv8, Gemini-vision, Gemini-pro, and Gradio ensures a streamlined approach to enhancing road safety.
  - Rapid detection, incident description, and real-time data summarization contribute to more efficient incident management and emergency response efforts.
