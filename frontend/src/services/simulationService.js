import api from "../api/api";

export const runSimulation = async () => {
    const response = await api.post("/simulation/run");
    return response.data;
};

export const getClosedLoopReport = async () => {
    const response = await api.get("/simulation/closed-loop-report");
    return response.data;
};