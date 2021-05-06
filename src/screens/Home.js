import React, { useState } from "react";
import MonacoEditor from "@monaco-editor/react";
import { Play, Loader } from "react-feather";

import options from "../config/editor.json";

export default function Home() {
	const [output, setOutput] = useState("");
	const [code, setCode] = useState(
		`#include <iostream>\n\nint main(){\n	std::cout << "Hello World\\n";\n}`
	);
	const [loading, setLoading] = useState(false);
	const submit = async () => {
		setLoading(true);
		try {
			const res = await fetch(process.env.BACKEND, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					code,
				}),
			});
			const result = await res.text();
			setOutput(result);
		} catch (err) {
			console.error(err);
			setOutput("");
		} finally {
			setLoading(false);
		}
	};
	return (
		<div
			className="flex h-full items-center"
			style={{
				background: "#1e1e1e",
			}}
		>
			<div id="editor-container" className="w-2/3 p-2">
				<MonacoEditor
					height="90vh"
					theme="vs-dark"
					language="cpp"
					options={options}
					onChange={(value) => setCode(value)}
					value={code}
				/>
			</div>
			<div className="w-1/3 flex flex-col items-center">
				<button
					id="run-btn"
					className={`
						flex pl-4 pr-3 py-1
						mb-4 rounded-md text-lg
						items-center shadow-lg
						${loading ? "loading" : ""}
					`}
					onClick={submit}
					disabled={loading}
				>
					{!loading ? (
						<>
							Run <Play size={18} className="ml-1" />
						</>
					) : (
						<>
							Executing <Loader size={18} className="ml-2" />
						</>
					)}
				</button>
				<MonacoEditor height="80vh" theme="vs-dark" value={output} />
			</div>
		</div>
	);
}
