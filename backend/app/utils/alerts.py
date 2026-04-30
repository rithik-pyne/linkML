"""
Alert generation engine for clinical monitoring

Implements alert logic based on:
- CHRYSALIS-2: VAF ≥2x from nadir predicts progression
- Standard care: Overdue imaging (>84 days)
- Resistance mutation detection
"""
from typing import List, Dict, Any
from datetime import datetime, timedelta


def calculate_vaf_alerts(
    mutations: List[Dict[str, Any]],
    molecular_tests: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate alerts for rising ctDNA VAF (≥2x from nadir)

    Args:
        mutations: List of mutations with VAF data
        molecular_tests: List of molecular tests with dates

    Returns:
        List of VAF alert dictionaries
    """
    alerts = []

    # Group mutations by gene + mutation type to track over time
    mutation_tracking = {}

    for mut in mutations:
        key = f"{mut.get('gene_symbol')}_{mut.get('mutation_type')}"

        if key not in mutation_tracking:
            mutation_tracking[key] = []

        mutation_tracking[key].append({
            "gene_symbol": mut.get('gene_symbol'),
            "mutation_type": mut.get('mutation_type'),
            "vaf_percent": mut.get('vaf_percent'),
            "test_date": mut.get('test_date'),
            "specimen_source": mut.get('specimen_source'),
            "is_primary_driver": mut.get('is_primary_driver')
        })

    # Check each mutation track for rising VAF
    for key, track in mutation_tracking.items():
        # Need at least 2 timepoints
        if len(track) < 2:
            continue

        # Sort by date
        track.sort(key=lambda x: x['test_date'] if x['test_date'] else '')

        # Find nadir (minimum VAF)
        vaf_values = [t['vaf_percent'] for t in track if t['vaf_percent'] is not None]
        if not vaf_values:
            continue

        nadir_vaf = min(vaf_values)
        current_vaf = track[-1]['vaf_percent']  # Latest value

        if current_vaf is None or nadir_vaf is None or nadir_vaf == 0:
            continue

        # Calculate fold change
        fold_change = current_vaf / nadir_vaf

        # Alert if ≥2x increase (CHRYSALIS-2 threshold)
        if fold_change >= 2.0:
            # Find nadir date
            nadir_entry = next((t for t in track if t['vaf_percent'] == nadir_vaf), None)

            alerts.append({
                "alert_id": f"ALR-VAF-{key}",
                "alert_type": "rising_ctdna_vaf",
                "severity": "High",
                "message": f"ctDNA VAF increased {fold_change:.1f}x from nadir ({nadir_vaf:.2f}% → {current_vaf:.2f}%)",
                "trigger_date": track[-1]['test_date'],
                "requires_action": True,
                "action_recommendation": "Molecular progression detected. Consider repeat imaging in 4-6 weeks (CHRYSALIS-2 precedent: VAF rise precedes radiographic progression by ~4 months).",
                "supporting_data": {
                    "gene_symbol": track[-1]['gene_symbol'],
                    "mutation_type": track[-1]['mutation_type'],
                    "nadir_vaf": nadir_vaf,
                    "nadir_date": nadir_entry['test_date'] if nadir_entry else None,
                    "current_vaf": current_vaf,
                    "current_date": track[-1]['test_date'],
                    "fold_change": round(fold_change, 1),
                    "threshold": 2.0,
                    "specimen_source": track[-1]['specimen_source']
                }
            })

    return alerts


def calculate_overdue_imaging_alerts(
    imaging_studies: List[Dict[str, Any]],
    current_stage: str
) -> List[Dict[str, Any]]:
    """
    Generate alerts for overdue imaging (>84 days since last scan)

    Args:
        imaging_studies: List of imaging studies with dates
        current_stage: Current AJCC stage

    Returns:
        List of overdue imaging alert dictionaries
    """
    alerts = []

    if not imaging_studies:
        return alerts

    # Sort by date
    imaging_studies.sort(key=lambda x: x.get('scan_date', ''), reverse=True)
    latest_scan = imaging_studies[0]

    try:
        # Parse scan date
        scan_date_str = latest_scan.get('scan_date')
        if not scan_date_str:
            return alerts

        # Handle different date formats
        if 'T' in scan_date_str:
            scan_date = datetime.fromisoformat(scan_date_str.replace('Z', '+00:00'))
        else:
            scan_date = datetime.strptime(scan_date_str, '%Y-%m-%d')

        # Calculate days since last scan
        days_since_scan = (datetime.now() - scan_date).days

        # Alert threshold: 84 days (12 weeks)
        if days_since_scan > 84:
            # Adjust severity based on stage
            severity = "High" if current_stage in ['IVA', 'IVB'] else "Medium"

            alerts.append({
                "alert_id": "ALR-IMG-OVERDUE",
                "alert_type": "overdue_imaging",
                "severity": severity,
                "message": f"Imaging overdue: {days_since_scan} days since last scan (standard interval: 12 weeks)",
                "trigger_date": scan_date_str,
                "requires_action": True,
                "action_recommendation": "Schedule CT chest/abdomen or PET-CT per standard surveillance protocol.",
                "supporting_data": {
                    "last_scan_date": scan_date_str,
                    "days_since_scan": days_since_scan,
                    "threshold_days": 84,
                    "last_modality": latest_scan.get('imaging_modality'),
                    "current_stage": current_stage
                }
            })
    except (ValueError, TypeError) as e:
        # Date parsing error - skip alert
        pass

    return alerts


def calculate_resistance_mutation_alerts(
    mutations: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate alerts for newly detected resistance mutations

    Args:
        mutations: List of mutations

    Returns:
        List of resistance mutation alert dictionaries
    """
    alerts = []

    # Find resistance mutations
    resistance_mutations = [
        m for m in mutations
        if m.get('resistance_mutation') or m.get('is_acquired_resistance')
    ]

    if not resistance_mutations:
        return alerts

    # Group by detection timepoint to identify acquired resistance
    acquired_resistance = [
        m for m in resistance_mutations
        if m.get('detection_timepoint') in ['Progression', 'Post_treatment']
    ]

    if acquired_resistance:
        mutation_list = []
        for m in acquired_resistance:
            mut_str = f"{m['gene_symbol']} {m['mutation_type']}"
            if m.get('vaf_percent'):
                mut_str += f" (VAF {m['vaf_percent']:.1f}%)"
            mutation_list.append(mut_str)

        alerts.append({
            "alert_id": "ALR-RES-001",
            "alert_type": "resistance_mutation",
            "severity": "High",
            "message": f"Acquired resistance mutations detected: {', '.join(mutation_list)}",
            "trigger_date": acquired_resistance[-1].get('test_date'),
            "requires_action": True,
            "action_recommendation": "Dual resistance mechanism identified. Consider targeted combination therapy per clinical trials (GEOMETRY-E1, TATTON) or MDT discussion for next-line options.",
            "supporting_data": {
                "resistance_mutations": [
                    {
                        "gene": m['gene_symbol'],
                        "mutation": m['mutation_type'],
                        "vaf_percent": m.get('vaf_percent')
                    }
                    for m in acquired_resistance
                ],
                "detection_timepoint": acquired_resistance[-1].get('detection_timepoint'),
                "specimen_source": acquired_resistance[-1].get('specimen_source')
            }
        })

    return alerts


def generate_all_alerts(
    mutations: List[Dict[str, Any]],
    molecular_tests: List[Dict[str, Any]],
    imaging_studies: List[Dict[str, Any]],
    current_stage: str
) -> List[Dict[str, Any]]:
    """
    Generate all clinical alerts for a patient

    Args:
        mutations: List of mutations
        molecular_tests: List of molecular tests
        imaging_studies: List of imaging studies
        current_stage: Current AJCC stage

    Returns:
        Combined list of all alert dictionaries
    """
    alerts = []

    # VAF trending alerts
    alerts.extend(calculate_vaf_alerts(mutations, molecular_tests))

    # Overdue imaging alerts
    alerts.extend(calculate_overdue_imaging_alerts(imaging_studies, current_stage))

    # Resistance mutation alerts
    alerts.extend(calculate_resistance_mutation_alerts(mutations))

    return alerts