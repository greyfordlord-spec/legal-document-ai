@echo off
echo Testing Python installation...
python --version
echo.
echo Testing Streamlit installation...
pip show streamlit
echo.
echo Running test app...
python -m streamlit run app-test.py --server.port 8502
pause
