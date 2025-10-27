# file: main.py

from video_processor import VideoProcessor
from fourier_lockin import FourierLockIn
import time

def main():
    """
    Main orchestration script to perform Lock-In analysis on a video file.
    """
    # --- 1. Configuration ---
    VIDEO_FILE = 'AISI304.avi'  # Make sure this file is accessible
    START_FRAME = 3000
    END_FRAME = 8000
    MODULATION_FREQ = 0.3

    print("--- Lock-In Analysis Started ---")
    print(f"Video: {VIDEO_FILE}, Frames: {START_FRAME}-{END_FRAME}, Freq: {MODULATION_FREQ} Hz")

    try:
        # --- 2. Initialization ---
        video = VideoProcessor(VIDEO_FILE)
        
        total_frames_to_process = END_FRAME - START_FRAME + 1
        
        lockin = FourierLockIn(
            modulation_freq=MODULATION_FREQ,
            frame_rate=video.frame_rate,
            total_frames=total_frames_to_process,
            frame_shape=(video.height, video.width)
        )

        # --- 3. Processing Loop ---
        start_time = time.time()
        
        # Use the generator to iterate through the desired frames
        frame_generator = video.frames_generator(start_frame=START_FRAME, end_frame=END_FRAME)
        
        for frame in frame_generator:
            lockin.process_frame(frame)
            # Simple progress bar
            print(f"\rProcessing... {lockin.frames_processed}/{lockin.total_frames} frames", end="")
        
        print("\nProcessing finished.")
        
        # --- 4. Get and Export Results ---
        amplitude_map = lockin.get_amplitude()
        phase_map = lockin.get_phase()
        
        FourierLockIn.export_to_mat(amplitude_map, phase_map)
        print("Amplitude and Phase maps exported to 'Amplitude.mat' and 'Phase.mat'.")

        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds.")

    except (IOError, ValueError) as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # The VideoProcessor will be released automatically, but explicit is good practice
        if 'video' in locals():
            video.release()

if __name__ == '__main__':
    main()

