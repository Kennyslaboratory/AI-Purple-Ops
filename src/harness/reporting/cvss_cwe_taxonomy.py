"""CVSS/CWE taxonomy system for AI vulnerability classification.

Provides CVSS v3.1 scoring, CWE mappings, OWASP LLM Top 10, and MITRE ATLAS
technique mappings for AI/LLM vulnerabilities.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class VulnerabilitySeverity(Enum):
    """Vulnerability severity levels."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class CVSSScore:
    """CVSS v3.1 Score representation.
    
    Attributes:
        base_score: CVSS base score (0.0-10.0)
        attack_vector: Attack Vector (N=Network, A=Adjacent, L=Local, P=Physical)
        attack_complexity: Attack Complexity (L=Low, H=High)
        privileges_required: Privileges Required (N=None, L=Low, H=High)
        user_interaction: User Interaction (N=None, R=Required)
        scope: Scope (U=Unchanged, C=Changed)
        confidentiality: Confidentiality Impact (N=None, L=Low, H=High)
        integrity: Integrity Impact (N=None, L=Low, H=High)
        availability: Availability Impact (N=None, L=Low, H=High)
    """
    
    base_score: float
    attack_vector: str  # N, A, L, P
    attack_complexity: str  # L, H
    privileges_required: str  # N, L, H
    user_interaction: str  # N, R
    scope: str  # U, C
    confidentiality: str  # N, L, H
    integrity: str  # N, L, H
    availability: str  # N, L, H
    
    @property
    def vector_string(self) -> str:
        """Generate CVSS vector string."""
        return (
            f"CVSS:3.1/"
            f"AV:{self.attack_vector}/"
            f"AC:{self.attack_complexity}/"
            f"PR:{self.privileges_required}/"
            f"UI:{self.user_interaction}/"
            f"S:{self.scope}/"
            f"C:{self.confidentiality}/"
            f"I:{self.integrity}/"
            f"A:{self.availability}"
        )


# Vulnerability type to CWE/CVSS/OWASP/MITRE mappings
VULNERABILITY_TAXONOMY: dict[str, dict[str, Any]] = {
    "prompt_injection": {
        "cwe_id": "CWE-77",
        "cwe_name": "Improper Neutralization of Special Elements used in a Command ('Command Injection')",
        "owasp_llm": "LLM01:2025 - Prompt Injection",
        "mitre_atlas": "AML.T0051 - LLM Prompt Injection",
        "cvss": CVSSScore(
            base_score=8.1,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="H",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.HIGH,
        "description": "Attacker manipulates LLM behavior through crafted input prompts",
    },
    "jailbreak": {
        "cwe_id": "CWE-863",
        "cwe_name": "Incorrect Authorization",
        "owasp_llm": "LLM01:2025 - Prompt Injection",
        "mitre_atlas": "AML.T0054 - LLM Jailbreak",
        "cvss": CVSSScore(
            base_score=7.5,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="L",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.HIGH,
        "description": "Bypass of safety guardrails and content policy restrictions",
    },
    "tool_misuse": {
        "cwe_id": "CWE-285",
        "cwe_name": "Improper Authorization",
        "owasp_llm": "LLM07:2025 - System Prompt Leakage",
        "mitre_atlas": "AML.T0054 - LLM Jailbreak",
        "cvss": CVSSScore(
            base_score=8.8,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="H",
            availability="H",
        ),
        "severity": VulnerabilitySeverity.CRITICAL,
        "description": "Unauthorized or malicious use of tool calling capabilities",
    },
    "data_exfiltration": {
        "cwe_id": "CWE-200",
        "cwe_name": "Exposure of Sensitive Information to an Unauthorized Actor",
        "owasp_llm": "LLM06:2025 - Sensitive Information Disclosure",
        "mitre_atlas": "AML.T0024 - Exfiltration via ML Model",
        "cvss": CVSSScore(
            base_score=7.5,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="N",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.HIGH,
        "description": "Extraction of sensitive training data or system information",
    },
    "rag_poisoning": {
        "cwe_id": "CWE-502",
        "cwe_name": "Deserialization of Untrusted Data",
        "owasp_llm": "LLM03:2025 - Training Data Poisoning",
        "mitre_atlas": "AML.T0018 - Backdoor Attack",
        "cvss": CVSSScore(
            base_score=9.8,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="H",
            availability="H",
        ),
        "severity": VulnerabilitySeverity.CRITICAL,
        "description": "Injection of malicious data into RAG knowledge base",
    },
    "indirect_injection": {
        "cwe_id": "CWE-94",
        "cwe_name": "Improper Control of Generation of Code ('Code Injection')",
        "owasp_llm": "LLM01:2025 - Prompt Injection",
        "mitre_atlas": "AML.T0051 - LLM Prompt Injection",
        "cvss": CVSSScore(
            base_score=8.6,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="R",
            scope="C",
            confidentiality="H",
            integrity="H",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.HIGH,
        "description": "Malicious instructions embedded in external content (RAG, web pages)",
    },
    "model_denial_of_service": {
        "cwe_id": "CWE-400",
        "cwe_name": "Uncontrolled Resource Consumption",
        "owasp_llm": "LLM04:2025 - Model Denial of Service",
        "mitre_atlas": "AML.T0029 - Denial of ML Service",
        "cvss": CVSSScore(
            base_score=5.3,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="N",
            integrity="N",
            availability="L",
        ),
        "severity": VulnerabilitySeverity.MEDIUM,
        "description": "Resource exhaustion through expensive queries or context overflow",
    },
    "supply_chain": {
        "cwe_id": "CWE-1357",
        "cwe_name": "Reliance on Insufficiently Trustworthy Component",
        "owasp_llm": "LLM05:2025 - Supply Chain Vulnerabilities",
        "mitre_atlas": "AML.T0010 - ML Supply Chain Compromise",
        "cvss": CVSSScore(
            base_score=8.1,
            attack_vector="N",
            attack_complexity="H",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="H",
            availability="H",
        ),
        "severity": VulnerabilitySeverity.HIGH,
        "description": "Compromise through third-party models, plugins, or datasets",
    },
    "insecure_output_handling": {
        "cwe_id": "CWE-79",
        "cwe_name": "Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')",
        "owasp_llm": "LLM02:2025 - Insecure Output Handling",
        "mitre_atlas": "AML.T0051 - LLM Prompt Injection",
        "cvss": CVSSScore(
            base_score=6.1,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="R",
            scope="C",
            confidentiality="L",
            integrity="L",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.MEDIUM,
        "description": "LLM output used unsafely in web pages or system commands",
    },
    "excessive_agency": {
        "cwe_id": "CWE-269",
        "cwe_name": "Improper Privilege Management",
        "owasp_llm": "LLM08:2025 - Excessive Agency",
        "mitre_atlas": "AML.T0054 - LLM Jailbreak",
        "cvss": CVSSScore(
            base_score=7.3,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="L",
            integrity="H",
            availability="L",
        ),
        "severity": VulnerabilitySeverity.HIGH,
        "description": "LLM granted excessive permissions or autonomy",
    },
    "overreliance": {
        "cwe_id": "CWE-1395",
        "cwe_name": "Dependency on Vulnerable Third-Party Component",
        "owasp_llm": "LLM09:2025 - Overreliance",
        "mitre_atlas": "AML.T0043 - Model Evasion",
        "cvss": CVSSScore(
            base_score=4.3,
            attack_vector="N",
            attack_complexity="L",
            privileges_required="N",
            user_interaction="R",
            scope="U",
            confidentiality="L",
            integrity="L",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.MEDIUM,
        "description": "Excessive trust in LLM outputs without verification",
    },
    "model_theft": {
        "cwe_id": "CWE-506",
        "cwe_name": "Embedded Malicious Code",
        "owasp_llm": "LLM10:2025 - Model Theft",
        "mitre_atlas": "AML.T0024 - Exfiltration via ML Model",
        "cvss": CVSSScore(
            base_score=5.9,
            attack_vector="N",
            attack_complexity="H",
            privileges_required="N",
            user_interaction="N",
            scope="U",
            confidentiality="H",
            integrity="N",
            availability="N",
        ),
        "severity": VulnerabilitySeverity.MEDIUM,
        "description": "Unauthorized extraction of model weights or architecture",
    },
}


class VulnerabilityClassifier:
    """Classify vulnerabilities and assign CVSS/CWE/OWASP LLM/MITRE ATLAS mappings.
    
    Example:
        >>> classifier = VulnerabilityClassifier()
        >>> taxonomy = classifier.classify("prompt_injection")
        >>> print(taxonomy["cvss"].base_score)  # 8.1
        >>> print(taxonomy["owasp_llm"])  # LLM01:2025 - Prompt Injection
    """
    
    def classify(self, vulnerability_type: str) -> dict[str, Any]:
        """Get taxonomy data for a vulnerability type.
        
        Args:
            vulnerability_type: Type of vulnerability (e.g., "prompt_injection")
            
        Returns:
            Dictionary containing CWE ID, CVSS score, OWASP LLM mapping, etc.
        """
        if vulnerability_type not in VULNERABILITY_TAXONOMY:
            return self._default_classification()
        
        return VULNERABILITY_TAXONOMY[vulnerability_type]
    
    def _default_classification(self) -> dict[str, Any]:
        """Default classification for unknown vulnerability types."""
        return {
            "cwe_id": "CWE-693",
            "cwe_name": "Protection Mechanism Failure",
            "owasp_llm": "Unknown",
            "mitre_atlas": "Unknown",
            "cvss": CVSSScore(
                base_score=5.0,
                attack_vector="N",
                attack_complexity="L",
                privileges_required="N",
                user_interaction="R",
                scope="U",
                confidentiality="L",
                integrity="L",
                availability="N",
            ),
            "severity": VulnerabilitySeverity.MEDIUM,
            "description": "Unknown vulnerability type",
        }
    
    def get_severity_from_cvss(self, cvss_score: float) -> VulnerabilitySeverity:
        """Determine severity level from CVSS base score.
        
        Args:
            cvss_score: CVSS v3.1 base score (0.0-10.0)
            
        Returns:
            VulnerabilitySeverity enum value
        """
        if cvss_score >= 9.0:
            return VulnerabilitySeverity.CRITICAL
        elif cvss_score >= 7.0:
            return VulnerabilitySeverity.HIGH
        elif cvss_score >= 4.0:
            return VulnerabilitySeverity.MEDIUM
        elif cvss_score >= 0.1:
            return VulnerabilitySeverity.LOW
        else:
            return VulnerabilitySeverity.INFO
    
    def list_all_vulnerabilities(self) -> list[str]:
        """List all supported vulnerability types.
        
        Returns:
            List of vulnerability type identifiers
        """
        return list(VULNERABILITY_TAXONOMY.keys())

