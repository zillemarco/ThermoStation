import { Component, OnInit, Input, Output, EventEmitter, OnDestroy } from '@angular/core';
import { FormControl } from '@angular/forms';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
    selector: 'app-thermostat',
    templateUrl: './thermostat.component.html',
    styleUrls: ['./thermostat.component.scss']
})
export class ThermostatComponent implements OnInit, OnDestroy {

    @Input() thermostat: any;
    @Output() updated = new EventEmitter();
    @Output() deleted = new EventEmitter();

    pumps: any[] = [];
    pinValues: number[] = [];
    type: FormControl = null;
    name: FormControl = null;
    pin: FormControl = null;
    controlledPumps: FormControl = null;
    targetTemperature: FormControl = null;

    onStatusUrl: string = "";
    temperatureStatusUrl: string = "";

    private updateInterval: any = null;

    constructor(private http: HttpClient) {
        this.pinValues = Array(40).fill(0).map((_, i) => i);

        this.http.get(`${environment.api_address}/pumps`)
            .subscribe(
                (data: any[]) => {
                    this.pumps = data;
                });
    }

    ngOnInit() {
        this.updateInterval = setInterval(() => {
            this.updateStatus();
        }, environment.update_interval);

        console.log(this.thermostat.type);

        this.type = new FormControl(this.thermostat.type);
        this.name = new FormControl(this.thermostat.name);
        this.pin = new FormControl(this.thermostat.pin);
        this.targetTemperature = new FormControl(this.thermostat.targetTemperature);
        this.controlledPumps = new FormControl(this.thermostat.controlledPumps);

        this.onStatusUrl = `${environment.stats_address}/d-solo/nXxpC-Wgk/thermo-station?orgId=1&refresh=10s&from=1580029260847&to=1580050860847&var-deviceId=${this.thermostat.id}&panelId=2`;
        this.temperatureStatusUrl = `${environment.stats_address}/d-solo/nXxpC-Wgk/thermo-station?orgId=1&refresh=10s&from=1580029108038&to=1580050708038&var-deviceId=${this.thermostat.id}&panelId=4`;
    }

    ngOnDestroy() {
        clearInterval(this.updateInterval);
    }

    save() {
        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json'
            })
        };

        console.log(this.controlledPumps.value);

        if (this.thermostat.id != null) {
            this.http.post<any>(`${environment.api_address}/thermostat/${this.thermostat.id}`, {
                type: parseInt(this.type.value),
                name: this.name.value,
                pin: this.pin.value,
                targetTemperature: parseFloat(this.targetTemperature.value),
                controlledPumps: this.controlledPumps.value
            }, httpOptions)
                .subscribe(data => {
                    if (data && data.status) {
                        this.thermostat.name = this.name.value;
                        this.thermostat.pin = this.pin.value;
                        this.thermostat.targetTemperature = parseFloat(this.targetTemperature.value);
                        this.thermostat.controlledPumps = this.controlledPumps.value;
                        this.updated.emit(this.thermostat);
                    }
                });
        }
        else {
            this.http.post<any>(`${environment.api_address}/thermostats/add`, {
                type: parseInt(this.type.value),
                name: this.name.value,
                pin: this.pin.value,
                targetTemperature: parseFloat(this.targetTemperature.value),
                controlledPumps: this.controlledPumps.value
            }, httpOptions)
                .subscribe(data => {
                    this.thermostat.id = data.id;
                    this.thermostat.name = data.name;
                    this.thermostat.pin = data.pin;
                    this.thermostat.targetTemperature = data.targetTemperature;
                    this.thermostat.currentTemperature = data.currentTemperature;
                    this.thermostat.controlledPumps = data.controlledPumps;
                    this.thermostat.isOn = data.isOn;
                    this.onStatusUrl = `${environment.stats_address}/d-solo/nXxpC-Wgk/thermo-station?orgId=1&refresh=10s&from=1580029260847&to=1580050860847&var-deviceId=${this.thermostat.id}&panelId=2`;
                    this.temperatureStatusUrl = `${environment.stats_address}/d-solo/nXxpC-Wgk/thermo-station?orgId=1&refresh=10s&from=1580029108038&to=1580050708038&var-deviceId=${this.thermostat.id}&panelId=4`;
                    this.updated.emit(this.thermostat);
                });
        }
    }

    delete() {

        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json'
            })
        };
        this.http.delete(`${environment.api_address}/thermostat/${this.thermostat.id}`, httpOptions)
            .subscribe(() => {
                this.deleted.emit(this.thermostat);
            });
    }

    private updateStatus() {
        if (this.thermostat.id != null) {
            this.http.get(`${environment.api_address}/thermostat/${this.thermostat.id}/status`)
                .subscribe(
                    (data: any) => {
                        if (data) {
                            console.log(data);
                            this.thermostat.isOn = data.isOn;
                            this.thermostat.currentTemperature = data.currentTemperature;
                        }
                    });
        }
    }

}
