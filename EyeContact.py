import cv2


def analyze_video(video_path):
    """Analyzes an mp4 to estimate looking at camera time.

  Args:
    video_path: The path to the mp4 video file.

  Returns:
    None. This function does not return a value, but prints an estimate.
  """

    # Open the video capture
    cap = cv2.VideoCapture(video_path)

    # Initialize variables
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    looking_time = 0

    # Loop through each frame of the video
    for _ in range(total_frames):
        ret, frame = cap.read()

        # Check if frame is read correctly
        if not ret:
            print("Error: Could not read frame")
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Loop through each detected face
        for (x, y, w, h) in faces:
            # Extract the region of interest (ROI) for the face
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            # Detect eyes in the ROI
            eyes = eye_cascade.detectMultiScale(roi_gray)

            # Check if two eyes are detected
            if len(eyes) == 2:
                # Increment looking time counter
                looking_time += 1

    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

    # Estimate total looking time based on frame count and assumed FPS
    estimated_fps = 30  # Replace with actual FPS if known
    total_time = total_frames / estimated_fps
    print(f"Estimated looking at camera time: {looking_time / total_time:.2f} seconds")


# Replace 'path/to/video.mp4' with the path to your video file
video_path = 'eyetest.mp4'
analyze_video(video_path)
