import logging
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)

class ExecutionWrapper:
    """Wraps service execution for logging, timing, and fallback handling."""
    
    @staticmethod
    def execute(service_name: str, correlation_id: str, func: Callable, fallback_factory: Callable, *args, **kwargs) -> Any:
        start_time = time.time()
        logger.info(f"[{correlation_id}] START: {service_name}")
        
        try:
            result = func(*args, **kwargs)
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"[{correlation_id}] SERVICE COMPLETE: {service_name} in {elapsed:.2f}ms")
            return result
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"[{correlation_id}] ERROR in {service_name}: {str(e)}")
            logger.warning(f"[{correlation_id}] FALLBACK ACTIVATED for {service_name}")
            
            fallback_dto = fallback_factory()
            if hasattr(fallback_dto, "degradation_flags"):
                fallback_dto.degradation_flags.append(f"SERVICE_FAILED_{service_name.upper()}")
                
            return fallback_dto
