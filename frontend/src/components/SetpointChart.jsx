import { useEffect, useState } from "react";
import {
  ResponsiveContainer, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from "recharts";
import { Paper, Typography, Box, CircularProgress, Chip } from "@mui/material";
import AcUnitIcon from "@mui/icons-material/AcUnit";
import api from "../api/api";

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <Box sx={{ bgcolor:"#0F172A", color:"#fff", p:1.5, borderRadius:2, fontSize:13, minWidth:160 }}>
      <Typography sx={{ fontWeight:700, mb:0.5, fontSize:11, color:"#94A3B8" }}>
        Iteration {label}
      </Typography>
      {payload.map((p) => (
        <Box key={p.dataKey} sx={{ display:"flex", justifyContent:"space-between", gap:2 }}>
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ fontWeight:600 }}>{p.value}°C</span>
        </Box>
      ))}
    </Box>
  );
};

export default function SetpointChart() {
  const [data, setData]       = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/dashboard/history")
      .then((r) => {
        const rows = Array.isArray(r.data) ? r.data : [];
        setData(
          rows.map((row) => ({
            iteration: row.iteration,
            cooling:   row.cooling_setpoint,
            heating:   row.heating_setpoint,
            occupancy: Number(row.occupancy) || 0,
          }))
        );
      })
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Paper
      className="hover-lift fade-in"
      sx={{ p: 3, border: "1px solid #E2E8F0", height: 400 }}
    >
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box>
          <Typography variant="h6" fontWeight={700}>HVAC Setpoints</Typography>
          <Typography variant="body2" color="text.secondary">
            Cooling / Heating setpoints per iteration
          </Typography>
        </Box>
        <Chip icon={<AcUnitIcon />} label="HVAC" color="info" size="small" />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <CircularProgress />
        </Box>
      ) : data.length === 0 ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <Typography color="text.secondary">No simulation data yet.</Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <LineChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="iteration" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line type="monotone" dataKey="cooling" name="Cooling (°C)" stroke="#06B6D4" strokeWidth={2.5} dot={false} />
            <Line type="monotone" dataKey="heating" name="Heating (°C)" stroke="#EF4444" strokeWidth={2.5} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
