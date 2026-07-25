import { useEffect, useState } from "react";

import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

import {
  Paper,
  Typography,
  Box,
  Chip,
} from "@mui/material";

import BoltIcon from "@mui/icons-material/Bolt";

import { getEnergy } from "../services/analyticsService";

function EnergyChart() {

  const [data, setData] = useState([]);

  useEffect(() => {
    loadEnergy();
  }, []);

  const loadEnergy = async () => {

    try {

      const res = await getEnergy();

      setData([
        {
          name: "Minimum",
          energy: Number(res.minimum),
        },
        {
          name: "Average",
          energy: Number(res.average),
        },
        {
          name: "Maximum",
          energy: Number(res.maximum),
        },
      ]);

    } catch (err) {
      console.log(err);
    }

  };

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
            Energy Consumption
          </Typography>

          <Typography
            variant="body2"
            color="text.secondary"
          >
            Minimum, Average and Maximum Energy Usage
          </Typography>

        </Box>

        <Chip
          icon={<BoltIcon />}
          label="Live"
          color="primary"
        />

      </Box>

      <ResponsiveContainer
        width="100%"
        height="85%"
      >

        <AreaChart data={data}>

          <defs>

            <linearGradient
              id="energyGradient"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >

              <stop
                offset="5%"
                stopColor="#2563EB"
                stopOpacity={0.45}
              />

              <stop
                offset="95%"
                stopColor="#2563EB"
                stopOpacity={0}
              />

            </linearGradient>

          </defs>

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

          <Area
            type="monotone"
            dataKey="energy"
            stroke="#2563EB"
            strokeWidth={4}
            fill="url(#energyGradient)"
            animationDuration={1200}
          />

        </AreaChart>

      </ResponsiveContainer>

    </Paper>

  );

}

export default EnergyChart;