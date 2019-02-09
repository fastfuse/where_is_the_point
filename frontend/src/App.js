import React, {Component} from 'react';
import axios from 'axios';
import {Form, Button, Container, Row, Col} from 'react-bootstrap';

import './App.css';


class App extends Component {
    state = {
        create_lon: "",
        create_lat: "",
        create_name: "",
    };

    handleInput = prop => e => {
        this.setState({
            [prop]: e.target.value
        });
    };

    getLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this.handleScan);
        } else {
            console.log("Geolocation is not supported by this browser.");
        }
    };

    componentDidMount = () => {
        this.timer = setInterval(this.getLocation, 10000);
    };

    componentWillUnmount = () => {
        clearInterval(this.timer);
    };

    handleScan = position => {
        const data = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        };
        axios.post(`/api/scan`, data);
    };

    handleCreate = e => {
        const {create_lon, create_lat, create_name} = this.state;
        const data = {
            latitude: create_lat,
            longitude: create_lon,
            data: create_name
        };
        axios.post(`/api/create_point`, data);
    };

    render() {
        const {create_lon, create_lat, create_name} = this.state;

        return (
            <div className="App">
                <Container>
                    <Row className="justify-content-md-center">
                        <Col md="6">
                            <Form>
                                <Form.Group controlId="formBasicEmail">
                                    <Form.Label>Longitude</Form.Label>
                                    <Form.Control type="text" placeholder="Longitude"
                                                  onChange={this.handleInput('create_lon')}
                                                  value={create_lon}/>
                                </Form.Group>

                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label>Latitude</Form.Label>
                                    <Form.Control type="text" placeholder="Latitude"
                                                  onChange={this.handleInput('create_lat')}
                                                  value={create_lat}/>
                                </Form.Group>
                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control type="text" placeholder="Name"
                                                  onChange={this.handleInput('create_name')}
                                                  value={create_name}/>
                                </Form.Group>
                                <Button variant="primary" type="button" onClick={this.handleCreate}>
                                    Create
                                </Button>
                            </Form>
                        </Col>
                    </Row>
                </Container>

            </div>
        );
    }
}

export default App;
