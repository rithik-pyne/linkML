import React, { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen } from 'lucide-react';
import { useDecisions } from '../../hooks/useDecisions';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import { Badge } from '../common/Badge';
import type { Recommendation } from '../../types/decisions';

interface RecommendationCardProps {
  recommendation: Recommendation;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation }) => {
  const [expanded, setExpanded] = useState(false);

  // Priority badge variant
  const priorityVariant = {
    Urgent: 'danger',
    High: 'warning',
    Medium: 'info',
    Low: 'default',
  }[recommendation.priority] as 'danger' | 'warning' | 'info' | 'default';

  // Evidence level color
  const evidenceColor = recommendation.evidence_level.includes('Level I')
    ? 'text-green-700 bg-green-100 border-green-300'
    : recommendation.evidence_level.includes('Level II')
    ? 'text-blue-700 bg-blue-100 border-blue-300'
    : recommendation.evidence_level.includes('Level III')
    ? 'text-orange-700 bg-orange-100 border-orange-300'
    : 'text-gray-700 bg-gray-100 border-gray-300';

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start gap-3">
        <div className="flex-1">
          <div className="flex flex-wrap gap-2 mb-2">
            <Badge variant={priorityVariant} size="sm">
              {recommendation.priority}
            </Badge>
            <span className={`inline-flex items-center text-xs px-2 py-1 font-medium border rounded-full ${evidenceColor}`}>
              {recommendation.evidence_level}
            </span>
            <Badge variant={recommendation.confidence === 'High' ? 'success' : recommendation.confidence === 'Moderate' ? 'warning' : 'default'} size="sm">
              {recommendation.confidence} confidence
            </Badge>
          </div>

          {/* Recommendation text */}
          <h4 className="text-base font-semibold text-gray-900 mb-2">
            {recommendation.recommendation}
          </h4>

          {/* Rationale */}
          <p className="text-sm text-gray-700 mb-2">
            {recommendation.rationale}
          </p>

          {/* Guideline reference */}
          <div className="flex items-start gap-2 text-xs text-gray-600 italic">
            <BookOpen className="h-3 w-3 mt-0.5 flex-shrink-0" />
            <span>{recommendation.guideline_reference}</span>
          </div>
        </div>
      </div>

      {/* Expand/Collapse for supporting data */}
      {Object.keys(recommendation.supporting_data).length > 0 && (
        <div className="mt-3">
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-2 text-sm text-cpi-blue hover:text-cpi-blue-600 font-medium"
          >
            {expanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
            {expanded ? 'Hide' : 'Show'} Supporting Data
          </button>

          {expanded && (
            <div className="mt-3 p-3 bg-gray-50 rounded text-xs">
              <pre className="whitespace-pre-wrap text-gray-700 font-mono">
                {JSON.stringify(recommendation.supporting_data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

interface TreatmentRecommendationsProps {
  patientId: string | null;
}

export const TreatmentRecommendations: React.FC<TreatmentRecommendationsProps> = ({
  patientId
}) => {
  const { data, isLoading, error, refetch } = useDecisions(patientId);

  if (!patientId) {
    return (
      <Card title="Treatment Recommendations">
        <p className="text-gray-500 text-center py-8">
          Please select a patient to view recommendations
        </p>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title="Treatment Recommendations">
        <LoadingSpinner message="Loading recommendations..." />
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Treatment Recommendations">
        <ErrorMessage
          message={`Failed to load recommendations: ${error.message}`}
          onRetry={() => refetch()}
        />
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Treatment Recommendations">
        <p className="text-gray-500">No data available</p>
      </Card>
    );
  }

  return (
    <Card title="Treatment Recommendations">
      {data.recommendations.length === 0 ? (
        <p className="text-gray-500 text-center py-8">
          No active recommendations at this time.
        </p>
      ) : (
        <div className="space-y-4">
          {data.recommendations.map(rec => (
            <RecommendationCard key={rec.recommendation_id} recommendation={rec} />
          ))}
        </div>
      )}
    </Card>
  );
};