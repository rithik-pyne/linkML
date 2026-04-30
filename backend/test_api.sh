#!/bin/bash

# Backend API Test Suite
# Run all endpoints with curl to verify functionality
# Usage: bash backend/test_api.sh

BASE_URL="http://localhost:8000"

echo "=========================================="
echo "Backend API Test Suite"
echo "=========================================="
echo ""

# Check if server is running
echo "Checking if server is running..."
if ! curl -s "$BASE_URL/" > /dev/null 2>&1; then
    echo "ERROR: Server is not running at $BASE_URL"
    echo "Start server with: uvicorn backend.app.main:app --reload"
    exit 1
fi
echo "✓ Server is running"
echo ""

# Test 1: Root health check
echo "1. GET / - Health check"
curl -s "$BASE_URL/" | python -m json.tool
echo ""

# Test 2: Database status
echo "2. GET /api/db/status - Database status"
curl -s "$BASE_URL/api/db/status" | python -m json.tool
echo ""

# Test 3: Patient list
echo "3. GET /api/patients - Patient list"
curl -s "$BASE_URL/api/patients" | python -m json.tool
echo ""

# Test 4: Patient summary
echo "4. GET /api/patients/NGDX-001/summary - Patient summary"
curl -s "$BASE_URL/api/patients/NGDX-001/summary" | python -m json.tool
echo ""

# Test 5: Molecular profile
echo "5. GET /api/patients/NGDX-001/molecular - Molecular profile"
curl -s "$BASE_URL/api/patients/NGDX-001/molecular" | python -m json.tool
echo ""

# Test 6: Imaging history
echo "6. GET /api/patients/NGDX-001/imaging - Imaging history"
curl -s "$BASE_URL/api/patients/NGDX-001/imaging" | python -m json.tool
echo ""

# Test 7: Treatment history
echo "7. GET /api/patients/NGDX-001/treatments - Treatment history"
curl -s "$BASE_URL/api/patients/NGDX-001/treatments" | python -m json.tool
echo ""

# Test 8: Response assessments
echo "8. GET /api/patients/NGDX-001/response - Response assessments"
curl -s "$BASE_URL/api/patients/NGDX-001/response" | python -m json.tool
echo ""

# Test 9: Clinical assessments
echo "9. GET /api/patients/NGDX-001/clinical - Clinical assessments"
curl -s "$BASE_URL/api/patients/NGDX-001/clinical" | python -m json.tool
echo ""

# Test 10: Timeline
echo "10. GET /api/patients/NGDX-001/timeline - Disease timeline"
curl -s "$BASE_URL/api/patients/NGDX-001/timeline" | python -m json.tool
echo ""

# Test 11: Treatment decisions
echo "11. GET /api/patients/NGDX-001/decisions - Treatment recommendations"
curl -s "$BASE_URL/api/patients/NGDX-001/decisions" | python -m json.tool
echo ""

# Test 12: Alerts
echo "12. GET /api/patients/NGDX-001/alerts - Active alerts"
curl -s "$BASE_URL/api/patients/NGDX-001/alerts" | python -m json.tool
echo ""

# Test 13: 404 Error handling
echo "13. GET /api/patients/INVALID-999/summary - 404 Error test"
curl -s "$BASE_URL/api/patients/INVALID-999/summary" | python -m json.tool
echo ""

# Test all patients
echo "14. Testing all 5 patients..."
for patient in NGDX-001 NGDX-002 NGDX-003 NGDX-004 NGDX-005; do
    response=$(curl -s "$BASE_URL/api/patients/$patient/summary")
    if echo "$response" | grep -q "patient_id"; then
        echo "  ✓ $patient - OK"
    else
        echo "  ✗ $patient - FAILED"
    fi
done
echo ""

echo "=========================================="
echo "Test Suite Complete!"
echo "=========================================="
echo ""
echo "Interactive Documentation:"
echo "  Swagger UI: $BASE_URL/docs"
echo "  ReDoc:      $BASE_URL/redoc"