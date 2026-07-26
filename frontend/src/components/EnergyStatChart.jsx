import { useEffect, useState } from "react";
import {
  ResponsiveContainer, RadialBarChart, RadialBar,
  PolarAngleAxis, Tooltip,
} from "recharts";
import { Paper, Typography, Box, CircularProgress, Stack } from "@mui/material";
import BoltIcon from "@mui/icons-material/Bolt";
import { getEnergy } from "../services/analyticsService";

export default function EnergyStatChart() {
  const [stats, setStats]     = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getEnergy()
      .then(setStats)
      .catch(() => setStats(null))
      .finally(() => setLoading(false));
  }, []);

  const max = stats?.maximum || 1;
  const chartData = stats
    ? [
        { name: "Maximum", value: 100,                                     fill: "#EF4444" },
        { name: "Average", value: ((stats.average / max) * 100).toFixed(1), fill: "#2563EB" },
        { name: "Minimum", value: ((stats.minimum / max) * 100).toFixed(1), fill: "#22C55E" },
      ]
    : [];

  return (
    <Paper
      className="hover-lift fade-in"
      sx={{ p: 3, border: "1px solid #E2E8F0", height: 400 }}
    >
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Box>
          <Typography variant="h6" fontWeight={700}>Energy Statistics</Typography>
          <Typography variant="body2" color="text.secondary">
            Min / Avg / Max energy predictions
          </Typography>
        </Box>
        <BoltIcon sx={{ color: "#2563EB", fontSize: 28 }} />
      </Box>

      {loading ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <CircularProgress />
        </Box>
      ) : !stats ? (
        <Box display="flex" justifyContent="center" alignItems="center" height="80%">
          <Typography color="text.secondary">No data available.</Typography>
        </Box>
      ) : (
        <>
          <ResponsiveContainer width="100%" height="62%">
            <RadialBarChart
              innerRadius="30%"
              outerRadius="90%"
              data={chartData}
              startAngle={90}
              endAngle={-270}
            >
              <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
              <RadialBar
                dataKey="value"
                cornerRadius={8}
                background={{ fill: "#F1F5F9" }}
                animationDuration={1200}
              />
              <Tooltip
                formatter={(v, name) => [`${v}%`, name]}
                contentStyle={{ borderRadius: 12, border: "none" }}
              />
            </RadialBarChart>
          </ResponsiveContainer>

          <Stack direction="row" justifyContent="space-around" mt={1}>
            {[
              { label: "Min",  val: stats.minimum, color: "#22C55E" },
              { label: "Avg",  val: stats.average, color: "#2563EB" },
              { label: "Max",  val: stats.maximum, color: "#EF4444" },
            ].map((s) => (
              <Box key={s.label} textAlign="center">
                <Typography variant="h5" fontWeight={800} sx={{ color: s.color }}>
                  {Number(s.val).toFixed(2)}
                </Typography>
                <Typography variant="caption" color="text.secondary">{s.label} kWh</Typography>
              </Box>
            ))}
          </Stack>
        </>
      )}
    </Paper>
  );
}
