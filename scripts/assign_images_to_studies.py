"""
Assign CT images to imaging studies in the database
For the first 5 patients only (dashboard scope)
"""
import sqlite3

def assign_images():
    conn = sqlite3.connect('backend/clinical_data.db')
    cursor = conn.cursor()

    # Get all imaging studies for first 5 patients
    cursor.execute('''
        SELECT imaging_study_id, patient_id, scan_date, imaging_modality
        FROM ImagingStudy
        WHERE patient_id IN ('NGDX-001', 'NGDX-002', 'NGDX-003', 'NGDX-004', 'NGDX-005')
        ORDER BY patient_id, scan_date
    ''')

    studies = cursor.fetchall()

    # We have 7 CT images - cycle through them
    image_files = [
        ('lung_ct_001.jpg', 'lung_ct_001_thumb.jpg'),
        ('lung_ct_002.jpg', 'lung_ct_002_thumb.jpg'),
        ('lung_ct_003.jpg', 'lung_ct_003_thumb.jpg'),
        ('lung_ct_004.jpg', 'lung_ct_004_thumb.jpg'),
        ('lung_ct_005.jpg', 'lung_ct_005_thumb.jpg'),
        ('lung_ct_006.jpg', 'lung_ct_006_thumb.jpg'),
        ('lung_ct_007.jpg', 'lung_ct_007_thumb.jpg'),
    ]

    print(f'Assigning images to {len(studies)} imaging studies...\n')

    for i, study in enumerate(studies):
        study_id, patient_id, scan_date, modality = study

        # Cycle through images
        img_idx = i % len(image_files)
        full_img, thumb_img = image_files[img_idx]

        # Update database
        cursor.execute('''
            UPDATE ImagingStudy
            SET dicom_file_path = ?,
                thumbnail_image_path = ?
            WHERE imaging_study_id = ?
        ''', (full_img, thumb_img, study_id))

        print(f'  {patient_id} | {scan_date} | {modality:10s} -> {full_img}')

    conn.commit()
    print(f'\nDone! Updated {len(studies)} imaging studies with image paths')

    # Verify
    cursor.execute('''
        SELECT COUNT(*)
        FROM ImagingStudy
        WHERE patient_id IN ('NGDX-001', 'NGDX-002', 'NGDX-003', 'NGDX-004', 'NGDX-005')
        AND dicom_file_path IS NOT NULL
    ''')
    count = cursor.fetchone()[0]
    print(f'Verified: {count} studies now have images assigned')

    conn.close()

if __name__ == '__main__':
    assign_images()