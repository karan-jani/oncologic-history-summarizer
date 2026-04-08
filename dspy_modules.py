from __future__ import annotations

import dspy
from pydantic import RootModel

from schemas import StructuredOncSummary, SummaryContext


class OncSummaryList(RootModel[list[StructuredOncSummary]]):
    pass

class RAGSummaryGeneration(dspy.Signature):
    """Extract a structured oncologic summary. If not found, return 'not specified'"""

    context: list[SummaryContext] = dspy.InputField(desc="List of clinical notes and their dates")
    primary_cancer: int = dspy.OutputField(desc="number of primary cancers in the patient")
    onc_summary: OncSummaryList = dspy.OutputField(
        desc="List of structured summaries per primary cancer with the most updated information"
    )
