import api from "../api/api";

export const getSensors = async () => {
  const response = await api.get("/sensors");
  return response.data;
};