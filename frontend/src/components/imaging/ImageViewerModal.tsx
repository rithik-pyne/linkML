import React, { useState, useEffect } from 'react';
import { X, ZoomIn, ZoomOut, ChevronLeft, ChevronRight } from 'lucide-react';
import { format } from 'date-fns';
import type { ImagingStudy } from '../../hooks/useImagingStudies';

interface ImageViewerModalProps {
  study: ImagingStudy;
  studies: ImagingStudy[];
  onClose: () => void;
  onNavigate?: (study: ImagingStudy) => void;
}

export const ImageViewerModal: React.FC<ImageViewerModalProps> = ({
  study,
  studies,
  onClose,
  onNavigate,
}) => {
  const [zoom, setZoom] = useState(100);

  // Find current index
  const currentIndex = studies.findIndex(s => s.imaging_study_id === study.imaging_study_id);
  const hasPrevious = currentIndex > 0;
  const hasNext = currentIndex < studies.length - 1;

  // Keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      } else if (e.key === 'ArrowLeft' && hasPrevious && onNavigate) {
        onNavigate(studies[currentIndex - 1]);
      } else if (e.key === 'ArrowRight' && hasNext && onNavigate) {
        onNavigate(studies[currentIndex + 1]);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentIndex, hasPrevious, hasNext, onClose, onNavigate, studies]);

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const imagePath = study.dicom_file_path
    ? `/static/imaging/full/${study.dicom_file_path}`
    : study.thumbnail_image_path
    ? `/static/imaging/thumbnails/${study.thumbnail_image_path}`
    : null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black bg-opacity-90 flex items-center justify-center p-4"
      onClick={handleBackdropClick}
    >
      <div className="bg-white rounded-lg max-w-7xl w-full max-h-[95vh] flex flex-col shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b bg-gray-50">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {study.imaging_modality} - {study.study_description}
            </h3>
            <p className="text-sm text-gray-600 mt-1">
              {format(new Date(study.scan_date), 'PPP')} • {study.ajcc_stage}
            </p>
          </div>
          <div className="flex items-center gap-3">
            {/* Zoom Controls */}
            <div className="flex items-center gap-2 bg-white border rounded-lg px-3 py-1">
              <button
                onClick={() => setZoom(Math.max(50, zoom - 25))}
                className="p-1 hover:bg-gray-100 rounded"
                title="Zoom out"
                disabled={zoom <= 50}
              >
                <ZoomOut className="h-4 w-4 text-gray-600" />
              </button>
              <span className="text-sm text-gray-700 font-medium min-w-[60px] text-center">
                {zoom}%
              </span>
              <button
                onClick={() => setZoom(Math.min(200, zoom + 25))}
                className="p-1 hover:bg-gray-100 rounded"
                title="Zoom in"
                disabled={zoom >= 200}
              >
                <ZoomIn className="h-4 w-4 text-gray-600" />
              </button>
            </div>

            {/* Close Button */}
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
              title="Close (ESC)"
            >
              <X className="h-5 w-5 text-gray-600" />
            </button>
          </div>
        </div>

        {/* Image Viewer */}
        <div className="flex-1 overflow-auto bg-gray-900 flex items-center justify-center p-6">
          {imagePath ? (
            <img
              src={imagePath}
              alt={study.study_description}
              style={{ width: `${zoom}%`, maxWidth: 'none' }}
              className="object-contain"
            />
          ) : (
            <div className="text-center text-gray-400">
              <p className="text-lg">No image available</p>
              <p className="text-sm mt-2">DICOM file not found</p>
            </div>
          )}
        </div>

        {/* Metadata Footer */}
        <div className="p-4 border-t bg-gray-50">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
            <div>
              <p className="text-gray-600 font-medium">TNM Stage</p>
              <p className="text-gray-900">{study.t_stage}{study.n_stage}{study.m_stage}</p>
            </div>
            <div>
              <p className="text-gray-600 font-medium">Primary Tumor</p>
              <p className="text-gray-900">
                {study.primary_tumor_diameter_mm ? `${study.primary_tumor_diameter_mm} mm` : 'N/A'}
              </p>
            </div>
            {study.suv_max && (
              <div>
                <p className="text-gray-600 font-medium">SUV Max</p>
                <p className="text-gray-900">{study.suv_max}</p>
              </div>
            )}
            {study.brain_metastasis_present && (
              <div>
                <p className="text-gray-600 font-medium">Brain Metastases</p>
                <p className="text-cpi-red font-semibold">
                  {study.brain_lesion_count} lesion(s)
                </p>
              </div>
            )}
            <div>
              <p className="text-gray-600 font-medium">Accession #</p>
              <p className="text-gray-900 font-mono text-xs">
                {study.accession_number || 'N/A'}
              </p>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between pt-3 border-t">
            <button
              onClick={() => hasPrevious && onNavigate && onNavigate(studies[currentIndex - 1])}
              disabled={!hasPrevious}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                hasPrevious
                  ? 'bg-cpi-blue text-white hover:bg-cpi-blue-600'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              <ChevronLeft className="h-4 w-4" />
              Previous
            </button>

            <span className="text-sm text-gray-600">
              Study {currentIndex + 1} of {studies.length}
            </span>

            <button
              onClick={() => hasNext && onNavigate && onNavigate(studies[currentIndex + 1])}
              disabled={!hasNext}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                hasNext
                  ? 'bg-cpi-blue text-white hover:bg-cpi-blue-600'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              Next
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};