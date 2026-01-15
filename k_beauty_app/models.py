from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Integer, Float, ForeignKey

class Base(DeclarativeBase):
    pass

class AgeRanges(Base):
    __tablename__ = "AGE_RANGES"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}')"

class SkinType(Base):
    __tablename__ = "SKIN_TYPES"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    advice: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}', advice = '{self.advice}')"

class Concerns(Base):
    __tablename__ = "CONCERNS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}')"

class RuntimeSteps(Base):
    __tablename__ = "ROUTINE_STEPS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}', sequence = '{self.sequence})"
    
class Products(Base):
    __tablename__ = "PRODUCTS"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(100))
    rating: Mapped[float] = mapped_column(Float)

    skin_type_id: Mapped[int] = mapped_column(ForeignKey("SKIN_TYPES.id"))
    concern_id: Mapped[int] = mapped_column(ForeignKey("CONCERNS.id"))
    age_range_id: Mapped[int] = mapped_column(ForeignKey("AGE_RANGES.id"))
    step_id: Mapped[int] = mapped_column(ForeignKey("ROUTINE_STEPS.id"))

    step: Mapped["RuntimeSteps"] = relationship()
    skin_type: Mapped["SkinType"] = relationship()

    def __repr__(self) -> str:
        return f"Skin_Type(id={self.id}, name='{self.name}',brand='{self.brand}',rating='{self.rating}', skin_type_id='{self.skin_type_id}')"