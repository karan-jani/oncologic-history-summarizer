from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field


class Diagnosis(BaseModel):
    primary_malignancy: str = Field(
        default="not specified",
        description="only the primary malignancy",
    )
    stage: str = Field(
        default="not specified",
        description="TNM staging information, not specified if unknown",
    )


class Metastases(BaseModel):
    known: list[str] = Field(
        default_factory=list,
        description="only includes known sites of metastatic disease for the primary malignancy",
    )
    suspected_possible: list[str] = Field(
        default_factory=list,
        description="possible metastases including sites of possible recurrence",
    )


class SystemicTherapy(BaseModel):
    drug: str = Field(..., description="name of the drug")
    drug_class: Literal[
        "chemotherapy",
        "immunotherapy",
        "radiopharmaceutical",
        "hormonal therapy",
        "targeted therapy",
    ] = Field(
        ...,
        description="class of drug (chemotherapy, immunotherapy, radiopharmaceutical, hormonal therapy, or targeted therapy)",
    )
    treatment_status: bool = Field(
        ...,
        description="true if patient is currently being treated with drug and false if not",
    )
    start_date: str = Field(
        ...,
        description="date of drug initiation, not specified if unknown",
    )
    end_date: str = Field(
        ...,
        description="date of drug completion, not specified if unknown or ongoing",
    )


class RadiationTherapy(BaseModel):
    site_of_radiation: str = Field(
        ...,
        description="includes sites of previous radiation therapy, which may be abbreviated as SBRT",
    )
    last_radiation_date: str = Field(..., description="last date of radiation to site")


class SurgeryHistory(BaseModel):
    procedure_type: str = Field(..., description="name of surgery")
    date_of_procedure: str = Field(..., description="date of procedure, not specified if unknown")


class StructuredOncSummary(BaseModel):
    diagnosis: Diagnosis
    metastatic_sites: Metastases
    radiation_therapy: list[RadiationTherapy] = Field(default_factory=list)
    systemic_therapy: list[SystemicTherapy] = Field(default_factory=list)
    surgical_history: list[SurgeryHistory] = Field(
        default_factory=list,
        description="only includes any previous surgeries",
    )
    findings_for_followup: list[str] = Field(
        default_factory=list,
        description="pertinent primary cancer related findings only in previous medical imaging and radiology reports",
    )


class StructuredOncSummaries(BaseModel):
    onc_summary: list[StructuredOncSummary] = Field(
        default_factory=list,
        description="list of structured summaries for each unique malignancy",
    )


class SummaryContext(BaseModel):
    context: str = Field(
        ...,
        description="contains history of cancer diagnosis, staging, previous surgeries, treatment, and radiology findings to followup. May contain multiple primary cancers",
    )
    date: str = Field(..., description="date of the clinical or radiology note")
