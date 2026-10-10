"""
Image Preprocessor & Quality Validator
Inspects resolution, calculates brightness/contrast, detects blur via gradient variance.
"""

from typing import Tuple, Dict, Any
from io import BytesIO
from PIL import Image, ImageStat, ImageFilter
import numpy as np


class ImagePreprocessor:
    def __init__(self, min_width: int = 150, min_height: int = 150, max_dimension: int = 2048):
        self.min_width = min_width
        self.min_height = min_height
        self.max_dimension = max_dimension

    def process(self, image_bytes: bytes) -> Tuple[Image.Image, Dict[str, Any]]:
        """
        Loads image, measures visual quality metrics (luminance, contrast, sharpness).
        """
        try:
            image = Image.open(BytesIO(image_bytes))
            image.load()
        except Exception as e:
            raise ValueError(f"Invalid image format: {str(e)}")

        orig_w, orig_h = image.size
        if orig_w < self.min_width or orig_h < self.min_height:
            raise ValueError(f"Image resolution too low ({orig_w}x{orig_h}). Minimum 150x150 required.")

        # Convert to RGB if necessary
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Downsample if exceeding max dimension
        processed_img = image
        if max(orig_w, orig_h) > self.max_dimension:
            processed_img.thumbnail((self.max_dimension, self.max_dimension), Image.Resampling.LANCZOS)

        # 1. Luminance & Contrast via ImageStat
        gray = processed_img.convert("L")
        stat = ImageStat.Stat(gray)
        mean_lum = stat.mean[0]
        stddev_lum = stat.stddev[0]

        # 2. Gradient / Edge Sharpness via High-Pass Filter variance
        edges = gray.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        edge_variance = edge_stat.var[0] # Higher variance indicates sharper edges/fonts

        is_too_dark = mean_lum < 30
        is_too_bright = mean_lum > 230
        is_low_contrast = stddev_lum < 18
        is_blurry = edge_variance < 15.0

        # Normalized sharpness score (0 to 100)
        sharpness_score = min(100, int((edge_variance / 150.0) * 100))

        quality_report = {
            "original_width": orig_w,
            "original_height": orig_h,
            "processed_width": processed_img.width,
            "processed_height": processed_img.height,
            "mean_luminance": round(mean_lum, 1),
            "contrast_stddev": round(stddev_lum, 1),
            "edge_sharpness_score": sharpness_score,
            "is_acceptable": not (is_too_dark or is_too_bright),
            "is_blurry": is_blurry,
            "warnings": []
        }

        if is_too_dark:
            quality_report["warnings"].append("Low light detected. Scan under brighter lighting.")
        if is_too_bright:
            quality_report["warnings"].append("Excessive glare detected. Tilt packaging away from glare.")
        if is_low_contrast:
            quality_report["warnings"].append("Low contrast. Packaging should stand out against background.")
        if is_blurry:
            quality_report["warnings"].append("Potential image blur. Ensure packaging text is sharp.")

        return processed_img, quality_report
