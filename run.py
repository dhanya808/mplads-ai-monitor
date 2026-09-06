import uvicorn
import os
import sys

if __name__ == '__main__':
    print('=' * 70)
    print('  MPLADS AI Monitor — Explainable AI Risk & Anomaly Detection Platform')
    print('  Ministry of Statistics & Programme Implementation (MoSPI) - DIID')
    print('=' * 70)
    print('  Starting server on http://127.0.0.1:8000')
    print('  Swagger API Documentation: http://127.0.0.1:8000/docs')
    print('=' * 70)

    uvicorn.run('backend.app.main:app', host='127.0.0.1', port=8000, reload=True)
