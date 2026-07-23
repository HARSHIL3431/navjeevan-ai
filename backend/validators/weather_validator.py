def validate_weather(temp: float, humidity: float) -> tuple[float, float]:
    if not -50 <= temp <= 60:
        raise ValueError("Temperature out of valid range (-50 to 60)")
    if not 0 <= humidity <= 100:
        raise ValueError("Humidity must be between 0 and 100")
    return temp, humidity
