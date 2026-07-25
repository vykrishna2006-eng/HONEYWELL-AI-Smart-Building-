import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";

import {
  Paper,
  Typography,
  Box,
  Chip,
} from "@mui/material";

import ThermostatIcon from "@mui/icons-material/Thermostat";

import { getComfort } from "../services/analyticsService";

function ComfortChart() {

  const [data, setData] = useState([]);

  useEffect(() => {
    loadComfort();
  }, []);

  const loadComfort = async () => {

    try {

      const res = await getComfort();

      setData([
        {
          name: "Minimum",
          comfort: Number(res.minimum),
        },
        {
          name: "Average",
          comfort: Number(res.average),
        },
        {
          name: "Maximum",
          comfort: Number(res.maximum),
        },
      ]);

    } catch (err) {

      console.log(err);

    }

  };

  const colors = [
    "#22C55E",
    "#16A34A",
    "#15803D",
  ];

  return (

    <Paper
      elevation={0}
      sx={{
        p: 3,
        borderRadius: 5,
        height: 420,
        border: "1px solid #E2E8F0",
        background:
          "linear-gradient(145deg,#ffffff,#f8fafc)",
      }}
    >

      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={3}
      >

        <Box>

          <Typography
            variant="h6"
            fontWeight={700}
          >
            Comfort Analysis
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Indoor comfort level comparison
          </Typography>

        </Box>

        <Chip
          icon={<ThermostatIcon />}
          label="Healthy"
          color="success"
        />

      </Box>

      <ResponsiveContainer
        width="100%"
        height="85%"
      >

        <BarChart
          data={data}
        >

          <CartesianGrid
            strokeDasharray="5 5"
            stroke="#E5E7EB"
          />

          <XAxis
            dataKey="name"
            tick={{
              fontSize: 13,
            }}
          />

          <YAxis
            tick={{
              fontSize: 13,
            }}
          />

          <Tooltip
            contentStyle={{
              borderRadius: 12,
              border: "none",
              boxShadow:
                "0 10px 25px rgba(0,0,0,.15)",
            }}
          />

          <Bar
            dataKey="comfort"
            radius={[12,12,0,0]}
            animationDuration={1200}
          >
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={colors[index]}
              />
            ))}
          </Bar>

        </BarChart>

      </ResponsiveContainer>

    </Paper>

  );

}

export default ComfortChart;