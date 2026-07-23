from backend.models.dtos import ConfidenceRequestDTO, ConfidenceResponseDTO

def execute(request: ConfidenceRequestDTO) -> ConfidenceResponseDTO:
    score = 100
    for flag in request.flags:
        penalty = request.penalties.get(flag, 0)
        score += penalty # penalties should be negative integers
        
    score = max(0, min(100, score))
    return ConfidenceResponseDTO(score=score)
