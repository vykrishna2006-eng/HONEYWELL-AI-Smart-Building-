export default function DashboardCards({

    summary,
    prediction,
    energy,
    comfort

}) {

    const cards = [

        {
            title: "Predictions",
            value: summary.total_predictions
        },

        {
            title: "Energy Prediction",
            value: prediction.energy_prediction
        },

        {
            title: "Comfort Prediction",
            value: prediction.comfort_prediction
        },

        {
            title: "Confidence",
            value: prediction.confidence
        },

        {
            title: "Average Energy",
            value: summary.average_energy_prediction
        },

        {
            title: "Average Comfort",
            value: summary.average_comfort_score
        },

        {
            title: "Expected Savings",
            value: summary.average_expected_savings
        },

        {
            title: "Max Energy",
            value: energy.maximum
        },

        {
            title: "Average Energy",
            value: energy.average
        },

        {
            title: "Average Comfort",
            value: comfort.average
        }

    ];

    return (

        <div className="grid grid-cols-5 gap-6">

            {cards.map((card, index) => (

                <div
                    key={index}
                    className="bg-white rounded-lg shadow p-5"
                >

                    <h2 className="text-gray-500">

                        {card.title}

                    </h2>

                    <p className="text-3xl font-bold">

                        {card.value ?? "--"}

                    </p>

                </div>

            ))}

        </div>

    );

}