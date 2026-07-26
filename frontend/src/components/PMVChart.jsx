import {

    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid

} from "recharts";

export default function PMVChart({ data }) {

    return (

        <div className="bg-white p-6 rounded-xl shadow">

            <h2 className="text-xl font-bold mb-4">

                PMV

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
                    dataKey="pmv"
                    type="monotone"
                />

            </LineChart>

        </div>

    );

}