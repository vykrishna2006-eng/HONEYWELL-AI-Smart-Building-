import api from "../api/api";

// Get AI recommendation
export const getRecommendation = async () => {
    const response = await api.get("/llm/recommendation");
    return response.data;
};

// Alias used by the redesigned UI
export const generateRecommendation = async () => {
    const response = await api.get("/llm/recommendation");
    return response.data;
};