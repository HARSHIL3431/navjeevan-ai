from backend.models.dtos import IrrigationRequestDTO, IrrigationResponseDTO

def execute(request: IrrigationRequestDTO) -> IrrigationResponseDTO:
    flags = []
    
    if not request.weather.is_available:
        flags.append("WEATHER_UNAVAILABLE")
        return IrrigationResponseDTO(
            irrigate=True, 
            volume_l=0.0, 
            reason="Weather data unavailable. Manual soil moisture check required.", 
            degradation_flags=flags
        )
        
    rain = request.weather.forecast_3d_rain_mm
    if rain is None:
        flags.append("MISSING_RAIN_DATA")
        return IrrigationResponseDTO(
            irrigate=True,
            volume_l=0.0,
            reason="Rain forecast missing. Manual soil check advised.",
            degradation_flags=flags
        )
        
    if rain > request.rules.rain_threshold_mm:
        return IrrigationResponseDTO(
            irrigate=False,
            volume_l=0.0,
            reason=f"Sufficient rain expected ({rain}mm).",
            degradation_flags=flags
        )
        
    volume_modifier = request.rules.stage_modifiers.get(request.stage, 1.0)
    base_volume = 1000.0 # Base liters per acre example
    final_volume = base_volume * volume_modifier
    
    return IrrigationResponseDTO(
        irrigate=True,
        volume_l=final_volume,
        reason=f"Dry conditions expected. Stage '{request.stage}' requires irrigation.",
        degradation_flags=flags
    )
