import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Button from "react-bootstrap/Button";
import "./leftPanel.css";
import React, { useState } from "react";

export const LeftPanel = () => {
	const [searchKeywords, setSearchKeywords] = useState("");
	return (
		<div className="left-panel__main">
			<div className="left-panel__wrapper">
				<div className="left-panel__inputsWrapper">
					<InputGroup className="mb-3" size="sm">
						<Form.Control
							as="input"
							size="sm"
							placeholder="Search"
							onChange={(e) => setSearchKeywords(e.target.value)}
						/>
						<Button
							variant="outline-secondary"
							onClick={() => console.log(searchKeywords)}
						>
							Button
						</Button>
					</InputGroup>
				</div>
				<div className="verticalDivider" />
			</div>
		</div>
	);
};
