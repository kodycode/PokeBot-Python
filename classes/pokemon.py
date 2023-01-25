from dataclasses import dataclass

@dataclass
class Pokemon:
    name: str
    img_path: str
    is_legendary: bool=False
    is_shiny: bool=False
    is_ultra_beast: bool=False
