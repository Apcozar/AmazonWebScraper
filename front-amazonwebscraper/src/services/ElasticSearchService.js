// Reference example, please remove it
export async function getExampleElements(params) {
	const url = "http://example.com/movies.json";
	return fetch(`${url}?exampleParam=${params.paramExample}`, {
		method: "GET", // POST, PUT, DELETE...
		mode: "cors", // no-cors, *cors, same-origin
		body: JSON.stringify(params),
	})
		.then((res) => res.json())
		.then((res) => res.data);
}
