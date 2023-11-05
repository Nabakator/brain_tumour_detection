from mrcnn.config import Config

class TumorConfig(Config):
    """Configuration for training on the brain tumor dataset."""
    
    # Give the configuration a recognizable name
    NAME = 'tumor_detector'
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 1 + 1  # background + tumor
    DETECTION_MIN_CONFIDENCE = 0.85    
    STEPS_PER_EPOCH = 100
    LEARNING_RATE = 0.001

    # Add the missing attribute
    PRE_NMS_LIMIT = 600