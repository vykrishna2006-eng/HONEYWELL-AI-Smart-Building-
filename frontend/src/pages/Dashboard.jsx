import { useEffect, useState } from "react";
import api from "../api/api";

import DashboardCards from "../components/DashboardCards";
import RecommendationPanel from "../components/RecommendationPanel";

export default function Dashboard() {

    const [summary, setSummary] = useState({});
    const [prediction, setPrediction] = useState({});
    const [recommendation, setRecommendation] = useState({});
    const [energy, setEnergy] = useState({});
    const [comfort, setComfort] = useState({});

    useEffect(() => {
        loadDashboard();
    }, []);

    async function loadDashboard() {

        try {

            const [
                summaryRes,
                predictionRes,
                recommendationRes,
                energyRes,
                comfortRes
            ] = await Promise.all([

                api.get("/analytics/dashboard"),

                api.get("/analytics/latest-prediction"),

                api.get("/analytics/latest-recommendation"),

                api.get("/analytics/energy"),

                api.get("/analytics/comfort")

            ]);

            setSummary(summaryRes.data);

            setPrediction(predictionRes.data);

            setRecommendation(recommendationRes.data);

            setEnergy(energyRes.data);

            setComfort(comfortRes.data);

        }

        catch (err) {

            console.error(err);

        }

    }

    return (

        <div className="p-8 bg-gray-100 min-h-screen">

            <h1 className="text-4xl font-bold mb-8">

                AI Smart Building Dashboard

            </h1>

            <DashboardCards
                summary={summary}
                prediction={prediction}
                energy={energy}
                comfort={comfort}
            />

            <RecommendationPanel
                recommendation={recommendation}
            />

        </div>

    );

}