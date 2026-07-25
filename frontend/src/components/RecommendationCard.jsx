import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Chip,
  Box,
  Stack,
  Divider,
  Avatar,
  CircularProgress,
} from "@mui/material";

import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";
import SavingsIcon from "@mui/icons-material/Savings";
import ThermostatIcon from "@mui/icons-material/Thermostat";
import PriorityHighIcon from "@mui/icons-material/PriorityHigh";
import SmartToyIcon from "@mui/icons-material/SmartToy";

import { getLatestRecommendation } from "../services/analyticsService";

function RecommendationCard() {

  const [recommendation, setRecommendation] = useState(null);

  useEffect(() => {
    loadRecommendation();
  }, []);

  const loadRecommendation = async () => {

    try {

      const data = await getLatestRecommendation();

      setRecommendation(data);

    } catch (err) {

      console.log(err);

    }

  };

  if (!recommendation) {

    return (

      <Paper
        sx={{
          p: 5,
          borderRadius: 5,
          textAlign: "center",
        }}
      >

        <CircularProgress />

        <Typography mt={2}>
          Loading AI Recommendation...
        </Typography>

      </Paper>

    );

  }

  const priorityColor = {

    High: "error",
    Medium: "warning",
    Low: "success",

  }[recommendation.priority] || "primary";

  return (

    <Paper
      elevation={0}
      sx={{
        borderRadius: 5,
        p: 4,
        border: "1px solid #E2E8F0",
        background:
          "linear-gradient(145deg,#ffffff,#f8fafc)",
      }}
    >

      {/* Header */}

      <Stack
        direction="row"
        justifyContent="space-between"
        alignItems="center"
      >

        <Stack
          direction="row"
          spacing={2}
          alignItems="center"
        >

          <Avatar
            sx={{
              bgcolor: "#2563EB",
              width: 56,
              height: 56,
            }}
          >

            <SmartToyIcon />

          </Avatar>

          <Box>

            <Typography
              variant="h5"
              fontWeight={700}
            >
              AI Recommendation
            </Typography>

            <Typography
              color="text.secondary"
            >
              Intelligent Building Optimisation
            </Typography>

          </Box>

        </Stack>

        <Chip

          icon={<PriorityHighIcon />}

          label={recommendation.priority}

          color={priorityColor}

          sx={{
            fontWeight: 700,
          }}

        />

      </Stack>

      <Divider sx={{ my: 3 }} />

      {/* Recommendation */}

      <Paper
        elevation={0}
        sx={{
          bgcolor: "#EFF6FF",
          borderLeft: "5px solid #2563EB",
          p: 3,
          borderRadius: 3,
        }}
      >

        <Stack
          direction="row"
          spacing={2}
          alignItems="flex-start"
        >

          <TipsAndUpdatesIcon
            sx={{
              color: "#2563EB",
              mt: .5,
            }}
          />

          <Typography
            sx={{
              lineHeight: 1.8,
            }}
          >
            {recommendation.recommendation}
          </Typography>

        </Stack>

      </Paper>

      {/* Metrics */}

      <Stack
        direction={{
          xs: "column",
          md: "row",
        }}
        spacing={3}
        mt={4}
      >

        <Paper
          elevation={0}
          sx={{
            flex: 1,
            p: 3,
            bgcolor: "#F0FDF4",
            borderRadius: 4,
          }}
        >

          <Stack
            direction="row"
            spacing={2}
            alignItems="center"
          >

            <SavingsIcon
              sx={{
                color: "#22C55E",
                fontSize: 40,
              }}
            />

            <Box>

              <Typography
                color="text.secondary"
              >
                Expected Savings
              </Typography>

              <Typography
                variant="h4"
                fontWeight={700}
                color="#16A34A"
              >
                {recommendation.energy_saving}%
              </Typography>

            </Box>

          </Stack>

        </Paper>

        <Paper
          elevation={0}
          sx={{
            flex: 1,
            p: 3,
            bgcolor: "#FFF7ED",
            borderRadius: 4,
          }}
        >

          <Stack
            direction="row"
            spacing={2}
            alignItems="center"
          >

            <ThermostatIcon
              sx={{
                color: "#F59E0B",
                fontSize: 40,
              }}
            />

            <Box>

              <Typography
                color="text.secondary"
              >
                Comfort Score
              </Typography>

              <Typography
                variant="h4"
                fontWeight={700}
                color="#EA580C"
              >
                {recommendation.comfort_score}%
              </Typography>

            </Box>

          </Stack>

        </Paper>

      </Stack>

    </Paper>

  );

}

export default RecommendationCard;