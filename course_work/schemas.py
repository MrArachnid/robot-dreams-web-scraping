from dataclasses import dataclass, field


@dataclass
class Course:
    url: str
    name: str = None
    short_descr: str = None
    full_descr: str = None
    lector_name: str = None
    lector_pos: str = None
    lector_img: str = None
    program: list[str] = field(default_factory=list)