import { LeftPanel } from "./components/LeftPanel.jsx/LeftPanel";
import { Catalog } from "./components/Catalog/Catalog";
import { CustomNavbar } from "./components/CustomNavbar/CustomNavbar";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
	return (
		<div className="app__main">
			<CustomNavbar />
			<LeftPanel />
			<Catalog />
		</div>
	);
}

export default App;
