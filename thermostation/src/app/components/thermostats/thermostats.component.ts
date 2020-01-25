import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
    selector: 'app-thermostats',
    templateUrl: './thermostats.component.html',
    styleUrls: ['./thermostats.component.scss']
})
export class ThermostatsComponent implements OnInit {

    thermostats: any[];

    constructor(private http: HttpClient) { }

    ngOnInit() {
        this.http.get(`${environment.api_address}/thermostats`)
            .subscribe(
                (data: any[]) => {
                    this.thermostats = data;
                });
    }

    thermostatUpdated(thermostat: any) {
        this.thermostats[this.thermostats.indexOf(thermostat)] = thermostat;
    }

    thermostatDeleted(thermostat: any) {
        this.thermostats.splice(this.thermostats.indexOf(thermostat), 1);
    }

    addThermostat() {
        this.thermostats.push({
            id: null,
            name: "Nuovo termostato",
            pin: null,
            isOn: false,
            controlledPumps: []
        });
    }
}
