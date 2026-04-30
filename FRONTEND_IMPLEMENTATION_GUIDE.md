# FRONTEND DETAILED GUIDE - FINAL PHASES

**Continuation of Phase 8-11**

This file completes the ultra-detailed implementation guide with Timeline Chart, Recommendations, Alerts, and Final Integration.

---

## Phase 8 Continued: Timeline Chart (Recharts Implementation)

**Current Progress**: Steps 8.1-8.3 complete (types, hook, structure)

### Step 8.4: Install and Test Recharts

**Goal**: Ensure Recharts is working before building complex chart

**Manual Test 8.4.1** - Verify Recharts Installation:
```bash
cd frontend
npm list recharts
```

✅ **EXPECTED**: Shows recharts version (e.g., recharts@2.12.7)

**Manual Test 8.4.2** - Simple Recharts Test:

Update `frontend/src/components/timeline/DiseaseTimeline.tsx`:

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Inside the final return, replace placeholder with:
return (
  <Card title={`Disease Timeline: ${data.patient_id}`}>
    <div className="h-96">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={[
          { date: '2020-01', vaf: 38 },
          { date: '2020-06', vaf: 5 },
          { date: '2022-05', vaf: 12 }
        ]}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="vaf" stroke="#0058AA" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </Card>
);
```

1. Save file
2. ✅ **EXPECTED**:
   - Chart appears with blue line
   - 3 data points visible
   - X-axis shows dates
   - Y-axis shows numbers
   - Grid lines visible
   - Hover over points shows tooltip

**Visual Confirmation**:
- ✅ Recharts renders without errors
- ✅ Chart is responsive (resize window = chart resizes)
- ✅ Blue line color (#0058AA) matches CPI brand

**✅ CHECKPOINT 8.4**: Recharts working

---

### Step 8.5: Transform VAF Data for Chart

**Goal**: Convert API data to Recharts format

**File**: `frontend/src/components/timeline/DiseaseTimeline.tsx` (UPDATE)

Add helper function above component:

```typescript
import { format } from 'date-fns';

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
```

**Manual Test 8.5.1** - Test Data Transformation:

Add console log before return:

```typescript
const vafData = prepareVAFData(data.vaf_series);
console.log('VAF Data for Chart:', vafData);
```

1. Save file
2. Select NGDX-001
3. Open console
4. ✅ **EXPECTED OUTPUT**:
```javascript
[
  { date: '2020-03-14', EGFR_Exon_19_deletion: 38.5 },
  { date: '2020-09-01', EGFR_Exon_19_deletion: 0.08 },
  { date: '2022-05-14', EGFR_Exon_19_deletion: 12.4, EGFR_T790M: 8.2 }
]
```

**What This Does**:
- Groups data by date
- Creates property name for each unique mutation
- Handles multiple mutations on same date
- Sorts chronologically

**✅ CHECKPOINT 8.5**: VAF data transformation working

---

### Step 8.6: Create VAF Line Chart

**Goal**: Display VAF trends over time

**File**: `frontend/src/components/timeline/DiseaseTimeline.tsx` (UPDATE)

```typescript
export const DiseaseTimeline: React.FC<DiseaseTimelineProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = useTimeline(patientId);

  // ... loading/error states ...

  if (!data) return null;

  const vafData = prepareVAFData(data.vaf_series);

  // Extract unique mutations for line configuration
  const mutations = Array.from(new Set(
    data.vaf_series.map(v => `${v.gene_symbol}_${v.mutation_type.replace(/\s+/g, '_')}`)
  ));

  return (
    <Card title={`Disease Timeline: ${data.patient_id}`}>
      <div className="space-y-4">
        <div className="h-96 bg-white rounded border border-gray-200 p-4">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={vafData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(date) => format(new Date(date), 'MM/yyyy')}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                label={{ value: 'VAF (%)', angle: -90, position: 'insideLeft' }}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                formatter={(value: any) => [`${value}%`, '']}
                labelFormatter={(date) => format(new Date(date), 'MMM dd, yyyy')}
              />
              <Legend />
              
              {/* EGFR Ex19del - primary driver (solid blue) */}
              {mutations.includes('EGFR_Exon_19_deletion') && (
                <Line 
                  type="monotone" 
                  dataKey="EGFR_Exon_19_deletion" 
                  stroke="#0058AA" 
                  strokeWidth={2}
                  name="EGFR Ex19del"
                  dot={{ fill: '#0058AA', r: 4 }}
                  activeDot={{ r: 6 }}
                />
              )}
              
              {/* T790M resistance (dashed red) */}
              {mutations.includes('EGFR_T790M') && (
                <Line 
                  type="monotone" 
                  dataKey="EGFR_T790M" 
                  stroke="#d3353d" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="EGFR T790M (resistance)"
                  dot={{ fill: '#d3353d', r: 4 }}
                  activeDot={{ r: 6 }}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Card>
  );
};
```

**What Changed**:
- Real VAF data displayed
- Date formatting (MM/yyyy on axis, full date in tooltip)
- Y-axis label rotated
- Primary driver (Ex19del) = solid blue line
- Resistance (T790M) = dashed red line
- Dots on data points (radius 4px, active 6px)
- Tooltip shows percentage sign
- Legend shows mutation names

**Manual Test 8.6.1** - Verify VAF Chart:
1. Save file
2. Select NGDX-001
3. ✅ **EXPECTED**:
   - Chart shows 2 lines:
     - Blue solid line (EGFR Ex19del): High → Very low → Rising
     - Red dashed line (T790M): Appears only at last timepoint
   - X-axis: 03/2020, 09/2020, 05/2022
   - Y-axis: 0-40 range
   - Legend: "EGFR Ex19del", "EGFR T790M (resistance)"

**Manual Test 8.6.2** - Hover Interaction:
1. Hover over first data point (03/2020)
2. ✅ **EXPECTED TOOLTIP**:
   - Date: "Mar 14, 2020"
   - EGFR Ex19del: 38.5%
3. Hover over last point (05/2022)
4. ✅ **EXPECTED**: Shows both mutations

**Clinical Interpretation**:
- ✅ High baseline VAF (38.5%) = significant tumor burden
- ✅ Dramatic drop to 0.08% = excellent treatment response
- ✅ Rise to 12.4% = molecular progression
- ✅ T790M emergence = resistance mechanism

**Visual Confirmation**:
- ✅ Blue line is prominent (primary driver)
- ✅ Red dashed line signals resistance
- ✅ Chart is readable and professional
- ✅ Data story is clear

**✅ CHECKPOINT 8.6**: VAF line chart complete

---

### Step 8.7: Add RECIST Tumor Diameter Bars

**Goal**: Overlay tumor size measurements

**File**: `frontend/src/components/timeline/DiseaseTimeline.tsx` (UPDATE)

Add helper function:

```typescript
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
```

Update chart to use ComposedChart (allows mixing line + bar):

```typescript
import { ComposedChart, Line, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

// Inside component, prepare combined data:
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
```

Replace LineChart with ComposedChart:

```typescript
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
    formatter={(value: any, name: string) => {
      if (name.includes('VAF') || name.includes('diameter')) {
        return [typeof value === 'number' ? `${value}%` : value, name];
      }
      return [value, name];
    }}
    labelFormatter={(date) => format(new Date(date), 'MMM dd, yyyy')}
  />
  <Legend />
  
  {/* VAF Lines (yAxisId="left") */}
  {mutations.includes('EGFR_Exon_19_deletion') && (
    <Line 
      yAxisId="left"
      type="monotone" 
      dataKey="EGFR_Exon_19_deletion" 
      stroke="#0058AA" 
      strokeWidth={2}
      name="EGFR Ex19del VAF"
      dot={{ fill: '#0058AA', r: 4 }}
    />
  )}
  
  {mutations.includes('EGFR_T790M') && (
    <Line 
      yAxisId="left"
      type="monotone" 
      dataKey="EGFR_T790M" 
      stroke="#d3353d" 
      strokeWidth={2}
      strokeDasharray="5 5"
      name="T790M VAF"
      dot={{ fill: '#d3353d', r: 4 }}
    />
  )}
  
  {/* Tumor Diameter Bars (yAxisId="right") */}
  <Bar 
    yAxisId="right"
    dataKey="diameter" 
    fill="#e5e5e5" 
    fillOpacity={0.6}
    name="Tumor Diameter (mm)"
  />
</ComposedChart>
```

**What Changed**:
- ComposedChart allows mixing Line + Bar
- Two Y-axes: left (VAF), right (tumor diameter)
- VAF lines reference left axis
- Bars reference right axis
- Merged data combines VAF and RECIST by date
- Gray bars (semi-transparent) for tumor diameter

**Manual Test 8.7.1** - Verify Dual-Axis Chart:
1. Save file
2. Select NGDX-001
3. ✅ **EXPECTED**:
   - Left Y-axis: "VAF (%)" label
   - Right Y-axis: "Tumor Diameter (mm)" label
   - Blue line (VAF) on left scale
   - Gray bars (tumor) on right scale
   - 5 timepoints with either VAF, tumor, or both
   - Bars show: 15.6mm → 0mm → 0mm → 0mm → 35mm

**Manual Test 8.7.2** - Hover Multi-Data:
1. Hover over 05/2022 point
2. ✅ **EXPECTED TOOLTIP**:
   - Date: May 14, 2022
   - EGFR Ex19del VAF: 12.4%
   - T790M VAF: 8.2%
   - Tumor Diameter: 35mm (shown if available)

**Clinical Interpretation**:
- ✅ Tumor shrinks to 0mm (complete response)
- ✅ Stays 0mm during remission
- ✅ Regrows to 35mm at progression
- ✅ VAF rise precedes tumor regrowth (molecular precedes radiographic)

**Visual Confirmation**:
- ✅ Two Y-axes don't confuse the display
- ✅ Bars don't obscure lines
- ✅ Both data types are readable

**✅ CHECKPOINT 8.7**: RECIST bars added successfully

---

### Step 8.8: Add Toggle Controls

**Goal**: Allow showing/hiding different data series

**File**: `frontend/src/components/timeline/DiseaseTimeline.tsx` (UPDATE)

Add state at top of component:

```typescript
import { useState } from 'react';

export const DiseaseTimeline: React.FC<DiseaseTimelineProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = useTimeline(patientId);
  const [showVAF, setShowVAF] = useState(true);
  const [showRECIST, setShowRECIST] = useState(true);
  
  // ... rest of component ...
```

Add controls above chart:

```typescript
<Card title={`Disease Timeline: ${data.patient_id}`}>
  {/* Toggle Controls */}
  <div className="flex flex-wrap gap-4 mb-4 p-3 bg-gray-50 rounded border border-gray-200">
    <label className="flex items-center gap-2 cursor-pointer">
      <input
        type="checkbox"
        checked={showVAF}
        onChange={() => setShowVAF(!showVAF)}
        className="w-4 h-4 text-cpi-blue rounded focus:ring-cpi-blue"
      />
      <span className="text-sm font-medium text-gray-700">Show VAF Trends</span>
    </label>
    
    <label className="flex items-center gap-2 cursor-pointer">
      <input
        type="checkbox"
        checked={showRECIST}
        onChange={() => setShowRECIST(!showRECIST)}
        className="w-4 h-4 text-cpi-blue rounded focus:ring-cpi-blue"
      />
      <span className="text-sm font-medium text-gray-700">Show Tumor Diameter</span>
    </label>
    
    <div className="ml-auto text-xs text-gray-500">
      {data.timeline_events.length} events • {data.vaf_series.length} VAF measurements
    </div>
  </div>

  {/* Chart */}
  <div className="h-96 bg-white rounded border border-gray-200 p-4">
    {/* ... chart code, wrap VAF lines in: */}
    {showVAF && mutations.includes('EGFR_Exon_19_deletion') && (
      <Line ... />
    )}
    
    {/* Wrap RECIST bars in: */}
    {showRECIST && (
      <Bar ... />
    )}
  </div>
</Card>
```

**Manual Test 8.8.1** - Test VAF Toggle:
1. Save file
2. ✅ **EXPECTED**: Both checkboxes checked by default
3. Uncheck "Show VAF Trends"
4. ✅ **EXPECTED**: Blue lines disappear, bars remain
5. Check it again
6. ✅ **EXPECTED**: Lines reappear

**Manual Test 8.8.2** - Test RECIST Toggle:
1. Uncheck "Show Tumor Diameter"
2. ✅ **EXPECTED**: Gray bars disappear, lines remain
3. Uncheck both
4. ✅ **EXPECTED**: Empty chart with just grid and axes

**Visual Confirmation**:
- ✅ Checkboxes are styled consistently
- ✅ Toggle actions are instant
- ✅ Chart rescales appropriately
- ✅ Event count shown on right

**✅ CHECKPOINT 8.8**: Toggle controls working

---

### Step 8.9: Add Timeline Events List Below Chart

**Goal**: Show key events chronologically

**File**: `frontend/src/components/timeline/DiseaseTimeline.tsx` (UPDATE)

Add helper for event icons:

```typescript
import { Activity, Syringe, Microscope, TrendingUp, FileText } from 'lucide-react';

function getEventIcon(eventType: string) {
  switch (eventType) {
    case 'treatment_start':
      return <Syringe className="h-4 w-4 text-green-600" />;
    case 'molecular_test':
      return <Microscope className="h-4 w-4 text-purple-600" />;
    case 'response_assessment':
      return <Activity className="h-4 w-4 text-blue-600" />;
    case 'imaging':
      return <FileText className="h-4 w-4 text-gray-600" />;
    default:
      return <TrendingUp className="h-4 w-4 text-gray-600" />;
  }
}
```

Add events list after chart:

```typescript
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
```

**What Changed**:
- Event type icons (color-coded)
- Scrollable list (max-height 256px)
- Date + description for each event
- Hover effect on event rows
- Custom scrollbar (thin, CPI blue)

**Manual Test 8.9.1** - Verify Events List:
1. Save file
2. Select NGDX-001
3. Scroll below chart
4. ✅ **EXPECTED EVENTS** (chronological):
   - 📅 Mar 14, 2020: Tissue NGS - EGFR Ex19del detected
   - 💉 Mar 25, 2020: Surgery - Lobectomy
   - 💉 Apr 15, 2020: Adjuvant Osimertinib
   - 📊 Apr 29, 2020: Post-surgery - Complete Response
   - (... more events ...)
   - 🔬 May 14, 2022: ctDNA - T790M + MET amp resistance detected
5. ✅ **VERIFY**:
   - Icons match event types
   - Dates are formatted consistently
   - Descriptions are concise and clear

**Manual Test 8.9.2** - Test Scrolling (if > 6 events):
1. Try to scroll event list
2. ✅ **EXPECTED**: Scrollbar appears if needed, CPI blue color

**Visual Confirmation**:
- ✅ Events are easy to scan
- ✅ Icons add visual categorization
- ✅ Hover feedback is subtle but clear
- ✅ Timeline tells complete patient story

**✅ CHECKPOINT 8.9**: Timeline events list complete

---

### Step 8.10: Test Complete Timeline Component

**Goal**: Comprehensive integration testing

**Manual Test 8.10.1** - Full Timeline Review (NGDX-001):
1. Select NGDX-001
2. ✅ **VERIFY CHART**:
   - Blue line (EGFR Ex19del): 38.5% → 0.08% → 12.4%
   - Red dashed line (T790M): Appears at 8.2% only at end
   - Gray bars show tumor: 15.6mm → 0 → 0 → 0 → 35mm
   - Left Y-axis: 0-40% (VAF)
   - Right Y-axis: 0-40mm (tumor)
   - X-axis: 5 timepoints from 03/2020 to 05/2022
3. ✅ **VERIFY CONTROLS**:
   - Toggle VAF off → lines disappear
   - Toggle RECIST off → bars disappear
   - Toggle both back on → all visible
4. ✅ **VERIFY EVENTS**:
   - 12+ events listed chronologically
   - Icons match event types
   - Descriptions are clear

**Manual Test 8.10.2** - Clinical Story Validation:
1. Read through timeline top to bottom
2. ✅ **VERIFY NARRATIVE**:
   - High baseline VAF (advanced disease)
   - Surgery performed
   - VAF drops dramatically (treatment working)
   - Tumor shrinks to 0mm (complete response)
   - ~2 years stable
   - VAF rises (molecular progression)
   - Tumor regrows (radiographic progression)
   - Resistance mutations detected
   - Treatment changes

**Manual Test 8.10.3** - Test Other Patients:
1. Select NGDX-002, NGDX-003, etc.
2. ✅ **VERIFY**:
   - Different mutation patterns display
   - Charts update correctly
   - Events are patient-specific
   - No errors in console

**Manual Test 8.10.4** - Responsive Design:
1. Toggle device toolbar
2. Select mobile device (375px)
3. ✅ **VERIFY**:
   - Chart stacks vertically
   - Controls wrap properly
   - Events list scrolls
   - Touch interactions work
4. Desktop view (1920px)
5. ✅ **VERIFY**:
   - Chart uses available width
   - Layout is comfortable
   - No wasted space

**Performance Check**:
- Chart renders in < 1 second
- Toggle interactions are instant
- Hover tooltips respond quickly
- No lag when switching patients

**Visual Confirmation**:
- ✅ Timeline is the most complex component
- ✅ All elements work together harmoniously
- ✅ Clinical data story is clear
- ✅ Interactions are intuitive
- ✅ Professional medical visualization

**✅ CHECKPOINT 8.10**: DiseaseTimeline component COMPLETE!

---

## Phase 8 Complete Summary

**DiseaseTimeline Component** is fully built with:
- ✅ VAF line chart (multiple mutations)
- ✅ RECIST tumor diameter bars
- ✅ Dual Y-axes (VAF + diameter)
- ✅ Toggle controls (show/hide series)
- ✅ Timeline events list with icons
- ✅ Recharts integration (ComposedChart)
- ✅ Date formatting (date-fns)
- ✅ Interactive tooltips
- ✅ Responsive design
- ✅ CPI branding (colors)
- ✅ Tested with multiple patients
- ✅ Clinical narrative is clear

**Progress**: 62 checkpoints complete out of ~100 total

---

## Phase 9: Treatment Recommendations Component

### Step 9.1: Add Recommendations Types

**Goal**: TypeScript definitions for clinical recommendations

**File**: `frontend/src/types/decisions.ts` (NEW FILE)

```typescript
export interface Recommendation {
  recommendation_id: string;
  recommendation: string;
  rationale: string;
  evidence_level: string;
  guideline_reference: string;
  confidence: 'High' | 'Moderate' | 'Low';
  applicable: boolean;
  priority: 'Urgent' | 'High' | 'Medium' | 'Low';
  supporting_data: Record<string, any>;
}

export interface Alert {
  alert_id: string;
  alert_type: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  message: string;
  trigger_date: string;
  requires_action: boolean;
  action_recommendation: string;
  supporting_data?: Record<string, any>;
}

export interface DecisionsResponse {
  patient_id: string;
  current_treatment_line: number;
  current_stage: string;
  recommendations: Recommendation[];
  alerts: Alert[];
}
```

**✅ CHECKPOINT 9.1**: Recommendations types defined

---

### Step 9.2: Create useDecisions Hook

**Goal**: Fetch treatment recommendations from API

**File**: `frontend/src/hooks/useDecisions.ts` (NEW FILE)

```typescript
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { DecisionsResponse } from '../types/decisions';

export function useDecisions(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.decisions, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<DecisionsResponse>(
        `/api/patients/${patientId}/decisions`
      );
      return response.data;
    },
    enabled: !!patientId,
  });
}
```

**✅ CHECKPOINT 9.2**: useDecisions hook created

---

### Step 9.3: Create TreatmentRecommendations Component Structure

**Goal**: Basic component with loading/error states

**File**: `frontend/src/components/decisions/TreatmentRecommendations.tsx` (NEW FILE)

```typescript
import React from 'react';
import { useDecisions } from '../../hooks/useDecisions';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';

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
      <div className="space-y-2">
        <p className="text-sm text-gray-600">
          Current stage: <strong>{data.current_stage}</strong> | 
          Treatment line: <strong>{data.current_treatment_line}</strong>
        </p>
        <p className="text-sm text-gray-600">
          {data.recommendations.length} recommendations available
        </p>
      </div>
    </Card>
  );
};
```

**Manual Test 9.3.1** - Test Hook and Structure:

Update `frontend/src/App.tsx` to add TreatmentRecommendations (in 3-column layout later, for now just test):

```typescript
import { TreatmentRecommendations } from './components/decisions/TreatmentRecommendations';

// Add after DiseaseTimeline:
<TreatmentRecommendations patientId={selectedPatientId} />
```

1. Save files
2. Select NGDX-001
3. ✅ **EXPECTED**:
   - Card title: "Treatment Recommendations"
   - Current stage: IVB
   - Treatment line: 2
   - Count: 2 recommendations available (for NGDX-001)

**✅ CHECKPOINT 9.3**: TreatmentRecommendations structure working

---

### Step 9.4: Create RecommendationCard Component

**Goal**: Display individual recommendation with badges

**File**: `frontend/src/components/decisions/TreatmentRecommendations.tsx` (UPDATE)

Add before TreatmentRecommendations component:

```typescript
import { useState } from 'react';
import { ChevronDown, ChevronUp, BookOpen } from 'lucide-react';
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
```

**What This Does**:
- Priority badge (color-coded: red/orange/blue/gray)
- Evidence level badge (custom colors: green for Level I RCT, blue for Level II, etc.)
- Confidence badge (High=green, Moderate=yellow, Low=gray)
- Recommendation as heading (bold)
- Rationale as body text
- Guideline reference with book icon (italics)
- Expandable supporting data (JSON formatted)
- Hover shadow effect

**Manual Test 9.4.1** - Test RecommendationCard:

Update TreatmentRecommendations return to display cards:

```typescript
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
```

1. Save file
2. With NGDX-001 selected:
3. ✅ **EXPECTED (Recommendation 1)**:
   - Badges: "High" (orange), "Level II (Phase II)" (blue), "Moderate confidence" (yellow)
   - Recommendation: "Consider adding MET inhibitor (Tepotinib or Savolitinib) to Osimertinib"
   - Rationale: "MET amplification detected as acquired resistance..."
   - Reference: "GEOMETRY-E1 trial (Wu et al., Lancet Resp Med 2023); TATTON trial..."
   - "Show Supporting Data" button

4. ✅ **EXPECTED (Recommendation 2)**:
   - Similar structure
   - Different content (T790M + MET dual combination)

**Manual Test 9.4.2** - Test Expand/Collapse:
1. Click "Show Supporting Data" on first recommendation
2. ✅ **EXPECTED**:
   - Gray box expands below
   - JSON data displayed (mutations_detected, current_treatment, etc.)
   - Button changes to "Hide Supporting Data"
3. Click again
4. ✅ **EXPECTED**: Data collapses

**Visual Confirmation**:
- ✅ Badges are prominent and color-coded correctly
- ✅ Evidence levels are clear (Level I = highest = green)
- ✅ Recommendation text is easy to read
- ✅ Reference citations are subtle but accessible
- ✅ Supporting data is optional but available

**✅ CHECKPOINT 9.4**: RecommendationCard complete

---

### Step 9.5: Test Treatment Recommendations with Multiple Patients

**Goal**: Verify component works for different scenarios

**Manual Test 9.5.1** - NGDX-001 (Has Recommendations):
1. Select NGDX-001
2. ✅ **VERIFY**:
   - 2 recommendations display
   - Both are "High" priority
   - Both are "Level II" evidence
   - MET inhibitor recommendation present
   - Dual combination recommendation present

**Manual Test 9.5.2** - Other Patients:
1. Select NGDX-002, NGDX-003, etc.
2. ✅ **VERIFY**:
   - Different numbers of recommendations
   - Or "No active recommendations" message
   - No errors in console

**Manual Test 9.5.3** - Clinical Validation:
1. Read NGDX-001 recommendations
2. ✅ **CLINICAL CHECK**:
   - MET amp detected → MET inhibitor recommended ✓
   - T790M detected → Keep 3rd-gen TKI ✓
   - References cite actual trials (GEOMETRY-E1, TATTON) ✓
   - Evidence levels are appropriate (Phase II = Level II) ✓

**Visual Confirmation**:
- ✅ Component is actionable and clinically useful
- ✅ Evidence hierarchy is clear
- ✅ Recommendations are concise but complete
- ✅ References provide credibility

**✅ CHECKPOINT 9.5**: TreatmentRecommendations COMPLETE!

---

## Phase 9 Complete Summary

**TreatmentRecommendations Component** is fully built with:
- ✅ Clinical decision rules display
- ✅ Evidence level badges (Level I-IV color-coded)
- ✅ Priority badges (Urgent/High/Medium/Low)
- ✅ Confidence indicators (High/Moderate/Low)
- ✅ Guideline references with citations
- ✅ Expandable supporting data
- ✅ Trial references (FLAURA, AURA3, GEOMETRY-E1, etc.)
- ✅ Tested with multiple patients
- ✅ Clinical validation complete

**Progress**: 67 checkpoints complete out of ~100 total

---

## Phase 10: Alerts Panel Component

### Step 10.1: Add Alerts Types (if not already in decisions.ts)

**File**: `frontend/src/types/decisions.ts` (UPDATE if needed)

Already defined in Step 9.1 - Alert interface exists.

**✅ CHECKPOINT 10.1**: Alert types confirmed

---

### Step 10.2: Create useAlerts Hook

**Goal**: Fetch active clinical alerts

**File**: `frontend/src/hooks/useAlerts.ts` (NEW FILE)

```typescript
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { Alert } from '../types/decisions';

interface AlertsResponse {
  patient_id: string;
  alerts: Alert[];
  overdue_tests: string[];
  total_active_alerts: number;
}

export function useAlerts(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.alerts, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<AlertsResponse>(
        `/api/patients/${patientId}/alerts`
      );
      return response.data;
    },
    enabled: !!patientId,
  });
}
```

**✅ CHECKPOINT 10.2**: useAlerts hook created

---

### Step 10.3: Create AlertPanel Component Structure

**Goal**: Basic alert display component

**File**: `frontend/src/components/alerts/AlertPanel.tsx` (NEW FILE)

```typescript
import React from 'react';
import { useAlerts } from '../../hooks/useAlerts';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import { Badge } from '../common/Badge';

interface AlertPanelProps {
  patientId: string | null;
}

export const AlertPanel: React.FC<AlertPanelProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = useAlerts(patientId);

  if (!patientId) {
    return (
      <Card title="Active Alerts">
        <p className="text-gray-500 text-center py-8">
          Please select a patient to view alerts
        </p>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title="Active Alerts">
        <LoadingSpinner message="Loading alerts..." />
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Active Alerts">
        <ErrorMessage
          message={`Failed to load alerts: ${error.message}`}
          onRetry={() => refetch()}
        />
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Active Alerts">
        <p className="text-gray-500">No data available</p>
      </Card>
    );
  }

  return (
    <Card title="Active Alerts">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Clinical Alerts</h3>
        <Badge variant="danger" size="lg">
          {data.total_active_alerts}
        </Badge>
      </div>
      
      {data.alerts.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-green-600 font-medium">✓ No active alerts</p>
          <p className="text-sm text-gray-500 mt-1">Patient status is stable</p>
        </div>
      ) : (
        <div className="space-y-3">
          {data.alerts.map(alert => (
            <div key={alert.alert_id} className="p-3 bg-red-50 rounded border border-red-200">
              <p className="font-semibold text-red-800">{alert.message}</p>
              <p className="text-xs text-red-600 mt-1">Severity: {alert.severity}</p>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};
```

**Manual Test 10.3.1** - Test AlertPanel:

Update `frontend/src/App.tsx`:

```typescript
import { AlertPanel } from './components/alerts/AlertPanel';

// Add after TreatmentRecommendations:
<AlertPanel patientId={selectedPatientId} />
```

1. Save files
2. Select NGDX-001
3. ✅ **EXPECTED**:
   - Card title: "Active Alerts"
   - "Clinical Alerts" heading with red badge showing count (e.g., "2")
   - 2 alert boxes (red background):
     - Rising ctDNA VAF alert
     - Resistance mutation alert

**✅ CHECKPOINT 10.3**: AlertPanel structure working

---

### Step 10.4: Create AlertCard Component with Severity Styling

**Goal**: Detailed alert display with color-coded severity

**File**: `frontend/src/components/alerts/AlertPanel.tsx` (UPDATE)

Add before AlertPanel component:

```typescript
import { AlertCircle, AlertTriangle, Info, Clock } from 'lucide-react';
import type { Alert } from '../../types/decisions';

interface AlertCardProps {
  alert: Alert;
}

const AlertCard: React.FC<AlertCardProps> = ({ alert }) => {
  // Severity configuration
  const severityConfig = {
    Critical: {
      bg: 'bg-red-50',
      border: 'border-cpi-red',
      icon: AlertCircle,
      iconColor: 'text-cpi-red',
      textColor: 'text-red-800',
    },
    High: {
      bg: 'bg-orange-50',
      border: 'border-cpi-orange',
      icon: AlertTriangle,
      iconColor: 'text-cpi-orange',
      textColor: 'text-orange-800',
    },
    Medium: {
      bg: 'bg-blue-50',
      border: 'border-blue-400',
      icon: Info,
      iconColor: 'text-blue-600',
      textColor: 'text-blue-800',
    },
    Low: {
      bg: 'bg-gray-50',
      border: 'border-gray-300',
      icon: Clock,
      iconColor: 'text-gray-600',
      textColor: 'text-gray-800',
    },
  };

  const config = severityConfig[alert.severity] || severityConfig.Medium;
  const Icon = config.icon;

  return (
    <div className={`${config.bg} border-l-4 ${config.border} rounded-r p-4`}>
      <div className="flex items-start gap-3">
        <Icon className={`h-5 w-5 ${config.iconColor} flex-shrink-0 mt-0.5`} />
        
        <div className="flex-1">
          {/* Alert message */}
          <p className={`font-semibold ${config.textColor} mb-1`}>
            {alert.message}
          </p>
          
          {/* Trigger date */}
          <p className="text-xs text-gray-500 mb-2">
            Triggered: {new Date(alert.trigger_date).toLocaleDateString()}
          </p>
          
          {/* Action recommendation (if requires action) */}
          {alert.requires_action && (
            <div className="mt-3 p-3 bg-white rounded-lg border border-gray-200">
              <p className="text-xs font-medium text-cpi-blue-600 mb-1">
                Recommended Action:
              </p>
              <p className="text-sm text-gray-700">
                {alert.action_recommendation}
              </p>
            </div>
          )}
          
          {/* Severity badge */}
          <div className="mt-2">
            <Badge 
              variant={alert.severity === 'Critical' || alert.severity === 'High' ? 'danger' : alert.severity === 'Medium' ? 'info' : 'default'} 
              size="sm"
            >
              {alert.severity}
            </Badge>
          </div>
        </div>
      </div>
    </div>
  );
};
```

Update AlertPanel return to use AlertCard:

```typescript
{data.alerts.length === 0 ? (
  // ... no alerts message ...
) : (
  <div className="space-y-3">
    {data.alerts.map(alert => (
      <AlertCard key={alert.alert_id} alert={alert} />
    ))}
  </div>
)}
```

**What Changed**:
- Severity-based color coding (Critical=red, High=orange, Medium=blue, Low=gray)
- Icons for each severity level
- Thick left border (4px) in severity color
- Action recommendation in white box (if applicable)
- Severity badge at bottom
- Clean, scannable layout

**Manual Test 10.4.1** - Verify Alert Styling:
1. Save file
2. With NGDX-001 selected:
3. ✅ **EXPECTED (Alert 1 - Rising VAF)**:
   - Red/orange background
   - AlertCircle or AlertTriangle icon (red/orange)
   - Message: "ctDNA VAF increased 155x from nadir (0.08% → 12.4%)"
   - Triggered date: 5/14/2022
   - White box with action: "Molecular progression detected. Consider repeat imaging..."
   - Severity badge: "High" (red)

4. ✅ **EXPECTED (Alert 2 - Resistance)**:
   - Similar red/orange styling
   - Message: "Acquired resistance mutations detected: T790M (EGFR), MET amplification"
   - Action recommendation visible

**Visual Confirmation**:
- ✅ Critical/High alerts are impossible to miss
- ✅ Color coding is consistent with medical urgency
- ✅ Action recommendations are actionable
- ✅ Layout is clean despite information density

**✅ CHECKPOINT 10.4**: AlertCard with severity styling complete

---

### Step 10.5: Add Overdue Tests Section

**Goal**: Display overdue follow-up tests

**File**: `frontend/src/components/alerts/AlertPanel.tsx` (UPDATE)

Add after alerts list:

```typescript
{/* Overdue Tests */}
{data.overdue_tests && data.overdue_tests.length > 0 && (
  <div className="mt-4 pt-4 border-t border-gray-200">
    <div className="flex items-center gap-2 mb-3">
      <Clock className="h-4 w-4 text-orange-600" />
      <h4 className="text-sm font-semibold text-gray-700">Overdue Tests</h4>
    </div>
    <div className="space-y-2">
      {data.overdue_tests.map((test, index) => (
        <div 
          key={index}
          className="p-2 bg-yellow-50 rounded border border-yellow-200 text-sm text-yellow-800"
        >
          {test}
        </div>
      ))}
    </div>
  </div>
)}
```

**Manual Test 10.5.1** - Test Overdue Section:
1. If NGDX-001 has overdue tests, they'll display
2. If not, section won't appear (conditional rendering)
3. ✅ **VERIFY**:
   - Yellow background boxes
   - Clock icon
   - Test descriptions are clear

**✅ CHECKPOINT 10.5**: Overdue tests section added

---

### Step 10.6: Test Complete Alerts Panel

**Goal**: Comprehensive testing of alert functionality

**Manual Test 10.6.1** - Full Alert Review (NGDX-001):
1. Select NGDX-001
2. Scroll to Alerts card
3. ✅ **VERIFY**:
   - Count badge shows correct number
   - All alerts have appropriate severity colors
   - Icons match severity levels
   - Messages are clear and specific
   - Trigger dates are formatted
   - Action recommendations provide guidance
   - Severity badges are visible

**Manual Test 10.6.2** - Test Other Patients:
1. Select patients without alerts
2. ✅ **EXPECTED**:
   - "No active alerts" message
   - Green checkmark
   - "Patient status is stable" text

**Manual Test 10.6.3** - Clinical Validation:
1. Review rising VAF alert
2. ✅ **VERIFY**:
   - VAF increase is clinically significant (155x from nadir)
   - Threshold is appropriate (≥2x from nadir)
   - Action recommendation is evidence-based (CHRYSALIS-2 trial)
3. Review resistance mutation alert
4. ✅ **VERIFY**:
   - Mutations listed (T790M, MET amp)
   - Mechanism is actionable
   - Treatment recommendation is appropriate

**Visual Confirmation**:
- ✅ Alerts are prominent without being alarming
- ✅ Severity hierarchy is clear
- ✅ Information is actionable
- ✅ Layout is professional

**✅ CHECKPOINT 10.6**: AlertPanel COMPLETE!

---

## Phase 10 Complete Summary

**AlertPanel Component** is fully built with:
- ✅ Active alerts display
- ✅ Severity color coding (Critical/High/Medium/Low)
- ✅ Severity-specific icons
- ✅ Action recommendations
- ✅ Alert count badge
- ✅ Overdue tests section
- ✅ "No alerts" state (positive messaging)
- ✅ Tested with multiple patients
- ✅ Clinical validation complete

**Progress**: 73 checkpoints complete out of ~100 total

---

## Phase 11: Final Dashboard Integration

### Step 11.1: Create Dashboard Layout (3-Column Grid)

**Goal**: Arrange all components in professional layout

**File**: `frontend/src/App.tsx` (MAJOR UPDATE)

```typescript
import { useState } from 'react';
import { Header } from './components/layout/Header';
import { DisclaimerBanner } from './components/common/DisclaimerBanner';
import { Footer } from './components/layout/Footer';
import { PatientSelector } from './components/patient/PatientSelector';
import { PatientSummary } from './components/patient/PatientSummary';
import { MolecularProfile } from './components/patient/MolecularProfile';
import { DiseaseTimeline } from './components/timeline/DiseaseTimeline';
import { TreatmentRecommendations } from './components/decisions/TreatmentRecommendations';
import { AlertPanel } from './components/alerts/AlertPanel';
import './App.css';

function App() {
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(null);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Fixed Header */}
      <Header />
      
      {/* Fixed Disclaimer */}
      <DisclaimerBanner />
      
      {/* Main Content */}
      <main className="container mx-auto px-6 py-8 flex-1">
        {/* Patient Selector - Full Width */}
        <div className="mb-6">
          <PatientSelector
            selectedPatientId={selectedPatientId}
            onSelect={setSelectedPatientId}
          />
        </div>

        {/* Dashboard Grid - 3 Columns */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column - Patient Info (4 cols) */}
          <div className="lg:col-span-4 space-y-6">
            <PatientSummary patientId={selectedPatientId} />
            <MolecularProfile patientId={selectedPatientId} />
          </div>

          {/* Center Column - Timeline (5 cols) */}
          <div className="lg:col-span-5">
            <DiseaseTimeline patientId={selectedPatientId} />
          </div>

          {/* Right Column - Decisions & Alerts (3 cols) */}
          <div className="lg:col-span-3 space-y-6">
            <AlertPanel patientId={selectedPatientId} />
            <TreatmentRecommendations patientId={selectedPatientId} />
          </div>

        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
```

**What Changed**:
- 12-column grid layout
- Left (4 cols): PatientSummary + MolecularProfile stacked
- Center (5 cols): DiseaseTimeline (largest)
- Right (3 cols): AlertPanel + TreatmentRecommendations stacked
- PatientSelector above grid (full width)
- Responsive: stacks vertically on mobile (< 1024px)

**Manual Test 11.1.1** - Desktop Layout (1920px):
1. Maximize browser window
2. Select NGDX-001
3. ✅ **VERIFY LAYOUT**:
   - 3 columns visible side-by-side
   - Left column: Patient data
   - Center column: Timeline chart (tallest)
   - Right column: Alerts on top, Recommendations below
   - Spacing is comfortable
   - No components feel cramped

**Manual Test 11.1.2** - Tablet Layout (768-1023px):
1. Resize to ~900px width
2. ✅ **EXPECTED**:
   - Columns stack vertically
   - Order: Patient selector → Patient info → Timeline → Alerts → Recommendations
   - All content readable

**Manual Test 11.1.3** - Mobile Layout (375px):
1. Toggle device toolbar, select iPhone SE
2. ✅ **EXPECTED**:
   - Single column, full stack
   - Horizontal scrolling never occurs
   - Touch interactions work
   - Charts are readable (though small)

**Visual Confirmation**:
- ✅ Dashboard looks professional and organized
- ✅ Visual hierarchy guides the eye
- ✅ Information density is appropriate
- ✅ Layout adapts gracefully to screen size

**✅ CHECKPOINT 11.1**: Dashboard layout complete

---

### Step 11.2: Add Loading State for Initial Load

**Goal**: Better UX when no patient selected yet

**File**: `frontend/src/App.tsx` (UPDATE)

Add after patient selector, before grid:

```typescript
{!selectedPatientId && (
  <div className="text-center py-16">
    <div className="max-w-md mx-auto">
      <div className="h-24 w-24 mx-auto mb-4 bg-cpi-blue-100 rounded-full flex items-center justify-center">
        <User className="h-12 w-12 text-cpi-blue" />
      </div>
      <h2 className="text-2xl font-semibold text-gray-900 mb-2">
        Welcome to the EGFR-NSCLC Dashboard
      </h2>
      <p className="text-gray-600">
        Please select a patient from the dropdown above to view their clinical data, 
        molecular profile, disease timeline, and treatment recommendations.
      </p>
    </div>
  </div>
)}

{selectedPatientId && (
  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
    {/* ... existing grid ... */}
  </div>
)}
```

Import User icon:
```typescript
import { User } from 'lucide-react';
```

**Manual Test 11.2.1** - Initial State:
1. Refresh browser
2. ✅ **EXPECTED**:
   - No patient selected
   - Centered welcome message
   - User icon in blue circle
   - Clear instructions

3. Select NGDX-001
4. ✅ **EXPECTED**:
   - Welcome message disappears
   - Dashboard grid appears

**✅ CHECKPOINT 11.2**: Welcome state added

---

### Step 11.3: Add Print Styles (Optional Enhancement)

**Goal**: Better print layout for clinical documentation

**File**: `frontend/src/index.css` (APPEND)

```css
@media print {
  /* Hide non-essential elements */
  .no-print,
  header,
  footer,
  button,
  input[type="checkbox"] {
    display: none !important;
  }
  
  /* Force white background */
  body {
    background: white !important;
  }
  
  /* Avoid page breaks inside cards */
  .card, .border {
    page-break-inside: avoid;
  }
  
  /* Show URLs in links */
  a[href]:after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666;
  }
}
```

**Manual Test 11.3.1** - Print Preview:
1. Select NGDX-001 (full data loaded)
2. Press Ctrl+P (print preview)
3. ✅ **EXPECTED**:
   - Header/footer hidden
   - No checkboxes visible
   - White background
   - All patient data visible
   - Charts render (as images)
   - Clean, professional appearance

**✅ CHECKPOINT 11.3**: Print styles added

---

### Step 11.4: Comprehensive Testing Checklist

**Goal**: Full system verification

**Manual Test 11.4.1** - Complete Patient Workflow (NGDX-001):

1. ✅ **Start State**:
   - Welcome message visible
   - No API calls yet

2. ✅ **Select Patient (NGDX-001)**:
   - Dropdown shows full patient list
   - Selection updates immediately
   - 6 API calls made in parallel:
     - GET /api/patients
     - GET /api/patients/NGDX-001/summary
     - GET /api/patients/NGDX-001/molecular
     - GET /api/patients/NGDX-001/timeline
     - GET /api/patients/NGDX-001/decisions
     - GET /api/patients/NGDX-001/alerts

3. ✅ **Patient Summary (Left Column)**:
   - Demographics: 73yo Female, NHS 4000007963
   - Baseline labs: ECOG 0, eGFR 113, normal CBC
   - Current status: Stage IVB, ECOG 1, Line 2 treatment

4. ✅ **Molecular Profile (Left Column)**:
   - Primary driver: EGFR Ex19del (blue card)
   - Resistance: T790M + MET amp (red boxes)
   - Co-mutations: TP53 R273H (gray)
   - PD-L1: 3% (gradient box)
   - NGS: Guardant360, 11,500x coverage

5. ✅ **Timeline Chart (Center Column)**:
   - Blue line: EGFR Ex19del VAF (38.5% → 0.08% → 12.4%)
   - Red dashed: T790M VAF (8.2% at end only)
   - Gray bars: Tumor diameter (15.6mm → 0 → 35mm)
   - 12+ events listed below
   - Toggle controls work

6. ✅ **Alert Panel (Right Column, Top)**:
   - Count: 2 alerts
   - Rising VAF alert (red/orange)
   - Resistance mutation alert (red/orange)
   - Action recommendations visible

7. ✅ **Treatment Recommendations (Right Column, Bottom)**:
   - 2 recommendations
   - MET inhibitor combination (High priority, Level II)
   - Dual therapy recommendation (High priority, Level II)
   - Guideline references visible

**Manual Test 11.4.2** - Switch Patients:
1. Select NGDX-002
2. ✅ **VERIFY**:
   - All components update
   - Different data displays
   - No stale NGDX-001 data
   - Smooth transition
3. Select NGDX-001 again
4. ✅ **VERIFY**:
   - Data loads instantly (from cache)
   - No new API calls
   - All data correct

**Manual Test 11.4.3** - Error Handling:
1. Stop backend server
2. Select a new patient or refresh page
3. ✅ **VERIFY**:
   - Error messages appear in each component
   - "Try Again" buttons visible
   - No crashes, no white screen
4. Restart backend
5. Click "Try Again" buttons
6. ✅ **VERIFY**: Components recover successfully

**Manual Test 11.4.4** - Performance:
1. Open DevTools → Network tab
2. Select NGDX-001
3. ✅ **VERIFY**:
   - All 6 API calls complete in < 2 seconds total
   - No duplicate requests
   - Charts render smoothly
4. Open Performance tab
5. Record timeline while switching patients
6. ✅ **VERIFY**:
   - No significant lag
   - 60fps maintained (or close)
   - No memory leaks

**✅ CHECKPOINT 11.4**: Comprehensive testing complete

---

### Step 11.5: Cross-Browser Testing

**Goal**: Ensure compatibility across major browsers

**Manual Test 11.5.1** - Chrome/Edge (Chromium):
1. Open in Chrome (or Edge)
2. Test full workflow
3. ✅ **VERIFY**: Everything works as expected

**Manual Test 11.5.2** - Firefox:
1. Open in Firefox
2. Test full workflow
3. ✅ **VERIFY**:
   - Charts render correctly
   - Colors match
   - Interactions work
   - No console errors

**Manual Test 11.5.3** - Safari (if available):
1. Open in Safari
2. Test full workflow
3. ✅ **VERIFY**: Compatible behavior

**✅ CHECKPOINT 11.5**: Cross-browser compatible

---

### Step 11.6: Accessibility Audit

**Goal**: Ensure dashboard is accessible

**Manual Test 11.6.1** - Keyboard Navigation:
1. Tab through entire dashboard
2. ✅ **VERIFY**:
   - Patient dropdown is reachable
   - Toggle checkboxes are reachable
   - Expand buttons are reachable
   - Focus rings are visible (CPI blue)
   - Tab order is logical

**Manual Test 11.6.2** - Screen Reader Labels:
1. Check all inputs have labels
2. ✅ **VERIFY**:
   - Dropdown has "Select Patient" label
   - Checkboxes have descriptive labels
   - Icons have aria-labels (if needed)

**Manual Test 11.6.3** - Color Contrast:
1. Use DevTools → Lighthouse → Accessibility
2. Run audit
3. ✅ **TARGET**: Score ≥ 90
4. Fix any contrast issues flagged

**✅ CHECKPOINT 11.6**: Accessibility audit complete

---

### Step 11.7: Final Polish

**Goal**: Last-minute improvements

**Manual Test 11.7.1** - Visual Consistency:
1. Check all cards have same border radius (8px)
2. Check all spacing is consistent (gap-6 between components)
3. Check all fonts are Inter
4. Check all blue colors are CPI blue (#0058AA)

**Manual Test 11.7.2** - Error Message Clarity:
1. Review all error messages
2. Ensure they provide actionable guidance
3. No generic "Error occurred" messages

**Manual Test 11.7.3** - Loading States:
1. Throttle network (DevTools → Network → Slow 3G)
2. Select patient
3. ✅ **VERIFY**:
   - Loading spinners are clear
   - No layout shift when data loads
   - Progressive rendering (components load independently)

**✅ CHECKPOINT 11.7**: Final polish complete

---

### Step 11.8: Create README Documentation

**Goal**: Document how to run the dashboard

**File**: `frontend/README.md` (NEW FILE)

```markdown
# EGFR-NSCLC Clinical Dashboard

React dashboard for displaying patient clinical data, molecular profiles, disease timelines, and treatment recommendations.

## Quick Start

### Prerequisites
- Node.js 18+
- npm 9+
- Backend API running on http://localhost:8000

### Installation

\`\`\`bash
cd frontend
npm install
\`\`\`

### Development

\`\`\`bash
npm run dev
\`\`\`

Dashboard will be available at: http://localhost:5173

### Build for Production

\`\`\`bash
npm run build
\`\`\`

Built files will be in `dist/` directory.

## Features

- **Patient Selection**: Dropdown to select from 5 patients
- **Patient Summary**: Demographics, baseline labs, current status (3-column layout)
- **Molecular Profile**: Driver mutations, resistance mutations, co-mutations, PD-L1 status
- **Disease Timeline**: VAF trends + tumor diameter over time (Recharts)
- **Treatment Recommendations**: Evidence-based clinical decision rules
- **Alert Panel**: Active clinical alerts (rising VAF, resistance mutations)

## Technology Stack

- **React** 18.3
- **TypeScript** 5.5
- **Vite** 5.4
- **TanStack Query** 5.x (data fetching)
- **Recharts** 2.12 (charts)
- **Tailwind CSS** 3.4 (styling)
- **Lucide React** (icons)

## Project Structure

\`\`\`
frontend/
├── src/
│   ├── components/
│   │   ├── layout/          # Header, Footer, DisclaimerBanner
│   │   ├── patient/         # PatientSelector, PatientSummary, MolecularProfile
│   │   ├── timeline/        # DiseaseTimeline
│   │   ├── decisions/       # TreatmentRecommendations
│   │   ├── alerts/          # AlertPanel
│   │   ├── common/          # Card, Badge, LoadingSpinner, ErrorMessage, DataRow
│   │   └── ui/              # (future reusable UI components)
│   ├── hooks/               # usePatients, usePatientSummary, useMolecularProfile, useTimeline, useDecisions, useAlerts
│   ├── types/               # TypeScript type definitions
│   ├── api/                 # API client (Axios)
│   ├── config/              # Constants (API URL, colors)
│   ├── App.tsx              # Main dashboard layout
│   └── main.tsx             # Entry point with React Query provider
├── public/
│   └── assets/
│       └── cpi-logo.png     # CPI logo
├── tailwind.config.js       # CPI color palette
├── package.json
└── README.md
\`\`\`

## API Endpoints Used

- `GET /api/patients` - List all patients
- `GET /api/patients/{id}/summary` - Patient demographics
- `GET /api/patients/{id}/molecular` - Molecular profile
- `GET /api/patients/{id}/timeline` - Timeline data
- `GET /api/patients/{id}/decisions` - Treatment recommendations
- `GET /api/patients/{id}/alerts` - Active alerts

## CPI Branding

Colors:
- Primary Blue: #0058AA
- Navy (header): #001d38
- Red (alerts): #d3353d
- Orange (warnings): #ff9200
- Teal (success): #007169

## Testing

Tested with:
- 5 patients (NGDX-001 to NGDX-005)
- All browsers (Chrome, Firefox, Safari, Edge)
- Responsive design (desktop, tablet, mobile)
- Accessibility (keyboard navigation, WCAG AA)

## Known Limitations

- Demonstration system only - NOT for clinical use
- Read-only (no data editing)
- 5 sample patients only
- Requires backend API to be running

## Support

For issues or questions, refer to:
- System Spec: `00-SYSTEM-SPEC.md`
- Backend API Spec: `02-backend-api.md`
- CPI Branding: `CPI_BRAND_GUIDELINES.md`
\`\`\`

**✅ CHECKPOINT 11.8**: README documentation complete

---

## Phase 11 Complete Summary

**Dashboard Integration** is fully complete with:
- ✅ 3-column responsive layout
- ✅ All 6 components integrated
- ✅ Parallel API calls
- ✅ React Query caching
- ✅ Welcome state for initial load
- ✅ Print styles
- ✅ Comprehensive testing (all patients)
- ✅ Error handling (try again buttons)
- ✅ Performance optimization
- ✅ Cross-browser compatibility
- ✅ Accessibility audit
- ✅ Final polish
- ✅ README documentation

**Progress**: 81 checkpoints complete

---

## Final Summary: Complete Implementation Guide

### 📊 Total Checkpoints Completed: 81

### ✅ All Phases Complete:

**Phase 0: Environment Setup** (5 checkpoints)
- Backend verification
- Vite project initialization  
- Dependencies installation
- Tailwind initialization
- First dev server test

**Phase 1: Tailwind Configuration** (7 checkpoints)
- Content paths
- CPI brand colors (tested)
- CPI typography (Inter font)
- Base styles
- Project folder structure
- Constants file
- CPI logo setup

**Phase 2: Basic Layout** (7 checkpoints)
- Header (logo + title + version)
- Disclaimer banner (red warning)
- Footer (project info)

**Phase 3: Reusable Components** (8 checkpoints)
- Card (normal + highlighted)
- Badge (5 variants, 3 sizes)
- ECOGBadge (auto color-coded)
- StageBadge (auto color-coded)
- LoadingSpinner (animated)
- ErrorMessage (with retry)
- DataRow (label-value pairs)

**Phase 4: API Integration** (9 checkpoints)
- API client with interceptors
- React Query provider
- Patient types
- usePatients hook (tested with caching)
- usePatientSummary hook
- Molecular types
- useMolecularProfile hook

**Phase 5: Patient Selector** (2 checkpoints)
- PatientSelector structure
- Full styling with CPI branding

**Phase 6: Patient Summary** (7 checkpoints)
- Component structure
- Demographics section
- Baseline labs section
- Current status section
- Responsive layout
- Multi-patient testing
- Hover effects

**Phase 7: Molecular Profile** (8 checkpoints)
- Component structure
- MutationCard component
- Primary driver section
- Resistance mutations (red alert)
- Co-mutations section
- PD-L1 status display
- NGS test footer
- Multi-patient testing

**Phase 8: Timeline Chart** (10 checkpoints)
- Timeline types
- useTimeline hook
- Component structure
- Recharts installation test
- VAF data transformation
- VAF line chart
- RECIST bars (dual-axis)
- Toggle controls
- Timeline events list
- Complete integration test

**Phase 9: Treatment Recommendations** (5 checkpoints)
- Recommendations types
- useDecisions hook
- Component structure
- RecommendationCard with badges
- Multi-patient testing

**Phase 10: Alerts Panel** (6 checkpoints)
- Alert types confirmation
- useAlerts hook
- Component structure
- AlertCard with severity styling
- Overdue tests section
- Complete integration test

**Phase 11: Final Integration** (8 checkpoints)
- Dashboard layout (3-column grid)
- Welcome state
- Print styles
- Comprehensive testing
- Cross-browser testing
- Accessibility audit
- Final polish
- README documentation

---

## 🎯 What You Now Have

### **Complete Specifications** for:

1. ✅ **Environment Setup** - Exact commands to run
2. ✅ **Project Configuration** - Tailwind, TypeScript, React Query
3. ✅ **Reusable Components** - 8 building blocks
4. ✅ **API Integration** - 6 hooks with caching
5. ✅ **Patient Selector** - Dropdown with full patient info
6. ✅ **Patient Summary** - 3-column responsive layout
7. ✅ **Molecular Profile** - Driver + resistance + co-mutations
8. ✅ **Timeline Chart** - VAF + RECIST + events (Recharts)
9. ✅ **Treatment Recommendations** - Evidence-based rules
10. ✅ **Alerts Panel** - Severity-coded alerts
11. ✅ **Dashboard Layout** - Complete integration

### **Each Checkpoint Includes**:
- ✅ Exact code to write
- ✅ File path and location
- ✅ What changed explanation
- ✅ Manual test steps (numbered)
- ✅ Expected results (with ✅ checkboxes)
- ✅ Visual confirmation checklist
- ✅ Clinical validation (where applicable)

### **Testing Coverage**:
- ✅ All 5 patients (NGDX-001 to NGDX-005)
- ✅ Loading states
- ✅ Error states with retry
- ✅ Caching behavior
- ✅ Responsive design (mobile/tablet/desktop)
- ✅ Cross-browser (Chrome, Firefox, Safari)
- ✅ Accessibility (keyboard, screen readers)
- ✅ Performance (< 2 second load)

---

## 🚀 Ready to Implement

You now have **3 detailed specification files**:
1. **FRONTEND_DETAILED_GUIDE.md** - Phases 0-3 (Environment through UI Components)
2. **FRONTEND_DETAILED_GUIDE_PHASES_4-10.md** - Phases 4-7 (API through Molecular Profile)
3. **FRONTEND_DETAILED_GUIDE_FINAL.md** - Phases 8-11 (Timeline through Final Integration)

**Total**: ~200+ pages of ultra-detailed, step-by-step implementation guide

**Next Step**: Start implementing Phase 0.1 and follow the guide checkpoint by checkpoint! 🎨

---

**END OF COMPLETE SPECIFICATION**