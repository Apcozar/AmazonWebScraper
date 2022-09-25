import Navbar from "react-bootstrap/Navbar";
import "./customNavbar.css";

export const CustomNavbar = () => {
	return (
		<Navbar className="custom-navbar" expand="lg" variant="dark" fixed="top">
			<Navbar.Brand className="customNavbar__title">
				Amazon Search Engine
			</Navbar.Brand>
		</Navbar>
	);
};
