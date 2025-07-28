# 🛠️ Machine Maintenance Dashboard

A real-time dashboard for monitoring the health of industrial machinery using live sensor metrics like temperature, vibration, pressure, and humidity. This project predicts hazard levels and maintenance needs using predictive analytics and visualizations.

<img width="1916" height="972" alt="Screenshot 2025-07-25 125706" src="https://github.com/user-attachments/assets/b86d9d30-c3f8-4d61-9e72-02e419ed3a58" />

*Main Interface with Machine Hazard Ratings*

---

## 📌 Features

* 🔍 **Real-time Monitoring** of industrial machines
* 📊 **Live Sensor Metrics**: Temperature, Vibration, Pressure, Humidity
* ⚠️ **Hazard Detection & Risk Levels** (in %)
* 📅 **Maintenance Scheduling**: Shows last and upcoming maintenance dates
* 📈 **Predictive Analysis** with accuracy metrics
* 📌 **Detailed Pop-ups** with historical trends per machine
* 🎨 Clean UI with interactive elements

---

## 🖼️ Additional Preview

<img width="1919" height="974" alt="Screenshot 2025-07-25 125759" src="https://github.com/user-attachments/assets/efdcbbbd-d334-4ca6-956a-fc1ece901829" />

*Live Graphs for Centrifugal Pump Monitoring*

---

## 🏗️ Tech Stack

| Layer               | Technology                        |
| ------------------- | --------------------------------- |
| Frontend            | HTML, CSS, Bootstrap              |
| Backend             | Python (Flask / FastAPI optional) |
| Machine Learning    | TensorFlow / PyTorch / Sklearn    |
| Data Visualization  | Matplotlib, Chart.js, Recharts    |
| Database (optional) | PostgreSQL / SQLite               |

---

## 🔧 How It Works

1. **Machine Cards**: Each card displays the machine name, current hazard percentage, and recommendation.
2. **Live Sensor Panel**: Clicking a card opens detailed metrics and trend plots for the last 24 hours.
3. **Predictive Engine**: Machine learning model predicts future risks and maintenance needs based on sensor data.
4. **Accuracy Metric**: Model performance is tracked and shown per machine.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Machine-Maintenance-Dashboard.git
cd Machine-Maintenance-Dashboard
```

### 2. Install dependencies

Make sure you have Python 3.8+ and pip installed.

```bash
pip install -r requirements.txt
```

If using Flask:

```bash
pip install flask flask_sqlalchemy flask_migrate
```

For FastAPI alternative:

```bash
pip install fastapi uvicorn
```

### 3. Run the app

#### For Flask:

```bash
python app.py
```

#### For FastAPI (if implemented):

```bash
uvicorn app:app --reload
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📂 Project Structure

```bash
.
├── backend/
│   ├── app.py                # Flask/FastAPI backend
│   ├── model/                # ML model files
│   └── database/             # DB models & migrations
├── frontend/
│   ├── index.html            # Main dashboard page
│   └── static/               # CSS, JS, and assets
├── data/
│   └── sensor_data.csv       # Raw or simulated machine data
├── requirements.txt
└── README.md
```

---

## 📈 Model & Prediction

* ML model trained to predict:

  * Hazard percentage
  * Likelihood of failure
  * Maintenance schedule
* Sensor features include:

  * `Temperature`, `Vibration`, `Pressure`, `Humidity`
* Accuracy metrics displayed visually in each machine's popup.

---

## 📊 Example Machine Stats

| Machine Name                    | Hazard % | Accuracy | Maintenance Due |
| ------------------------------- | -------- | -------- | --------------- |
| Centrifugal Compressor          | 99%      | 93%      | 2025-08-14      |
| Atmospheric Distillation Column | 94%      | 91%      | 2025-08-12      |
| Mechanical Draft Cooling Tower  | 100%     | 95%      | 2025-08-09      |

---

## 📦 Future Enhancements

* Add SMS/email alerts for critical hazard levels
* Integrate with actual IoT sensor APIs
* Add role-based authentication and user dashboards
* Expand ML model for root cause analysis

---

## 🧠 Credits

* UI Design: Bootstrap & Custom CSS
* ML Pipeline: Scikit-learn + TensorFlow
* Visualization: Matplotlib, Recharts
* API: Flask / FastAPI

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙌 Contribution

Feel free to fork, submit pull requests, or suggest enhancements via Issues. We welcome contributors!
