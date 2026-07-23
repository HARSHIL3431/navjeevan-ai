from backend.models.dtos import PestRequestDTO, PestResponseDTO

def execute(request: PestRequestDTO) -> PestResponseDTO:
    flags = []
    
    if not request.weather.is_available:
        flags.append("WEATHER_UNAVAILABLE")
        return PestResponseDTO(risk_level="Unknown", pests=[], degradation_flags=flags)
        
    temp = request.weather.temp_c
    hum = request.weather.humidity_percent
    
    if temp is None or hum is None:
        flags.append("MISSING_WEATHER_PARAMS")
        return PestResponseDTO(risk_level="Unknown", pests=[], degradation_flags=flags)
        
    detected_pests = []
    for pest in request.rules.pests:
        min_t = pest.get("min_temp", -99)
        max_t = pest.get("max_temp", 99)
        min_h = pest.get("min_humidity", 0)
        
        if min_t <= temp <= max_t and hum >= min_h:
            detected_pests.append(pest.get("name", "Unknown Pest"))
            
    if detected_pests:
        return PestResponseDTO(risk_level="High", pests=detected_pests, degradation_flags=flags)
        
    return PestResponseDTO(risk_level="Low", pests=[], degradation_flags=flags)
