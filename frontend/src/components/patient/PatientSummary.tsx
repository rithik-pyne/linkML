import React from 'react';
import { User, Activity, Stethoscope } from 'lucide-react';
import { usePatientSummary } from '../../hooks/usePatientSummary';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import { DataRow } from '../common/DataRow';
import { ECOGBadge, StageBadge } from '../common/Badge';

interface PatientSummaryProps {
  patientId: string | null;
}

export const PatientSummary: React.FC<PatientSummaryProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = usePatientSummary(patientId);

  if (!patientId) {
    return (
      <Card title="Patient Summary">
        <p className="text-gray-500 text-center py-8">
          Please select a patient to view summary
        </p>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title="Patient Summary">
        <LoadingSpinner message="Loading patient summary..." />
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Patient Summary">
        <ErrorMessage
          message={`Failed to load summary: ${error.message}`}
          onRetry={() => refetch()}
        />
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Patient Summary">
        <p className="text-gray-500">No data available</p>
      </Card>
    );
  }

  return (
    <Card title={`Patient Summary: ${data.patient_id}`}>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Column 1: Demographics */}
        <div className="space-y-3 p-4 rounded-lg hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-2 mb-4">
            <User className="h-5 w-5 text-cpi-blue" />
            <h3 className="text-lg font-semibold text-gray-900">Demographics</h3>
          </div>

          <DataRow label="NHS Number" value={data.nhs_number} />
          <DataRow label="Age at Diagnosis" value={`${data.age_at_diagnosis} years`} />
          <DataRow label="Sex" value={data.sex} />
          <DataRow label="Ethnicity" value={data.ethnicity_code} />
          <DataRow label="Diagnosis Date" value={new Date(data.diagnosis_date).toLocaleDateString()} />
          <DataRow label="Pathway" value={data.diagnosis_pathway} />

          <div className="mt-4 pt-4 border-t border-gray-200">
            <h4 className="text-sm font-semibold text-gray-700 mb-3">Risk Factors</h4>
            <DataRow label="Smoking Status" value={data.smoking_status} />
            <DataRow label="Pack Years" value={data.pack_years} />
            <DataRow
              label="Family History"
              value={data.family_history_lung_cancer ? 'Yes' : 'No'}
            />
          </div>
        </div>

        {/* Column 2: Baseline Labs */}
        <div className="space-y-3 p-4 rounded-lg hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-2 mb-4">
            <Activity className="h-5 w-5 text-cpi-blue" />
            <h3 className="text-lg font-semibold text-gray-900">Baseline Labs</h3>
          </div>

          <DataRow
            label="ECOG Status"
            value={<ECOGBadge status={data.ecog_baseline} />}
          />
          <DataRow label="eGFR" value={`${data.baseline_egfr} mL/min/1.73m²`} />
          <DataRow label="WBC" value={`${data.baseline_wbc} × 10⁹/L`} />
          <DataRow label="Hemoglobin" value={`${data.baseline_hemoglobin} g/L`} />
          <DataRow label="Platelets" value={`${data.baseline_platelets} × 10⁹/L`} />

          <div className="mt-4 pt-4 border-t border-gray-200">
            <h4 className="text-sm font-semibold text-gray-700 mb-3">Liver Function</h4>
            <DataRow label="ALT" value={`${data.baseline_alt} U/L`} />
            <DataRow label="AST" value={`${data.baseline_ast} U/L`} />
          </div>
        </div>

        {/* Column 3: Current Status */}
        <div className="space-y-3 p-4 rounded-lg hover:bg-gray-50 transition-colors">
          <div className="flex items-center gap-2 mb-4">
            <Stethoscope className="h-5 w-5 text-cpi-blue" />
            <h3 className="text-lg font-semibold text-gray-900">Current Status</h3>
          </div>

          <DataRow
            label="Current Stage"
            value={<StageBadge stage={data.current_stage} />}
          />
          <DataRow
            label="Latest ECOG"
            value={<ECOGBadge status={data.latest_ecog} />}
          />
          <DataRow
            label="ECOG Date"
            value={new Date(data.latest_ecog_date).toLocaleDateString()}
          />

          <div className="mt-4 pt-4 border-t border-gray-200">
            <h4 className="text-sm font-semibold text-gray-700 mb-3">Current Treatment</h4>
            <DataRow label="Drug" value={data.current_treatment.drug_name} />
            <DataRow label="Line" value={data.current_treatment.treatment_line} />
            <DataRow label="Intent" value={data.current_treatment.treatment_intent} />
            <DataRow
              label="Start Date"
              value={new Date(data.current_treatment.treatment_start_date).toLocaleDateString()}
            />
            {data.current_treatment.drug_dose_mg && (
              <DataRow
                label="Dose"
                value={`${data.current_treatment.drug_dose_mg}mg ${data.current_treatment.drug_frequency || ''}`}
              />
            )}
          </div>
        </div>
      </div>
    </Card>
  );
};