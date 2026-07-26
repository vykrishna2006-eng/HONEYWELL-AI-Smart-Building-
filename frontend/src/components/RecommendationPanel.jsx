export default function RecommendationPanel({

    recommendation

}) {

    return (

        <div className="bg-white mt-8 p-6 rounded-xl shadow">

            <h2 className="text-2xl font-bold mb-4">

                AI Recommendation

            </h2>

            <p>

                <b>Cooling Setpoint :</b>

                {" "}

                {recommendation.cooling_setpoint_c} °C

            </p>

            <p>

                <b>Heating Setpoint :</b>

                {" "}

                {recommendation.heating_setpoint_c} °C

            </p>

            <p>

                <b>Lighting :</b>

                {" "}

                {recommendation.lighting_action}

            </p>

            <p>

                <b>Ventilation :</b>

                {" "}

                {recommendation.ventilation_action}

            </p>

            <p>

                <b>Equipment :</b>

                {" "}

                {recommendation.equipment_schedule}

            </p>

            <p className="mt-4">

                <b>Reason</b>

            </p>

            <p>

                {recommendation.reason}

            </p>

        </div>

    );

}