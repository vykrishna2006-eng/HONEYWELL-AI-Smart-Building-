import {

    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip

} from "recharts";

export default function EnergyChart({ data }) {

    return (

        <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-bold mb-4">

                Energy Consumption

            </h2>

            <LineChart
                width={500}
                height={300}
                data={data}
            >

                <CartesianGrid strokeDasharray="3 3"/>

                <XAxis dataKey="iteration"/>

                <YAxis/>

                <Tooltip/>

                <Line
                    dataKey="energy"
                    type="monotone"
                />

            </LineChart>

        </div>

    );

}