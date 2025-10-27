# file: src/PyThermLIA/main.py

from video_processor import VideoProcessor
from fourier_lockin import FourierLockIn
from config_loader import load_config
import time

def main():
    """
    Main orchestration script driven by an external configuration file.
    """
    try:
        # --- 1. Load Configuration ---
        config = load_config("config.json")
        io_cfg = config["io_settings"]
        vid_cfg = config["video_processing"]
        lockin_cfg = config["lockin_analysis"]

        print("--- Lock-In Analysis Started ---")
        print(f"Loading settings from config.json...")
        
        # --- 2. Initialization (using loaded config) ---
        video = VideoProcessor(
            filepath=io_cfg["video_file"],
            mode=vid_cfg["mode"],
            pipeline=vid_cfg["pipeline"]
        )
        
        total_frames_to_process = lockin_cfg["end_frame"] - lockin_cfg["start_frame"] + 1
        
        lockin = FourierLockIn(
            modulation_freq=lockin_cfg["modulation_freq"],
            frame_rate=video.frame_rate,
            total_frames=total_frames_to_process,
            frame_shape=(video.height, video.width)
        )

        # --- 3. Processing Loop ---
        start_time = time.time()
        
        frame_generator = video.frames_generator(
            start_frame=lockin_cfg["start_frame"], 
            end_frame=lockin_cfg["end_frame"]
        )
        
        for frame in frame_generator:
            lockin.process_frame(frame)
            print(f"\rProcessing... {lockin.frames_processed}/{lockin.total_frames} frames", end="")
        
        print("\nProcessing finished.")
        
        # --- 4. Get and Export Results ---
        amplitude_map = lockin.get_amplitude()
        phase_map = lockin.get_phase()
        
        FourierLockIn.export_to_mat(
            amplitude_map, 
            phase_map,
            amp_filename=io_cfg["amplitude_output_file"],
            phase_filename=io_cfg["phase_output_file"]
        )
        print(f"Results exported to '{io_cfg['amplitude_output_file']}' and '{io_cfg['phase_output_file']}'.")

        end_time = time.time()
        print(f"Total execution time: {end_time - start_time:.2f} seconds.")

    except (IOError, ValueError, KeyError) as e:
        print(f"\nAn error occurred: {e}")
    finally:
        if 'video' in locals():
            video.release()

if __name__ == '__main__':
    main()
