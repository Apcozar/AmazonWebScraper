import Card from "react-bootstrap/Card";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import "./catalog.css";
import { mockData } from "./catalogMockData";

export const Catalog = () => {
	return (
		<div className="catalog__main">
			<Row xs={1} md={2} lg={3} className="g-4">
				{mockData.map(({ name, description, price, rting }, idx) => (
					<Col key={idx}>
						<Card>
							{/* <Card.Img variant="top" src="holder.js/100px160" /> */}
							<Card.Body>
								<Card.Title>{name}</Card.Title>
								<Card.Text>{description}</Card.Text>
							</Card.Body>
						</Card>
					</Col>
				))}
			</Row>
		</div>
	);
};
