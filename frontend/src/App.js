import React, {Component} from 'react';
import axios from 'axios';
import {Form, Button, Container, Row, Col} from 'react-bootstrap';

import './App.css';


class App extends Component {
    state = {
        lon: "",
        lat: "",
        name: "",
        create_lon: "",
        create_lat: "",
        create_name: "",
    };

    handleInput = prop => e => {
        this.setState({
            [prop]: e.target.value
        });
    };

    handleSubmit = e => {
        const {lon, lat, name} = this.state;
        const data = {
            latitude: lat,
            longitude: lon,
            name: name
        };
        axios.post(`/api/ping`, data);
    };

    handleCreate = e => {
        const {create_lon, create_lat, create_name} = this.state;
        const data = {
            latitude: create_lat,
            longitude: create_lon,
            name: create_name
        };
        axios.post(`/api/create_point`, data);
    };

    render() {
        const {lon, lat, name, create_lon, create_lat, create_name} = this.state;

        return (
            <div className="App">
                <Container>
                    <Row className="justify-content-md-center">
                        <Col md="6">
                            <Form>
                                <Form.Group controlId="formBasicEmail">
                                    <Form.Label>Longitude</Form.Label>
                                    <Form.Control type="text" placeholder="Longitude" onChange={this.handleInput('lon')}
                                                  value={lon}/>
                                </Form.Group>

                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label>Latitude</Form.Label>
                                    <Form.Control type="text" placeholder="Latitude" onChange={this.handleInput('lat')}
                                                  value={lat}/>
                                </Form.Group>
                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control type="text" placeholder="Name" onChange={this.handleInput('name')}
                                                  value={name}/>
                                </Form.Group>
                                <Button variant="primary" type="button" onClick={this.handleSubmit}>
                                    Ping
                                </Button>
                            </Form>
                        </Col>
                    </Row>
                    <Row className="justify-content-md-center">
                        <Col md="6">
                            <Form>
                                <Form.Group controlId="formBasicEmail">
                                    <Form.Label>Longitude</Form.Label>
                                    <Form.Control type="text" placeholder="Longitude" onChange={this.handleInput('create_lon')}
                                                  value={create_lon}/>
                                </Form.Group>

                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label>Latitude</Form.Label>
                                    <Form.Control type="text" placeholder="Latitude" onChange={this.handleInput('create_lat')}
                                                  value={create_lat}/>
                                </Form.Group>
                                <Form.Group controlId="formBasicPassword">
                                    <Form.Label>Name</Form.Label>
                                    <Form.Control type="text" placeholder="Name" onChange={this.handleInput('create_name')}
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
