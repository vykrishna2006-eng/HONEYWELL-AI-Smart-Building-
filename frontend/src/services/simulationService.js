import api from "../api/api";

export const runSimulation = async () => {
    const response = await api.post("/simulation/run");
    return response.data;
};