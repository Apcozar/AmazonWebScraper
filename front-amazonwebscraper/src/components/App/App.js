import { LeftPanel } from "../LeftPanel/LeftPanel";
import { CustomNavbar } from "../CustomNavbar/CustomNavbar";
import { Catalog } from "../Catalog/Catalog";
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
