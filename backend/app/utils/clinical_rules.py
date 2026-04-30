"""
Clinical decision rule engine for EGFR-mutant NSCLC

Implements evidence-based treatment recommendations from clinical trials:
- FLAURA (Osimertinib 1st-line)
- AURA3 (T790M resistance)
- GEOMETRY-E1 (MET amplification)
- TATTON (Combination therapy)
- ORCHARD (C797S resistance)
"""
from typing import List, Dict, Any


def get_recommendations(
    patient_data: Dict[str, Any],
    mutations: List[Dict[str, Any]],
    treatments: List[Dict[str, Any]],
    current_stage: str
) -> List[Dict[str, Any]]:
    """
    Generate treatment recommendations based on clinical guidelines

    Args:
        patient_data: Patient demographics and baseline data
        mutations: List of mutations with flags (is_primary_driver, resistance_mutation, etc.)
        treatments: List of treatments ordered by treatment_line
        current_stage: Current AJCC stage

    Returns:
        List of recommendation dictionaries with evidence
    """
    recommendations = []

    # Extract mutation information
    has_egfr_ex19del = any(
        m.get('gene_symbol') == 'EGFR' and 'Ex19del' in m.get('mutation_type', '')
        for m in mutations
    )
    has_egfr_l858r = any(
        m.get('gene_symbol') == 'EGFR' and 'L858R' in m.get('mutation_type', '')
        for m in mutations
    )
    has_t790m = any(
        m.get('gene_symbol') == 'EGFR' and 'T790M' in m.get('mutation_type', '')
        for m in mutations
    )
    has_c797s = any(
        m.get('gene_symbol') == 'EGFR' and 'C797S' in m.get('mutation_type', '')
        for m in mutations
    )
    has_met_amp = any(
        m.get('gene_symbol') == 'MET' and 'Amplification' in m.get('mutation_type', '')
        for m in mutations
    )

    # Get current treatment
    current_treatment = treatments[-1] if treatments else None
    current_drug = current_treatment.get('drug_name', '') if current_treatment else ''

    # Identify resistance mutations
    resistance_mutations = [
        m for m in mutations
        if m.get('resistance_mutation') or m.get('is_acquired_resistance')
    ]

    # Rule 1: EGFR Ex19del/L858R + Advanced stage → Osimertinib (FLAURA)
    if (has_egfr_ex19del or has_egfr_l858r) and current_stage in ['IIIB', 'IIIC', 'IVA', 'IVB']:
        if not current_drug or 'Osimertinib' not in current_drug:
            recommendations.append({
                "recommendation_id": "REC-FLAURA-1L",
                "recommendation": "First-line osimertinib 80mg once daily",
                "rationale": "EGFR-sensitizing mutation (Ex19del or L858R) detected in advanced-stage NSCLC",
                "evidence_level": "Level I (Randomized Controlled Trial)",
                "guideline_reference": "FLAURA trial (Soria et al., NEJM 2018); NICE TA653 (2020)",
                "confidence": "High",
                "applicable": True,
                "priority": "High",
                "supporting_data": {
                    "mutation_type": "Ex19del" if has_egfr_ex19del else "L858R",
                    "stage": current_stage,
                    "trial_pfs": "18.9 months vs 10.2 months (HR 0.46)",
                    "current_treatment": current_drug or "None"
                }
            })

    # Rule 2: T790M resistance on 1st/2nd-gen TKI → Switch to osimertinib (AURA3)
    if has_t790m:
        on_first_gen_tki = any(
            drug in current_drug.lower()
            for drug in ['gefitinib', 'erlotinib', 'afatinib', 'icotinib']
        )

        if on_first_gen_tki or (current_drug and 'Osimertinib' not in current_drug):
            recommendations.append({
                "recommendation_id": "REC-AURA3-T790M",
                "recommendation": "Switch to osimertinib 80mg once daily",
                "rationale": "T790M resistance mutation detected after progression on EGFR TKI",
                "evidence_level": "Level I (Randomized Controlled Trial)",
                "guideline_reference": "AURA3 trial (Mok et al., NEJM 2017); NICE TA653 (2020)",
                "confidence": "High",
                "applicable": True,
                "priority": "High",
                "supporting_data": {
                    "resistance_mutation": "T790M",
                    "current_treatment": current_drug,
                    "trial_pfs": "10.1 months vs 4.4 months chemo (HR 0.30)"
                }
            })

    # Rule 3: MET amplification → Add MET inhibitor (GEOMETRY-E1, TATTON)
    if has_met_amp:
        # Check if already on osimertinib
        on_osimertinib = 'Osimertinib' in current_drug

        if on_osimertinib and 'Savolitinib' not in current_drug and 'Tepotinib' not in current_drug:
            recommendations.append({
                "recommendation_id": "REC-MET-AMP",
                "recommendation": "Consider adding MET inhibitor (Tepotinib or Savolitinib) to osimertinib",
                "rationale": "MET amplification detected as acquired resistance mechanism. Combination therapy addresses dual resistance pathway.",
                "evidence_level": "Level II (Phase II trial)",
                "guideline_reference": "GEOMETRY-E1 trial (Wu et al., Lancet Resp Med 2023); TATTON trial (Oxnard et al., JTO 2020)",
                "confidence": "Moderate",
                "applicable": True,
                "priority": "High",
                "supporting_data": {
                    "resistance_mutations": ["MET amplification"],
                    "current_treatment": current_drug,
                    "trial_orr": "64% (TATTON), 60% (GEOMETRY-E1)",
                    "note": "EU approved, off-label in UK as of 2024"
                }
            })
        elif not on_osimertinib:
            recommendations.append({
                "recommendation_id": "REC-MET-AMP-START",
                "recommendation": "Consider osimertinib + MET inhibitor combination",
                "rationale": "MET amplification detected. Upfront combination may be more effective than sequential therapy.",
                "evidence_level": "Level II (Phase II trial)",
                "guideline_reference": "GEOMETRY-E1 trial (Wu et al., Lancet Resp Med 2023)",
                "confidence": "Moderate",
                "applicable": True,
                "priority": "High",
                "supporting_data": {
                    "resistance_mutations": ["MET amplification"],
                    "current_treatment": current_drug or "None"
                }
            })

    # Rule 4: T790M + MET amplification → Dual combination (TATTON)
    if has_t790m and has_met_amp:
        recommendations.append({
            "recommendation_id": "REC-DUAL-RES",
            "recommendation": "Continue third-generation EGFR TKI with MET inhibitor combination",
            "rationale": "T790M co-exists with MET amplification - dual resistance mechanism requires combination therapy",
            "evidence_level": "Level II (Phase II trial)",
            "guideline_reference": "TATTON trial (Oxnard et al., JTO 2020)",
            "confidence": "Moderate",
            "applicable": True,
            "priority": "High",
            "supporting_data": {
                "resistance_mutations": ["T790M", "MET amplification"],
                "t790m_detected": has_t790m,
                "met_amplification": has_met_amp,
                "current_treatment": current_drug
            }
        })

    # Rule 5: C797S resistance → No targeted therapy (ORCHARD)
    if has_c797s:
        recommendations.append({
            "recommendation_id": "REC-C797S",
            "recommendation": "Platinum-doublet chemotherapy (carboplatin + pemetrexed) OR clinical trial",
            "rationale": "C797S mutation confers resistance to all EGFR TKIs. No approved targeted therapy available.",
            "evidence_level": "Level IV (Expert opinion)",
            "guideline_reference": "ORCHARD trial (Planchard et al., Lancet Oncol 2024); ESMO Guidelines 2023",
            "confidence": "Low",
            "applicable": True,
            "priority": "Medium",
            "supporting_data": {
                "resistance_mutation": "C797S",
                "c797s_mechanism": "Blocks drug binding to ATP pocket",
                "current_treatment": current_drug,
                "note": "Consider 4th-generation EGFR inhibitors in clinical trials"
            }
        })

    # Rule 6: Advanced stage with no active treatment → MDT discussion
    if current_stage in ['IVA', 'IVB'] and not current_drug:
        recommendations.append({
            "recommendation_id": "REC-MDT",
            "recommendation": "Urgent MDT discussion for treatment initiation",
            "rationale": "Advanced-stage disease without active systemic therapy",
            "evidence_level": "Standard of care",
            "guideline_reference": "UK NICE Guidelines",
            "confidence": "High",
            "applicable": True,
            "priority": "Urgent",
            "supporting_data": {
                "stage": current_stage,
                "mutations_detected": len([m for m in mutations if m.get('actionable_mutation')])
            }
        })

    return recommendations


def generate_alerts_from_mutations(
    mutations: List[Dict[str, Any]],
    treatments: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate clinical alerts based on mutation profile

    Args:
        mutations: List of mutations
        treatments: List of treatments

    Returns:
        List of alert dictionaries
    """
    alerts = []

    # Detect new resistance mutations
    resistance_mutations = [
        m for m in mutations
        if m.get('resistance_mutation') or m.get('is_acquired_resistance')
    ]

    if resistance_mutations:
        mutation_list = [f"{m['gene_symbol']} {m['mutation_type']}" for m in resistance_mutations]
        alerts.append({
            "alert_id": "ALR-RES-001",
            "alert_type": "resistance_mutation_detected",
            "severity": "High",
            "message": f"Acquired resistance mutations detected: {', '.join(mutation_list)}",
            "trigger_date": resistance_mutations[-1].get('test_date'),
            "requires_action": True,
            "action_recommendation": "Re-biopsy performed. Consider targeted therapy per resistance mechanism or clinical trial enrollment.",
            "supporting_data": {
                "resistance_mutations": [
                    {
                        "gene": m['gene_symbol'],
                        "mutation": m['mutation_type'],
                        "vaf_percent": m.get('vaf_percent')
                    }
                    for m in resistance_mutations
                ],
                "detection_timepoint": resistance_mutations[-1].get('detection_timepoint')
            }
        })

    return alerts