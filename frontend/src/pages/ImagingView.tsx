import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { FileImage, Filter } from 'lucide-react';
import { useImagingStudies } from '../hooks/useImagingStudies';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { ErrorMessage } from '../components/common/ErrorMessage';
import { ImagingStudyCard } from '../components/imaging/ImagingStudyCard';
import { ImageViewerModal } from '../components/imaging/ImageViewerModal';
import type { ImagingStudy } from '../hooks/useImagingStudies';

export const ImagingView: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>();
  const { data, isLoading, error, refetch } = useImagingStudies(patientId || null);
  const [selectedStudy, setSelectedStudy] = useState<ImagingStudy | null>(null);
  const [modalityFilter, setModalityFilter] = useState<string>('all');

  if (isLoading) {
    return (
      <div className="container mx-auto px-6 py-8">
        <LoadingSpinner message="Loading imaging studies..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-6 py-8">
        <ErrorMessage
          message={`Failed to load imaging studies: ${error.message}`}
          onRetry={() => refetch()}
        />
      </div>
    );
  }

  if (!data || data.imaging_studies.length === 0) {
    return (
      <div className="container mx-auto px-6 py-8">
        <div className="text-center py-16">
          <FileImage className="h-16 w-16 mx-auto text-gray-300 mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            No Imaging Studies Available
          </h2>
          <p className="text-gray-600">
            No imaging data has been uploaded for this patient yet.
          </p>
        </div>
      </div>
    );
  }

  // Filter studies by modality
  const filteredStudies = modalityFilter === 'all'
    ? data.imaging_studies
    : data.imaging_studies.filter(s => s.imaging_modality === modalityFilter);

  // Get unique modalities for filter
  const modalities = Array.from(new Set(data.imaging_studies.map(s => s.imaging_modality)));

  return (
    <>
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Imaging Studies
            </h1>
            <p className="text-gray-600 mt-1">
              {data.total_scans} total scan{data.total_scans !== 1 ? 's' : ''} • Patient {data.patient_id}
            </p>
          </div>

          {/* Filter Dropdown */}
          {modalities.length > 1 && (
            <div className="relative">
              <label className="flex items-center gap-2 text-sm text-gray-700">
                <Filter className="h-4 w-4" />
                <select
                  value={modalityFilter}
                  onChange={(e) => setModalityFilter(e.target.value)}
                  className="border border-gray-300 rounded-lg px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-cpi-blue"
                >
                  <option value="all">All Modalities ({data.total_scans})</option>
                  {modalities.map(modality => {
                    const count = data.imaging_studies.filter(s => s.imaging_modality === modality).length;
                    return (
                      <option key={modality} value={modality}>
                        {modality} ({count})
                      </option>
                    );
                  })}
                </select>
              </label>
            </div>
          )}
        </div>

        {/* Studies Grid */}
        {filteredStudies.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <p className="text-gray-600">No studies match the selected filter.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredStudies.map((study) => (
              <ImagingStudyCard
                key={study.imaging_study_id}
                study={study}
                onViewImage={() => setSelectedStudy(study)}
              />
            ))}
          </div>
        )}
      </div>

      {/* Image Viewer Modal */}
      {selectedStudy && (
        <ImageViewerModal
          study={selectedStudy}
          studies={filteredStudies}
          onClose={() => setSelectedStudy(null)}
          onNavigate={setSelectedStudy}
        />
      )}
    </>
  );
};