from backend.models.dtos import FertilizerRequestDTO, FertilizerResponseDTO

def execute(request: FertilizerRequestDTO) -> FertilizerResponseDTO:
    flags = []
    
    crop_reqs = request.rules.requirements.get(request.crop)
    if not crop_reqs:
        flags.append("CROP_NOT_FOUND")
        return FertilizerResponseDTO(n=0.0, p=0.0, k=0.0, notes="No data for this crop.", degradation_flags=flags)
        
    stage_reqs = crop_reqs.get(request.stage)
    if not stage_reqs:
        flags.append("STAGE_NOT_FOUND")
        # Fallback to vegetative or first available if stage missing
        default_stage = list(crop_reqs.values())[0] if crop_reqs else {"N":0, "P":0, "K":0, "notes":"Default"}
        return FertilizerResponseDTO(
            n=default_stage.get("N", 0.0),
            p=default_stage.get("P", 0.0),
            k=default_stage.get("K", 0.0),
            notes=default_stage.get("notes", "Using generic data."),
            degradation_flags=flags
        )
        
    return FertilizerResponseDTO(
        n=stage_reqs.get("N", 0.0),
        p=stage_reqs.get("P", 0.0),
        k=stage_reqs.get("K", 0.0),
        notes=stage_reqs.get("notes", "Optimal."),
        degradation_flags=flags
    )
