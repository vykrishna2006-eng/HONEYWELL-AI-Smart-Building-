import api from "../api/api";

export const getDashboard = async () => {
    const res = await api.get("/analytics/dashboard");
    return res.data;
};

export const getEnergy = async () => {
    const res = await api.get("/analytics/energy");
    return res.data;
};

export const getComfort = async () => {
    const res = await api.get("/analytics/comfort");
    return res.data;
};

export const getLatestRecommendation = async () => {
    const res = await api.get("/analytics/latest-recommendation");
    return res.data;
};

export const getPredictions = async () => {
    const res = await api.get("/analytics/predictions");
    return res.data;
};