import React, { useState } from 'react';
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { Activity, Syringe, Microscope, TrendingUp, FileText } from 'lucide-react';
import { useTimeline } from '../../hooks/useTimeline';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import type { VAFDataPoint, RECISTDataPoint } from '../../types/timeline';

function getEventIcon(eventType: string) {
  switch (eventType) {
    case 'treatment_start':
      return <Syringe className="h-4 w-4 text-green-600" />;
    case 'molecular_test':
      return <Microscope className="h-4 w-4 text-purple-600" />;
    case 'imaging_response':
      return <Activity className="h-4 w-4 text-blue-600" />;
    case 'clinical_response':
      return <Activity className="h-4 w-4 text-red-600" />;
    case 'imaging_study':
      return <FileText className="h-4 w-4 text-gray-600" />;
    default:
      return <TrendingUp className="h-4 w-4 text-gray-600" />;
  }
}

// Helper to transform VAF data for Recharts
function prepareVAFData(vafSeries: VAFDataPoint[]) {
  // Group by date and mutation
  const dataByDate: Record<string, any> = {};

  vafSeries.forEach(point => {
    const dateKey = point.date;
    if (!dataByDate[dateKey]) {
      dataByDate[dateKey] = { date: dateKey };
    }

    // Create unique key for each mutation (gene + type)
    const mutationKey = `${point.gene_symbol}_${point.mutation_type.replace(/\s+/g, '_')}`;
    dataByDate[dateKey][mutationKey] = point.vaf_percent;
  });

  // Convert to array and sort by date
  return Object.values(dataByDate).sort((a, b) =>
    new Date(a.date).getTime() - new Date(b.date).getTime()
  );
}

// Helper to prepare RECIST data
function prepareRECISTData(recistSeries: RECISTDataPoint[]) {
  return recistSeries
    .map(point => ({
      date: point.date,
      diameter: point.tumor_diameter_mm,
      stage: point.ajcc_stage,
      response: point.recist_response,
    }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
}

interface DiseaseTimelineProps {
  patientId: string | null;
}

export const DiseaseTimeline: React.FC<DiseaseTimelineProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = useTimeline(patientId);
  const [showVAF, setShowVAF] = useState(true);
  const [showRECIST, setShowRECIST] = useState(true);

  if (!patientId) {
    return (
      <Card title="Disease Timeline">
        <p className="text-gray-500 text-center py-8">
          Please select a patient to view timeline
        </p>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title="Disease Timeline">
        <LoadingSpinner message="Loading timeline data..." />
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Disease Timeline">
        <ErrorMessage
          message={`Failed to load timeline: ${error.message}`}
          onRetry={() => refetch()}
        />
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Disease Timeline">
        <p className="text-gray-500">No data available</p>
      </Card>
    );
  }

  const vafData = prepareVAFData(data.vaf_series);
  const recistData = prepareRECISTData(data.recist_series);

  // Merge VAF and RECIST data by date
  const mergedData = vafData.map(vafPoint => {
    const recistPoint = recistData.find(r => r.date === vafPoint.date);
    return {
      ...vafPoint,
      diameter: recistPoint?.diameter || null,
      response: recistPoint?.response || null,
    };
  });

  // Also add RECIST-only dates
  recistData.forEach(recistPoint => {
    if (!mergedData.find(m => m.date === recistPoint.date)) {
      mergedData.push({
        date: recistPoint.date,
        diameter: recistPoint.diameter,
        response: recistPoint.response,
      });
    }
  });

  // Sort merged data
  mergedData.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  console.log('Merged Timeline Data:', mergedData);

  // Extract unique mutations for line configuration
  const mutations = Array.from(new Set(
    data.vaf_series.map(v => `${v.gene_symbol}_${v.mutation_type.replace(/\s+/g, '_')}`)
  ));

  return (
    <Card title={`Disease Timeline: ${data.patient_id}`}>
      <div className="space-y-4">
        {/* Toggle Controls */}
        <div className="flex gap-4 items-center">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showVAF}
              onChange={(e) => setShowVAF(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm font-medium text-gray-700">Show VAF Lines</span>
          </label>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={showRECIST}
              onChange={(e) => setShowRECIST(e.target.checked)}
              className="w-4 h-4"
            />
            <span className="text-sm font-medium text-gray-700">Show Tumor Diameter</span>
          </label>
        </div>

        <div className="h-96 bg-white rounded border border-gray-200 p-4">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={mergedData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
              <XAxis
                dataKey="date"
                tickFormatter={(date) => format(new Date(date), 'MM/yyyy')}
                tick={{ fontSize: 12 }}
              />
              <YAxis
                yAxisId="left"
                label={{ value: 'VAF (%)', angle: -90, position: 'insideLeft' }}
                tick={{ fontSize: 12 }}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                label={{ value: 'Tumor Diameter (mm)', angle: 90, position: 'insideRight' }}
                tick={{ fontSize: 12 }}
              />
              <Tooltip
                formatter={(value: any, name: any) => {
                  const nameStr = String(name || '');
                  if (nameStr.includes('VAF')) {
                    return [`${value}%`, nameStr];
                  }
                  if (nameStr.includes('Diameter')) {
                    return [`${value} mm`, nameStr];
                  }
                  return [value, nameStr];
                }}
                labelFormatter={(date) => format(new Date(date), 'MMM dd, yyyy')}
              />
              <Legend />

              {/* VAF Lines - Dynamically render all mutations */}
              {showVAF && mutations.map((mutationKey) => {
                // Color coding: blue for primary drivers, red for resistance, orange for others
                const isResistance = mutationKey.includes('T790M') || mutationKey.includes('MET');
                const isPrimary = mutationKey.includes('Ex19del') || mutationKey.includes('L858R');
                const color = isResistance ? '#d3353d' : isPrimary ? '#0058AA' : '#ff9200';
                const dashArray = isResistance ? '5 5' : undefined;

                // Create readable name from key
                const displayName = mutationKey.replace(/_/g, ' ') + ' VAF';

                return (
                  <Line
                    key={mutationKey}
                    yAxisId="left"
                    type="monotone"
                    dataKey={mutationKey}
                    stroke={color}
                    strokeWidth={2}
                    strokeDasharray={dashArray}
                    name={displayName}
                    dot={{ fill: color, r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                );
              })}

              {/* Tumor Diameter Bars (yAxisId="right") */}
              {showRECIST && (
                <Bar
                  yAxisId="right"
                  dataKey="diameter"
                  fill="#e5e5e5"
                  fillOpacity={0.6}
                  name="Tumor Diameter"
                />
              )}
            </ComposedChart>
          </ResponsiveContainer>
        </div>

        {/* Timeline Events List */}
        <div className="mt-6 border-t pt-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Key Events</h4>
          <div className="space-y-2 max-h-64 overflow-y-auto scrollbar-thin">
            {data.timeline_events.map((event, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-2 hover:bg-gray-50 rounded transition-colors"
              >
                <div className="flex-shrink-0 mt-0.5">
                  {getEventIcon(event.event_type)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline gap-2">
                    <span className="text-xs font-medium text-gray-500 flex-shrink-0">
                      {format(new Date(event.date), 'MMM dd, yyyy')}
                    </span>
                    <span className="text-sm text-gray-900">{event.description}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Card>
  );
};