import { useState } from 'react';
import { User } from 'lucide-react';
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
          <div className="space-y-6">
            {/* Top Row - Patient Summary (Full Width) */}
            <PatientSummary patientId={selectedPatientId} />

            {/* Second Row - 2 Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column - Molecular Profile */}
              <div>
                <MolecularProfile patientId={selectedPatientId} />
              </div>

              {/* Right Column - Alerts & Recommendations */}
              <div className="space-y-6">
                <AlertPanel patientId={selectedPatientId} />
                <TreatmentRecommendations patientId={selectedPatientId} />
              </div>
            </div>

            {/* Third Row - Timeline (Full Width) */}
            <DiseaseTimeline patientId={selectedPatientId} />
          </div>
        )}
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;