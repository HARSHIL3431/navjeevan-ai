from dataclasses import dataclass

@dataclass(frozen=True)
class BusinessRules:
    RAIN_THRESHOLD_MM: float = 10.0
    TRANSPORT_COST_PER_KM_PER_QTL: float = 5.0
    MARKET_DATA_STALENESS_LIMIT_HOURS: int = 24
    CONFIDENCE_LIMIT_WEATHER_FAIL: int = -30
    CONFIDENCE_LIMIT_MARKET_FAIL: int = -20
    CONFIDENCE_LIMIT_GENERIC_RULE: int = -10

business_rules = BusinessRules()
