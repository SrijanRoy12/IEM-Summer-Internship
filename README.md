# IEM-Summer-Internship
🔍 Trained or Used Models (Based on Project Description)
1. Pre-trained Foundation Models (Not Trained from Scratch):
GPT (e.g., GPT-4, GPT-3.5):

Used for planning, predictions, agent decision logic, report generation.

Likely not retrained but used through APIs (OpenAI, Azure, etc.).

DALL·E / Sora / GenAI Visualization Models:

For generating city layouts, visual trend maps, emergency simulations.

Also likely not trained in your app but used via prompts (generative image/video outputs).

2. Agentic AI Frameworks (AutoGen / CrewAI):
These do not train models themselves, but rather orchestrate tasks between agents using LLMs and rules.

Each agent operates via role-based prompts and memory/context sharing — no separate ML training happens here unless extended.

3. Custom-Trained (Optional) Models (If Implemented):
You might have trained or fine-tuned models like:

✅ Traffic Congestion Predictor (e.g., Regression, LSTM, or XGBoost using real-time data)

✅ Pollution Level Forecaster (Time-series or statistical models)

✅ Energy Demand Predictor (Multivariate forecasting)

✅ Emergency Incident Classifier (Could be ML-based using past incident data)

✅ Crime Detection (Object detection / anomaly detection using YOLO, OpenCV, or CNNs)| Component                             | Model Type      | Trained?              | Notes                                             |
| ------------------------------------- | --------------- | --------------------- | ------------------------------------------------- |
| **LLMs (GPT)**                        | Generative AI   | ❌ (Used via API)      | Used for decisions, explanations, and simulations |
| **DALL·E / Sora**                     | Gen Image/Video | ❌                     | Visualizing simulations                           |
| **Traffic/Energy/Crime Prediction**   | ML/Stat Models  | ✅ (if custom-trained) | Optional, depending on dataset availability       |
| **Agent Framework (AutoGen, CrewAI)** | Orchestration   | ❌                     | No training; just coordination logic              |
