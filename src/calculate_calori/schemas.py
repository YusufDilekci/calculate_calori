import ast
import json
import re

from pydantic import BaseModel, Field, ValidationError


class KaloriAraligi(BaseModel):
    min: float
    max: float

    def __str__(self) -> str:
        if self.min == self.max:
            return f"{self.min:g} kcal"
        return f"{self.min:g}–{self.max:g} kcal"


class Oge(BaseModel):
    ad: str
    porsiyon: str = "-"
    kalori_kcal: KaloriAraligi
    protein_g: float = 0
    karbonhidrat_g: float = 0
    yag_g: float = 0
    guven: str = "-"


class Toplam(BaseModel):
    kalori_kcal: KaloriAraligi
    protein_g: float = 0
    karbonhidrat_g: float = 0
    yag_g: float = 0


class AnalizSonucu(BaseModel):
    ogeler: list[Oge] = Field(default_factory=list)
    toplam: Toplam
    varsayimlar: list[str] = Field(default_factory=list)
    netlestirme_sorusu: str | None = None

    def to_markdown(self) -> str:
        t = self.toplam
        lines = [
            f"## 🔥 Toplam: {t.kalori_kcal}",
            f"**Protein:** {t.protein_g:g} g · **Karbonhidrat:** {t.karbonhidrat_g:g} g · **Yağ:** {t.yag_g:g} g",
        ]
        if self.ogeler:
            lines += [
                "",
                "### Öğeler",
                "| Yiyecek | Porsiyon | Kalori | Protein | Karb. | Yağ | Güven |",
                "|---|---|---|---|---|---|---|",
            ]
            for o in self.ogeler:
                lines.append(
                    f"| {o.ad} | {o.porsiyon} | {o.kalori_kcal} | {o.protein_g:g} g "
                    f"| {o.karbonhidrat_g:g} g | {o.yag_g:g} g | {o.guven} |"
                )
        if self.varsayimlar:
            lines += ["", "### Varsayımlar", *[f"- {v}" for v in self.varsayimlar]]
        if self.netlestirme_sorusu:
            lines += ["", f"> ❓ {self.netlestirme_sorusu}"]
        lines += ["", "*Değerler tahminidir; tıbbi tavsiye değildir.*"]
        return "\n".join(lines)


def parse_sonuc(text: str) -> AnalizSonucu | None:

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    raw = match.group(0)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        try:
            data = ast.literal_eval(raw)
        except (ValueError, SyntaxError):
            return None
    try:
        return AnalizSonucu.model_validate(data)
    except ValidationError:
        return None
