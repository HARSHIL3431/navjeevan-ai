def validate_crop(crop: str) -> str:
    if not crop or not crop.strip():
        raise ValueError("Crop cannot be empty")
    return crop.strip().lower()
