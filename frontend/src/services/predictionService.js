import api from "../api/api";

// ML Prediction
export const predict = async (data) => {
  const response = await api.post("/ml/predict", data);
  return response.data;
};

// Get all saved predictions
export const getPredictions = async () => {
  const response = await api.get("/predictions");
  return response.data;
};

// Get prediction by ID
export const getPrediction = async (id) => {
  const response = await api.get(`/predictions/${id}`);
  return response.data;
};

// Update prediction
export const updatePrediction = async (id, data) => {
  const response = await api.put(`/predictions/${id}`, data);
  return response.data;
};

// Delete prediction
export const deletePrediction = async (id) => {
  const response = await api.delete(`/predictions/${id}`);
  return response.data;
};