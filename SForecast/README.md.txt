project-root/
│
├── WEB_UI/
│   ├── index.html
│   ├── forecast.html
│   ├── update_llm.html
│   ├── update_database.html
│   └── style.css
│
├── BACKEND/
│   ├── app.py
│   ├── requirements.txt
│   └── check.txt   (created at runtime)
│
└── README.md





Location: C:\Users\Sinsi\OneDrive\Documents\SForecast\Sforecast


cd C:\Users\Sinsi\OneDrive\Documents\SForecast\Sforecast
tree

cd BACKEND




curl -X POST "http://127.0.0.1:8000/check" -H "Content-Type: application/json" -d "{\"dataset\":\"Financial news dataset\",\"start_date\":\"2026-01-01\",\"end_date\":\"2026-01-10\",\"variable\":\"Inflation\",\"geography\":\"Sri Lanka\"}"



PS C:\Users\Sinsi> cd C:\Users\Sinsi\OneDrive\Documents\SForecast\SForecast\WEB_UI\
PS C:\Users\Sinsi\OneDrive\Documents\SForecast\SForecast\WEB_UI> python -m http.server 5500


python -m uvicorn app:app --reload
http://127.0.0.1:8000/docs#/default/check_data_check_post



    #query = '("inflation forecast" OR "predicted inflation" OR "expected inflation" OR "CPI projection") AND ("higher than expected" OR "lower than expected" OR "missed forecast" OR "forecast deviation" OR "inflation surprise")'
    # query = '("GDP forecast" OR "economic growth forecast" OR "GDP estimate" OR "GDP projection") AND ("higher than expected" OR "lower than expected" OR "forecast deviation" OR "GDP surprise" OR "missed estimate")'
    # query = '("unemployment forecast" OR "jobless claims forecast" OR "employment projection") AND ("higher than expected" OR "lower than expected" OR "forecast deviation" OR "surprise" OR "missed estimate")'
    # query = '("interest rate forecast" OR "policy rate projection" OR "central bank rate expectation") AND ("higher than expected" OR "lower than expected" OR "rate surprise" OR "deviation from forecast")'
    # query = '("trade balance forecast" OR "current account forecast" OR "export projection" OR "import projection") AND ("higher than expected" OR "lower than expected" OR "surprise" OR "forecast deviation")'
    # query = '("consumer confidence forecast" OR "PMI forecast" OR "business sentiment projection") AND ("higher than expected" OR "lower than expected" OR "survey deviation" OR "forecast miss")'


