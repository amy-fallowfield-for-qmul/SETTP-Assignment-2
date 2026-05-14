from typing import Dict

class Address:
    """Structured address object with separate components"""
    
    def __init__(
        self, 
        address_line: str, 
        town_city: str, 
        postcode: str
    ):
        self.address_line = address_line.strip()
        self.town_city = town_city.strip()
        self.postcode = postcode.strip().upper()
    
    def to_dict(self) -> Dict[str, str]:
        result = {
            "address_line": self.address_line,
            "town_city": self.town_city,
            "postcode": self.postcode
        }
        return result
    
    @classmethod
    def from_string(cls, address_string: str) -> "Address":
        if not isinstance(address_string, str) or not address_string.strip():
            raise ValueError("Address string cannot be empty")
        
        parts = [part.strip() for part in address_string.split(',') if part.strip()]
        
        if len(parts) != 3:
            raise ValueError("Address must contain exactly 3 parts: address line, town/city, and postcode")
        
        return cls(
            address_line=parts[0],
            town_city=parts[1],
            postcode=parts[2]
        )
    
    def __str__(self) -> str:
        return f"{self.address_line}, {self.town_city}, {self.postcode}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Address):
            return False
        return (
            self.address_line == other.address_line and
            self.town_city == other.town_city and
            self.postcode == other.postcode
        )
