Write-Host "Testing Python installation..." -ForegroundColor Green
try {
    python --version
} catch {
    Write-Host "Python not found in PATH" -ForegroundColor Red
}

Write-Host "`nTesting Streamlit installation..." -ForegroundColor Green
try {
    pip show streamlit
} catch {
    Write-Host "Streamlit not found" -ForegroundColor Red
}

Write-Host "`nRunning test app..." -ForegroundColor Green
try {
    python -m streamlit run app-test.py --server.port 8502
} catch {
    Write-Host "Error running app: $_" -ForegroundColor Red
}

Read-Host "Press Enter to continue"
