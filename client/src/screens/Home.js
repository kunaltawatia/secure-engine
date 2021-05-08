import React, { useState } from "react";
import MonacoEditor from "@monaco-editor/react";
import { Play, Loader } from "react-feather";

import options from "../config/editor.json";
import server from "../config/server.json";

export default function Home() {
	const [output, setOutput] = useState("");
	const [input, setInput] = useState("");
	const [code, setCode] = useState(
		`#include <iostream>\n\nint main(){\n	std::cout << "Hello World\\n";\n}`
	);
	const [loading, setLoading] = useState(false);
	const submit = async () => {
		setLoading(true);
		setOutput("");
		try {
			const res = await fetch(server.backend, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					code,
					input,
				}),
			});
			const result = await res.text();
			setOutput(result);
		} catch (err) {
			setOutput(err.message ?? "Server Error");
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
				<MonacoEditor
					height="40vh"
					theme="vs-dark"
					value={input}
					onChange={(value) => setInput(value)}
				/>
				<button
					id="run-btn"
					className={`
						flex pl-4 pr-3 py-1
						m-4 rounded-md text-lg
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
				<MonacoEditor height="40vh" theme="vs-dark" value={output} />
			</div>
		</div>
	);
}
