import React from 'react';
import { Dna, Target, AlertTriangle, FlaskConical } from 'lucide-react';
import { useMolecularProfile } from '../../hooks/useMolecularProfile';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import { Badge } from '../common/Badge';
import type { Mutation } from '../../types/molecular';

interface MutationCardProps {
  mutation: Mutation;
  isPrimary?: boolean;
}

const MutationCard: React.FC<MutationCardProps> = ({ mutation, isPrimary = false }) => {
  return (
    <div
      className={`p-4 rounded-lg border-2 ${
        isPrimary
          ? 'bg-cpi-blue-50 border-cpi-blue'
          : 'bg-white border-gray-200'
      }`}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex-1">
          <h4 className="text-lg font-bold text-gray-900">
            {mutation.gene_symbol} <span className="text-cpi-blue">{mutation.mutation_type}</span>
          </h4>
          <p className="text-sm text-gray-600 font-mono mt-1">{mutation.mutation_hgvs}</p>
        </div>
        {isPrimary && (
          <Target className="h-5 w-5 text-cpi-blue flex-shrink-0" />
        )}
      </div>

      <div className="flex flex-wrap gap-2 mt-3">
        <Badge variant="info" size="sm">
          VAF: {mutation.vaf_percent}%
        </Badge>
        {mutation.tumor_fraction_percent && (
          <Badge variant="info" size="sm">
            TF: {mutation.tumor_fraction_percent}%
          </Badge>
        )}
        {mutation.actionable_mutation && (
          <Badge variant="success" size="sm">Actionable</Badge>
        )}
        {mutation.is_primary_driver && (
          <Badge variant="info" size="sm">Driver</Badge>
        )}
      </div>

      <div className="mt-3 pt-3 border-t border-gray-200 text-xs text-gray-600">
        <div className="flex justify-between">
          <span>Detected: {new Date(mutation.test_date).toLocaleDateString()}</span>
          <span>{mutation.specimen_source}</span>
        </div>
        <div className="mt-1">
          {mutation.ngs_panel_name} • {mutation.detection_timepoint}
        </div>
      </div>
    </div>
  );
};

interface MolecularProfileProps {
  patientId: string | null;
}

export const MolecularProfile: React.FC<MolecularProfileProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = useMolecularProfile(patientId);

  if (!patientId) {
    return (
      <Card title="Molecular Profile">
        <p className="text-gray-500 text-center py-8">
          Please select a patient to view molecular profile
        </p>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title="Molecular Profile">
        <LoadingSpinner message="Loading molecular data..." />
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Molecular Profile">
        <ErrorMessage
          message={`Failed to load molecular profile: ${error.message}`}
          onRetry={() => refetch()}
        />
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Molecular Profile">
        <p className="text-gray-500">No data available</p>
      </Card>
    );
  }

  return (
    <Card title={`Molecular Profile: ${data.patient_id}`}>
      <div className="space-y-6">
        {/* Primary Driver Mutation */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Dna className="h-5 w-5 text-cpi-blue" />
            <h3 className="text-lg font-semibold text-gray-900">
              Primary Driver Mutation
            </h3>
          </div>
          <MutationCard mutation={data.primary_driver_mutation} isPrimary />
        </div>

        {/* Co-Mutations */}
        {data.co_mutations.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <Dna className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-900">
                Co-Mutations
              </h3>
              <Badge variant="default" size="sm">
                {data.co_mutations.length}
              </Badge>
            </div>
            <div className="grid grid-cols-1 gap-3">
              {data.co_mutations.map(mutation => (
                <div key={mutation.mutation_id} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">
                        {mutation.gene_symbol} {mutation.mutation_type}
                      </p>
                      {mutation.mutation_hgvs && (
                        <p className="text-xs text-gray-600 font-mono mt-1">
                          {mutation.mutation_hgvs}
                        </p>
                      )}
                      <div className="flex gap-2 mt-2">
                        <Badge variant="info" size="sm">
                          VAF: {mutation.vaf_percent}%
                        </Badge>
                        {mutation.actionable_mutation && (
                          <Badge variant="success" size="sm">Actionable</Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Resistance Mutations */}
        {data.resistance_mutations.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle className="h-5 w-5 text-cpi-red" />
              <h3 className="text-lg font-semibold text-gray-900">
                Acquired Resistance Mutations
              </h3>
              <Badge variant="danger" size="sm">
                {data.resistance_mutations.length}
              </Badge>
            </div>
            <div className="bg-cpi-red-bg border-l-4 border-cpi-red rounded-lg p-4">
              <div className="space-y-3">
                {data.resistance_mutations.map(mutation => (
                  <div key={mutation.mutation_id} className="bg-white rounded-lg p-3 shadow-sm">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="font-bold text-gray-900">
                          {mutation.gene_symbol} {mutation.mutation_type}
                        </p>
                        {mutation.mutation_hgvs && (
                          <p className="text-sm text-gray-600 font-mono mt-1">
                            {mutation.mutation_hgvs}
                          </p>
                        )}
                        <div className="flex gap-2 mt-2">
                          <Badge variant="danger" size="sm">
                            VAF: {mutation.vaf_percent}%
                          </Badge>
                          <Badge variant="default" size="sm">
                            {mutation.specimen_source}
                          </Badge>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">
                          Detected: {new Date(mutation.test_date).toLocaleDateString()} • {mutation.ngs_panel_name}
                        </p>
                      </div>
                      <Badge variant="danger" size="sm">Resistance</Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* PD-L1 Status */}
        {data.pdl1_status && (
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-4 border border-blue-200">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-1">PD-L1 Expression</h4>
                <p className="text-3xl font-bold text-cpi-blue">
                  {data.pdl1_status.tps_percent}%
                </p>
                <p className="text-xs text-gray-600 mt-1">
                  TPS • {data.pdl1_status.antibody_clone} clone
                </p>
              </div>
              <div className="text-right text-xs text-gray-500">
                <p>Tested:</p>
                <p className="font-medium">
                  {new Date(data.pdl1_status.test_date).toLocaleDateString()}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Latest NGS Test Info */}
        <div className="border-t pt-4 mt-6">
          <div className="flex items-center gap-2 mb-2">
            <FlaskConical className="h-4 w-4 text-gray-600" />
            <h4 className="text-sm font-semibold text-gray-700">Latest NGS Test</h4>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-xs text-gray-500">Panel</p>
              <p className="font-medium text-gray-900">
                {data.latest_ngs_test.ngs_panel_name}
              </p>
              <p className="text-xs text-gray-600">
                {data.latest_ngs_test.ngs_panel_version}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Test Date</p>
              <p className="font-medium text-gray-900">
                {new Date(data.latest_ngs_test.test_date).toLocaleDateString()}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Specimen</p>
              <p className="font-medium text-gray-900">
                {data.latest_ngs_test.specimen_source}
              </p>
            </div>
            <div>
              <p className="text-xs text-gray-500">Coverage</p>
              <p className="font-medium text-gray-900">
                {data.latest_ngs_test.mean_coverage_depth.toLocaleString()}x
              </p>
            </div>
          </div>
          <div className="mt-3 p-2 bg-cpi-blue-50 rounded">
            <p className="text-sm">
              <span className="text-gray-700">Actionable Mutations:</span>{' '}
              <strong className="text-cpi-blue">{data.actionable_mutations_count}</strong>
            </p>
          </div>
        </div>
      </div>
    </Card>
  );
};