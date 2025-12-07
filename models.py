from typing import Any


class Soup:
    
    def __init__(self, name: str, temperature: int):
        self.name = name
        self.temperature = temperature
    
    def __str__(self) -> str:
        return f"Soup(name='{self.name}', temperature={self.temperature}°C)"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Soup):
            return False
        return self.name == other.name and self.temperature == other.temperature
    
    def __hash__(self) -> int:
        return hash((self.name, self.temperature))
    
    def describe(self) -> str:
        return f"{self.name} - served at {self.temperature}°C"


class MainCourse:
    
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    
    def __str__(self) -> str:
        return f"MainCourse(name='{self.name}', price={self.price} PLN)"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MainCourse):
            return False
        return self.name == other.name and self.price == other.price
    
    def __hash__(self) -> int:
        return hash((self.name, self.price))
    
    def describe(self) -> str:
        return f"{self.name} - {self.price} PLN"


class Dessert:
    
    def __init__(self, name: str, calories: int):
        self.name = name
        self.calories = calories
    
    def __str__(self) -> str:
        return f"Dessert(name='{self.name}', calories={self.calories} kcal)"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Dessert):
            return False
        return self.name == other.name and self.calories == other.calories
    
    def __hash__(self) -> int:
        return hash((self.name, self.calories))
    
    def describe(self) -> str:
        return f"{self.name} - {self.calories} kcal"
