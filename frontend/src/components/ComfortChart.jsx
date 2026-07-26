import { useEffect, useState } from "react";
import {
  ResponsiveContainer, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Cell,
} from "recharts";
import { Paper, Typography, Box, CircularProgress, Chip } from "@mui/material";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import { getComfort } from "../services/analyticsService";

const COLORS = ["#22C55E", "#2563EB", "#F59E0B"];

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <Box sx={{ bgcolor:"#0F172A", color:"#fff", p:1.5, borderRadius:2, fontSize:13 }}>
      <Typography sx={{ fontWeight:700, mb:0.5, fontSize:12 }}>{label}</Typography>
      <Box sx={{ display:"flex", justifyContent:"space-between", gap:2 }}>
        <span style={{ color: payload[0]?.fill }}>Comfort</span>
        <span style={{ fontWeight:600 }}>{Number(payload[0]?.value).toFixed(4)}</span>
      </Box>
    </Box>
  );
};

export default function ComfortChart() {
  const [data, setData]       = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getComfort()
      .then((res) =>
        setData([
          { name: "Minimum", comfort: Number(res.minimum) },
          { name: "Average", comfort: Number(res.average) },
          { name: "Maximum", comfort: Number(res.maximum) },
        ])
      )
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
          <Typography variant="h6" fontWeight={700}>Comfort Statistics</Typography>
          <Typography variant="body2" color="text.secondary">
            Min / Avg / Max comfort predictions
          </Typography>
        </Box>
        <Chip icon={<ThermostatIcon />} label="Healthy" color="success" size="small" />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <CircularProgress />
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <BarChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="name" tick={{ fontSize: 13 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="comfort" radius={[12, 12, 0, 0]} animationDuration={1000}>
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
