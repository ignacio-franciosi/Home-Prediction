const form = document.getElementById('prediction-form');
const resultValue = document.getElementById('result-value');
const resultDetail = document.getElementById('result-detail');
const payloadPreview = document.getElementById('payload-preview');
const statusPill = document.getElementById('status-pill');

const setStatus = (state, text) => {
  statusPill.className = `status-pill ${state}`;
  statusPill.textContent = text;
};

const formatNumber = (value) => new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 2,
}).format(value);

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());
  const numericFields = ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income'];

  numericFields.forEach((field) => {
    payload[field] = Number(payload[field]);
  });

  payloadPreview.textContent = JSON.stringify(payload, null, 2);
  setStatus('loading', 'Processing');
  resultDetail.textContent = 'Calculating prediction with the XGBoost model...';

  try {
    const response = await fetch('/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'No se pudo generar la predicción.');
    }

    resultValue.textContent = data.prediction_formatted;
    resultDetail.textContent = 'Prediction generated successfully using derived features from the form.';
    setStatus('ok', 'Ready');
  } catch (error) {
    setStatus('error', 'Error');
    resultDetail.textContent = error.message;
  }
});