import api from "../api/api";

export const runSimulation = async () => {
  const response = await api.post("/simulation/run");
  return response.data;
};

export const runClosedLoop = async (iterations = 2) => {
  const response = await api.post(`/simulation/run-closed-loop?iterations=${iterations}`);
  return response.data;
};

export const getClosedLoopReport = async () => {
  const response = await api.get("/simulation/closed-loop-report");
  return response.data;
};

export const getLiveMetrics = async () => {
  const response = await api.get("/simulation/metrics");
  return response.data;
};

export const evaluatePerformance = async () => {
  const response = await api.get("/simulation/evaluate");
  return response.data;
};

export const getSimulationErrors = async () => {
  const response = await api.get("/simulation/errors");
  return response.data;
};
