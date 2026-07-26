import { useEffect, useState } from "react";
import {
  ResponsiveContainer, ComposedChart, Bar, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from "recharts";
import { Paper, Typography, Box, CircularProgress, Chip } from "@mui/material";
import QueryStatsIcon from "@mui/icons-material/QueryStats";
import { getPredictions } from "../services/analyticsService";

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <Box sx={{ bgcolor:"#0F172A", color:"#fff", p:1.5, borderRadius:2, fontSize:13, minWidth:170 }}>
      <Typography sx={{ fontWeight:700, mb:0.5, fontSize:11, color:"#94A3B8" }}>Prediction #{label}</Typography>
      {payload.map((p) => (
        <Box key={p.dataKey} sx={{ display:"flex", justifyContent:"space-between", gap:2 }}>
          <span style={{ color: p.color }}>{p.name}</span>
          <span style={{ fontWeight:600 }}>{Number(p.value).toFixed(3)}</span>
        </Box>
      ))}
    </Box>
  );
};

export default function PredictionHistoryChart() {
  const [data, setData]       = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPredictions()
      .then((rows) =>
        setData(
          rows.slice(-30).map((r, i) => ({
            id:      r.id ?? i + 1,
            energy:  Number(r.energy_prediction),
            comfort: Number(r.comfort_prediction),
            conf:    Number(r.confidence) * 100,
          }))
        )
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
          <Typography variant="h6" fontWeight={700}>Prediction History</Typography>
          <Typography variant="body2" color="text.secondary">
            Last 30 ML predictions (energy + comfort)
          </Typography>
        </Box>
        <Chip icon={<QueryStatsIcon />} label="ML" color="secondary" size="small" />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <CircularProgress />
        </Box>
      ) : data.length === 0 ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <Typography color="text.secondary">No predictions recorded yet.</Typography>
        </Box>
      ) : (
        <ResponsiveContainer width="100%" height="88%">
          <ComposedChart data={data} margin={{ top: 4, right: 4, left: -10, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
            <XAxis dataKey="id" tick={{ fontSize: 11 }} label={{ value: "Prediction ID", position: "insideBottom", offset: -2, fontSize: 11 }} />
            <YAxis yAxisId="left"  tick={{ fontSize: 11 }} />
            <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11 }} />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Bar    yAxisId="left"  dataKey="energy"  name="Energy (kWh)"  fill="#2563EB" radius={[4,4,0,0]} opacity={0.85} />
            <Bar    yAxisId="left"  dataKey="comfort" name="Comfort Score" fill="#22C55E" radius={[4,4,0,0]} opacity={0.85} />
            <Line   yAxisId="right" dataKey="conf"    name="Confidence (%)" stroke="#F59E0B" strokeWidth={2} dot={false} />
          </ComposedChart>
        </ResponsiveContainer>
      )}
    </Paper>
  );
}
