from crewai.tools import BaseTool
from typing import Type, ClassVar
from pydantic import BaseModel, Field

class ClassifyReportInput(BaseModel):
    """Input schema for classifying medical report type."""
    raw_input: str = Field(..., description="Le texte médical brut à classifier.")

class MedicalReportClassifierTool(BaseTool):
    # Le nom de l’outil doit correspondre à la tâche `determine_report_type`
    name: str = "determine_report_type"
    description: str = (
        "Détermine le type de rapport IRM (p.ex., 'irm_hepatique', 'irm_genou') "
        "à partir du texte médical brut."
    )
    args_schema: Type[BaseModel] = ClassifyReportInput
    tool_name: ClassVar[str] = "determine_report_type"

    def _run(self, raw_input: str) -> str:
        """Classifie le type de rapport médical basé sur le texte d’entrée."""
        report_type_keywords = {
            "irm_hepatique": ["foie", "hépatique", "liver", "hepatic", "biliaire", "cholangio-irm", "bili-irm"],
            "irm_genou": ["genou", "knee", "ménisque", "ménisques", "ligament croisé", "lca", "lcp", "tibia", "fémur"],
            # … vos autres mappings …
        }

        normalized = raw_input.lower()
        scores = {}
        for rpt, keys in report_type_keywords.items():
            scores[rpt] = sum(normalized.count(k) for k in keys)
        # Choix du meilleur score
        best = max(scores.items(), key=lambda x: x[1]) if any(scores.values()) else ("irm_general", 0)
        return best[0]
