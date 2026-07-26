import { useEffect, useState } from "react";
import {
  ResponsiveContainer, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from "recharts";
import { Paper, Typography, Box, CircularProgress, Chip } from "@mui/material";
import BoltIcon from "@mui/icons-material/Bolt";
import api from "../api/api";

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <Box
      sx={{
        bgcolor: "#0F172A", color: "#fff",
        p: 1.5, borderRadius: 2, fontSize: 13,
        boxShadow: "0 8px 24px rgba(0,0,0,0.3)",
        minWidth: 150,
      }}
    >
      <Typography sx={{ fontWeight: 700, mb: 0.5, fontSize: 12 }}>
        Iteration {label}
      </Typography>
      {payload.map((p) => (
        <Box key={p.dataKey} sx={{ display: "flex", justifyContent: "space-between", gap: 2 }}>
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ fontWeight: 600 }}>{Number(p.value).toFixed(3)}</span>
        </Box>
      ))}
    </Box>
  );
};

export default function EnergyChart() {
  const [data, setData]       = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/dashboard/history")
      .then((r) => {
        const rows = Array.isArray(r.data) ? r.data : [];
        setData(
          rows.map((row) => ({
            iteration:    row.iteration,
            energy:       Number(row.energy_kwh)    || 0,
            cooling:      Number(row.cooling_kwh)   || 0,
            heating:      Number(row.heating_kwh)   || 0,
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
          <Typography variant="h6" fontWeight={700}>
            Energy Consumption
          </Typography>
          <Typography variant="body2" color="text.secondary">
            kWh per simulation iteration
          </Typography>
        </Box>
        <Chip icon={<BoltIcon />} label="Live" color="primary" size="small" />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <CircularProgress />
        </Box>
      ) : data.length === 0 ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <Typography color="text.secondary">No simulation data yet. Run a simulation first.</Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <AreaChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
            <defs>
              <linearGradient id="gradEnergy" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#2563EB" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#2563EB" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="gradCool" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#06B6D4" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#06B6D4" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="gradHeat" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#F59E0B" stopOpacity={0.2} />
                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="iteration" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Area type="monotone" dataKey="energy"  name="Total (kWh)"   stroke="#2563EB" fill="url(#gradEnergy)" strokeWidth={2.5} dot={false} />
            <Area type="monotone" dataKey="cooling" name="Cooling (kWh)" stroke="#06B6D4" fill="url(#gradCool)"   strokeWidth={2}   dot={false} />
            <Area type="monotone" dataKey="heating" name="Heating (kWh)" stroke="#F59E0B" fill="url(#gradHeat)"   strokeWidth={2}   dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
