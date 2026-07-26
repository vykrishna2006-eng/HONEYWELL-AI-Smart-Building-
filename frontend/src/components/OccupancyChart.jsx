import { useEffect, useState } from "react";
import {
  ResponsiveContainer, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { Paper, Typography, Box, CircularProgress, Chip } from "@mui/material";
import PeopleIcon from "@mui/icons-material/People";
import api from "../api/api";

export default function OccupancyChart() {
  const [data, setData]       = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/dashboard/history")
      .then((r) => {
        const rows = Array.isArray(r.data) ? r.data : [];
        setData(
          rows.map((row) => ({
            iteration: row.iteration,
            occupancy: Number(row.occupancy) || 0,
          }))
        );
      })
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  // Color bar by occupancy level
  const maxOcc = Math.max(...data.map((d) => d.occupancy), 1);
  const getColor = (val) => {
    const ratio = val / maxOcc;
    if (ratio < 0.33) return "#22C55E";
    if (ratio < 0.66) return "#F59E0B";
    return "#EF4444";
  };

  return (
    <Paper
      className="hover-lift fade-in"
      sx={{ p: 3, border: "1px solid #E2E8F0", height: 400 }}
    >
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box>
          <Typography variant="h6" fontWeight={700}>Occupancy Levels</Typography>
          <Typography variant="body2" color="text.secondary">
            Sensor-reported occupancy per iteration
          </Typography>
        </Box>
        <Chip icon={<PeopleIcon />} label="Occupancy" size="small"
          sx={{ bgcolor: "#FFF7ED", color: "#EA580C" }} />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <CircularProgress />
        </Box>
      ) : data.length === 0 ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <Typography color="text.secondary">No data yet.</Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <BarChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="iteration" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip
              contentStyle={{ borderRadius: 12, border: "none" }}
              formatter={(v) => [v, "Occupancy"]}
            />
            <Bar dataKey="occupancy" radius={[6, 6, 0, 0]} animationDuration={1000}>
              {data.map((entry, i) => (
                <Cell key={i} fill={getColor(entry.occupancy)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
