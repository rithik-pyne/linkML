import React from 'react';
import { Calendar, FileImage } from 'lucide-react';
import { format } from 'date-fns';
import { Badge } from '../common/Badge';
import type { ImagingStudy } from '../../hooks/useImagingStudies';

interface ImagingStudyCardProps {
  study: ImagingStudy;
  onViewImage: () => void;
}

export const ImagingStudyCard: React.FC<ImagingStudyCardProps> = ({ study, onViewImage }) => {
  const hasImage = study.dicom_file_path || study.thumbnail_image_path;
  const thumbnailPath = study.thumbnail_image_path
    ? `/static/imaging/thumbnails/${study.thumbnail_image_path}`
    : null;

  return (
    <div className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
      {/* Thumbnail */}
      <div className="relative h-48 bg-gray-900 flex items-center justify-center">
        {thumbnailPath ? (
          <img
            src={thumbnailPath}
            alt={study.study_description}
            className="h-full w-full object-contain"
          />
        ) : (
          <FileImage className="h-16 w-16 text-gray-600" />
        )}

        {/* Stage Badge Overlay */}
        <div className="absolute top-2 right-2">
          <Badge
            variant={
              study.ajcc_stage?.includes('IV') ? 'danger' :
              study.ajcc_stage?.includes('III') ? 'warning' :
              'info'
            }
            size="sm"
          >
            {study.ajcc_stage}
          </Badge>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <div className="flex items-center gap-2 mb-2">
          <Calendar className="h-4 w-4 text-gray-500" />
          <span className="text-sm font-medium text-gray-900">
            {format(new Date(study.scan_date), 'MMM dd, yyyy')}
          </span>
        </div>

        <h4 className="font-semibold text-gray-900 mb-1">
          {study.imaging_modality}
        </h4>
        <p className="text-sm text-gray-600 mb-3">
          {study.study_description}
        </p>

        {/* Metadata Grid */}
        <div className="grid grid-cols-2 gap-2 text-xs text-gray-600 mb-3 pb-3 border-b">
          <div>
            <span className="font-medium">TNM:</span> {study.t_stage}{study.n_stage}{study.m_stage}
          </div>
          {study.primary_tumor_diameter_mm && (
            <div>
              <span className="font-medium">Tumor:</span> {study.primary_tumor_diameter_mm}mm
            </div>
          )}
          {study.suv_max && (
            <div>
              <span className="font-medium">SUV Max:</span> {study.suv_max}
            </div>
          )}
          {study.brain_metastasis_present && (
            <div className="col-span-2 text-cpi-red font-medium">
              Brain mets: {study.brain_lesion_count} lesion(s)
            </div>
          )}
        </div>

        {/* View Button */}
        <button
          onClick={onViewImage}
          disabled={!hasImage}
          className={`w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            hasImage
              ? 'bg-cpi-blue text-white hover:bg-cpi-blue-600'
              : 'bg-gray-100 text-gray-400 cursor-not-allowed'
          }`}
        >
          <FileImage className="h-4 w-4" />
          {hasImage ? 'View Full Image' : 'No Image Available'}
        </button>
      </div>
    </div>
  );
};