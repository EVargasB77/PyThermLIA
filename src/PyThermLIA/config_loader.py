# file: src/PyThermLIA/config_loader.py

import json
from .video_processor import FrameProcessingMode, FilterOperation

def load_config(config_path="config.json"):
    """
    Loads configuration from a JSON file and maps string values to Enums.

    Args:
        config_path (str): The path to the configuration file.

    Returns:
        dict: A dictionary containing the application settings.
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # --- Translate string settings to Enum types ---
        
        # 1. Translate FrameProcessingMode
        mode_str = config["video_processing"]["mode"]
        config["video_processing"]["mode"] = FrameProcessingMode[mode_str]
        
        # 2. Translate FilterOperation pipeline
        pipeline_str_list = config["video_processing"]["pipeline"]
        config["video_processing"]["pipeline"] = [FilterOperation[op_str] for op_str in pipeline_str_list]

        return config

    except FileNotFoundError:
        raise IOError(f"Configuration file not found at: {config_path}")
    except KeyError as e:
        raise ValueError(f"Missing required key in config file: {e}")
    except Exception as e:
        # This will catch invalid Enum strings (e.g., FilterOperation['INVALID_FILTER'])
        raise ValueError(f"Invalid value in configuration file: {e}")

