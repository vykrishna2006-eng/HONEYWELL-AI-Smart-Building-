import { useEffect, useState } from "react";
import {
  ResponsiveContainer, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ReferenceLine,
} from "recharts";
import {
  Paper, Typography, Box, CircularProgress,
  Chip, Stack, Avatar,
} from "@mui/material";
import AcUnitIcon    from "@mui/icons-material/AcUnit";
import LocalFireIcon from "@mui/icons-material/LocalFireDepartment";
import api from "../api/api";

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <Box sx={{
      bgcolor: "#0F172A", color: "#fff", p: 1.5,
      borderRadius: 2, fontSize: 13, minWidth: 170,
      boxShadow: "0 8px 24px rgba(0,0,0,0.3)",
    }}>
      <Typography sx={{ fontWeight: 700, mb: 0.5, fontSize: 11, color: "#94A3B8" }}>
        Iteration {label}
      </Typography>
      {payload.map((p) => (
        <Box key={p.dataKey}
          sx={{ display: "flex", justifyContent: "space-between", gap: 2 }}>
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ fontWeight: 600 }}>
            {p.value != null ? `${p.value}°C` : "Baseline"}
          </span>
        </Box>
      ))}
    </Box>
  );
};

// Convert "Baseline" or null → null (skip on chart), keep valid floats
function parseSetpoint(v) {
  if (v == null || v === "" || String(v).toLowerCase() === "baseline") return null;
  const n = parseFloat(v);
  return isNaN(n) ? null : n;
}

export default function SetpointChart() {
  const [data,    setData]    = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/api/dashboard/history")
      .then((r) => {
        const rows = Array.isArray(r.data) ? r.data : [];
        setData(
          rows.map((row) => ({
            iteration: row.iteration,
            cooling:   parseSetpoint(row.cooling_setpoint),
            heating:   parseSetpoint(row.heating_setpoint),
          }))
        );
      })
      .catch(() => setData([]))
      .finally(() => setLoading(false));
  }, []);

  // Stats for mini badges
  const validCool = data.map(d => d.cooling).filter(v => v != null);
  const validHeat = data.map(d => d.heating).filter(v => v != null);
  const avgCool = validCool.length ? (validCool.reduce((a,b) => a+b,0)/validCool.length).toFixed(1) : null;
  const avgHeat = validHeat.length ? (validHeat.reduce((a,b) => a+b,0)/validHeat.length).toFixed(1) : null;

  return (
    <Paper
      className="hover-lift fade-in"
      sx={{ p: 3, border: "1px solid #E2E8F0", height: 420 }}
    >
      {/* Header */}
      <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
        <Box>
          <Typography variant="h6" fontWeight={700}>HVAC Setpoints</Typography>
          <Typography variant="body2" color="text.secondary">
            AI-optimised cooling / heating setpoints per iteration
          </Typography>
        </Box>
        <Chip icon={<AcUnitIcon />} label="HVAC" color="info" size="small" />
      </Box>

      {/* Mini stat row */}
      {(avgCool || avgHeat) && (
        <Stack direction="row" spacing={2} mb={2}>
          {avgCool && (
            <Box sx={{ display:"flex", alignItems:"center", gap:0.5 }}>
              <AcUnitIcon sx={{ color:"#06B6D4", fontSize:16 }} />
              <Typography variant="caption" fontWeight={600} color="#06B6D4">
                Avg Cooling: {avgCool}°C
              </Typography>
            </Box>
          )}
          {avgHeat && (
            <Box sx={{ display:"flex", alignItems:"center", gap:0.5 }}>
              <LocalFireIcon sx={{ color:"#EF4444", fontSize:16 }} />
              <Typography variant="caption" fontWeight={600} color="#EF4444">
                Avg Heating: {avgHeat}°C
              </Typography>
            </Box>
          )}
        </Stack>
      )}

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="70%">
          <CircularProgress />
        </Box>
      ) : data.length === 0 || (validCool.length === 0 && validHeat.length === 0) ? (
        <Box
          display="flex" flexDirection="column"
          justifyContent="center" alignItems="center" height="70%"
        >
          <AcUnitIcon sx={{ fontSize: 48, color: "#CBD5E1", mb: 1 }} />
          <Typography color="text.secondary" fontWeight={500}>
            No setpoint data yet
          </Typography>
          <Typography variant="caption" color="text.secondary" mt={0.5}>
            Run the closed-loop simulation to generate HVAC setpoints
          </Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height="78%">
          <LineChart
            data={data}
            margin={{ top: 8, right: 16, left: -4, bottom: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis
              dataKey="iteration"
              tick={{ fontSize: 11 }}
              label={{ value: "Iteration", position: "insideBottom", offset: -2, fontSize: 11 }}
            />
            <YAxis
              tick={{ fontSize: 11 }}
              domain={[14, 30]}
              tickFormatter={(v) => `${v}°C`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            {/* Comfort zone band */}
            <ReferenceLine y={22} stroke="#06B6D4" strokeDasharray="4 4"
              label={{ value: "22°C", fill: "#06B6D4", fontSize: 9, position: "left" }} />
            <ReferenceLine y={20} stroke="#EF4444" strokeDasharray="4 4"
              label={{ value: "20°C", fill: "#EF4444", fontSize: 9, position: "left" }} />
            <Line
              type="monotone"
              dataKey="cooling"
              name="Cooling (°C)"
              stroke="#06B6D4"
              strokeWidth={2.5}
              dot={{ r: 5, fill: "#06B6D4" }}
              connectNulls={false}
              activeDot={{ r: 7 }}
            />
            <Line
              type="monotone"
              dataKey="heating"
              name="Heating (°C)"
              stroke="#EF4444"
              strokeWidth={2.5}
              dot={{ r: 5, fill: "#EF4444" }}
              connectNulls={false}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
