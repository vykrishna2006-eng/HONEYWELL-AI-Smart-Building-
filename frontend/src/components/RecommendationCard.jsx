import { useEffect, useState } from "react";

import {
  Paper,
  Typography,
  Box,
  Stack,
  Divider,
  Avatar,
  CircularProgress,
} from "@mui/material";

import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";
import SavingsIcon from "@mui/icons-material/Savings";
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
            {recommendation.reason}
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
                {recommendation.expected_savings}%
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

            <Box>

              <Typography
                color="text.secondary"
              >
                Recommended Setpoint
              </Typography>

              <Typography
                variant="h4"
                fontWeight={700}
                color="#EA580C"
              >
                {recommendation.recommended_setpoint}°C
              </Typography>

            </Box>

          </Stack>

        </Paper>

      </Stack>

    </Paper>

  );

}

export default RecommendationCard;