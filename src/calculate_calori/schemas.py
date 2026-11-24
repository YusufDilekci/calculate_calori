from pydantic import BaseModel, Field, ValidationError


class CalorieRange(BaseModel):
    min: float
    max: float

    def __str__(self) -> str:
        if self.min == self.max:
            return f"{self.min:g} kcal"
        return f"{self.min:g}–{self.max:g} kcal"


class FoodItem(BaseModel):
    name: str
    portion: str = "-"
    calories_kcal: CalorieRange
    protein_g: float = 0
    carbs_g: float = 0
    fat_g: float = 0
    confidence: str = "-"


class Totals(BaseModel):
    calories_kcal: CalorieRange
    protein_g: float = 0
    carbs_g: float = 0
    fat_g: float = 0


class AnalysisResult(BaseModel):
    items: list[FoodItem] = Field(default_factory=list)
    total: Totals
    assumptions: list[str] = Field(default_factory=list)
    clarifying_question: str | None = None

    def to_markdown(self) -> str:
        t = self.total
        lines = [
            f"## 🔥 Toplam: {t.calories_kcal}",
            f"**Protein:** {t.protein_g:g} g · **Karbonhidrat:** {t.carbs_g:g} g · **Yağ:** {t.fat_g:g} g",
        ]
        if self.items:
            lines += [
                "",
                "### Öğeler",
                "| Yiyecek | Porsiyon | Kalori | Protein | Karb. | Yağ | Güven |",
                "|---|---|---|---|---|---|---|",
            ]
            for item in self.items:
                lines.append(
                    f"| {item.name} | {item.portion} | {item.calories_kcal} | {item.protein_g:g} g "
                    f"| {item.carbs_g:g} g | {item.fat_g:g} g | {item.confidence} |"
                )
        if self.assumptions:
            lines += ["", "### Varsayımlar", *[f"- {a}" for a in self.assumptions]]
        if self.clarifying_question:
            lines += ["", f"> ❓ {self.clarifying_question}"]
        lines += ["", "*Değerler tahminidir; tıbbi tavsiye değildir.*"]
        return "\n".join(lines)



