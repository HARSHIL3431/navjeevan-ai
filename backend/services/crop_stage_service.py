from datetime import datetime
from typing import Optional
from backend.models.dtos import CropStageRequestDTO, CropStageResponseDTO

def _calculate_days(sowing_date: Optional[str]) -> int:
    if not sowing_date:
        return -1
    try:
        sowing = datetime.strptime(sowing_date, "%Y-%m-%d")
        delta = datetime.now() - sowing
        return delta.days
    except ValueError:
        return -1

def execute(request: CropStageRequestDTO) -> CropStageResponseDTO:
    flags = []
    
    if not request.sowing_date:
        flags.append("MISSING_SOWING_DATE")
        return CropStageResponseDTO(stage="Unknown", days_active=0, degradation_flags=flags)
        
    days = _calculate_days(request.sowing_date)
    if days < 0:
        flags.append("INVALID_DATE")
        return CropStageResponseDTO(stage="Unknown", days_active=0, degradation_flags=flags)
        
    for stage in request.rules.stages:
        if stage.get("min_days", 0) <= days <= stage.get("max_days", 999):
            return CropStageResponseDTO(
                stage=stage.get("name", "Unknown"),
                days_active=days,
                degradation_flags=flags
            )
            
    flags.append("RULE_MISSING")
    return CropStageResponseDTO(stage="Mature", days_active=days, degradation_flags=flags)
