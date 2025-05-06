
#!/bin/bash
echo "Starting Rollbaserat Juridiskt AI-system..."
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 5000 --server.address 0.0.0.0
