import React from 'react';
import { User } from 'lucide-react';
import { usePatients } from '../../hooks/usePatients';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';

interface PatientSelectorProps {
  selectedPatientId: string | null;
  onSelect: (patientId: string) => void;
}

export const PatientSelector: React.FC<PatientSelectorProps> = ({
  selectedPatientId,
  onSelect,
}) => {
  const { data, isLoading, error, refetch } = usePatients();

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <LoadingSpinner message="Loading patients..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <ErrorMessage
          message={`Failed to load patients: ${error.message}`}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  if (!data || data.patients.length === 0) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
        <p className="text-gray-500 text-center">No patients available</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <User className="h-5 w-5 text-cpi-blue" />
        <label htmlFor="patient-select" className="text-lg font-semibold text-gray-900">
          Select Patient
        </label>
        <span className="ml-auto text-sm text-gray-500">
          {data.total} patients available
        </span>
      </div>

      {/* Dropdown */}
      <select
        id="patient-select"
        value={selectedPatientId || ''}
        onChange={(e) => onSelect(e.target.value)}
        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-cpi-blue focus:border-transparent text-base bg-white"
      >
        <option value="">-- Select a patient --</option>
        {data.patients.map((patient) => (
          <option key={patient.patient_id} value={patient.patient_id}>
            {patient.patient_id} - {patient.age_at_diagnosis}yo {patient.sex}, Stage {patient.current_stage} ({patient.current_treatment})
          </option>
        ))}
      </select>

      {/* Selected patient indicator */}
      {selectedPatientId && (
        <div className="mt-4 p-3 bg-cpi-blue-50 rounded-lg border border-cpi-blue-200">
          <p className="text-sm text-gray-700">
            Currently viewing: <strong className="text-cpi-blue">{selectedPatientId}</strong>
          </p>
        </div>
      )}
    </div>
  );
};