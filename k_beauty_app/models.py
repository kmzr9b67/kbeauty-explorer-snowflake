from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float

class Age_Ranges(DeclarativeBase):
    __tablename__ = "AGE_RANGES"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}')"

class Skin_Type(DeclarativeBase):
    __tablename__ = "SKIN_TYPES"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    advice: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}', advice = '{self.advice}')"

class Concerns(DeclarativeBase):
    __tablename__ = "CONCERNS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}')"

class Runtime_Steps(DeclarativeBase):
    __tablename__ = "ROUTINE_STEPS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}', sequence = '{self.sequence})"
    
class Products(DeclarativeBase):
    __tablename__ = "PRODUCTS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(100))
    rating: Mapped[int] = mapped_column(Float)
    skin_type_id: Mapped[int] = mapped_column(Integer)
    concern_id: Mapped[int] = mapped_column(Integer)
    age_range_id: Mapped[int] = mapped_column(Integer)
    step_id: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}',brand='{self.brand}',rating='{self.rating}', skin_type_id='{self.skin_type_id}')"