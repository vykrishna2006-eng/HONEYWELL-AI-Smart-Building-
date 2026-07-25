import api from "../api/api";

export const getRooms = async () => {
  const response = await api.get("/rooms");
  return response.data;
};