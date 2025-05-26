from crewai.tools import BaseTool
from typing import Type, List, Dict, Optional
from pydantic import BaseModel, Field, PrivateAttr
import os, re
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

FRENCH_STOPWORDS = [ ... ]  # inchangé

class RetrieveReportsInput(BaseModel):
    """Input schema for retrieving similar medical reports."""
    raw_input: str = Field(..., description="Le texte médical brut servant de requête.")
    report_type: str = Field(
        ...,
        description="Le type de rapport à récupérer (p.ex. 'irm_hepatique').",
    )
    top_k: int = Field(3, description="Nombre de rapports à renvoyer (par défaut 3).")

class RAGMedicalReportsTool(BaseTool):
    name: str = "retrieve_similar_reports"
    description: str = (
        "Récupère des rapports médicaux similaires pour servir de référence."
    )
    args_schema: Type[BaseModel] = RetrieveReportsInput
    knowledge_base_path: Path = Field(default_factory=lambda: Path("knowledge/reports/training"))
    _vectorizer: TfidfVectorizer = PrivateAttr(default_factory=lambda: TfidfVectorizer(stop_words=FRENCH_STOPWORDS))
    _reports_cache: dict = PrivateAttr(default_factory=dict)

    def __init__(self, knowledge_base_path: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if knowledge_base_path:
            self.knowledge_base_path = Path(knowledge_base_path)

    # … (toutes les méthodes internes _read_report, _get_all_reports, etc. restent identiques) …

    def _run(self, raw_input: str, report_type: str, top_k: int = 3) -> str:
        """
        raw_input  : le texte médical brut servant de requête
        report_type: le type de rapport issu de la tâche précédente
        top_k      : nombre maximum de rapports à retourner
        """
        # Utilisez raw_input comme query
        all_reports      = self._get_all_reports()
        filtered_reports = self._filter_reports_by_type(all_reports, report_type)
        if not filtered_reports:
            return f"Aucun rapport pour le type « {report_type} »."
        similar = self._calculate_similarity(raw_input, filtered_reports)
        top     = similar[:top_k]

        # formatage identique à avant
        output = [f"Retrieved {len(top)} similar reports for input."]
        for i, rpt in enumerate(top, 1):
            output.append(f"--- Report {i} ---")
            output.append(self._format_report_for_output(rpt))
        return "\n".join(output)
