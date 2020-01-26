import { Component, OnInit, Input, Output, EventEmitter, OnDestroy } from '@angular/core';
import { FormControl } from '@angular/forms';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
    selector: 'app-pump',
    templateUrl: './pump.component.html',
    styleUrls: ['./pump.component.scss']
})
export class PumpComponent implements OnInit, OnDestroy {

    @Input() pump: any;
    @Output() updated = new EventEmitter();
    @Output() deleted = new EventEmitter();

    pinValues: number[] = [];
    name: FormControl = null;
    pin: FormControl = null;
    startTime: FormControl = null;
    stopTime: FormControl = null;
    statsUrl: string = "";

    private updateInterval: any = null;

    constructor(private http: HttpClient) {
        this.pinValues = Array(40).fill(0).map((_, i) => i);
    }

    ngOnInit() {
        this.updateInterval = setInterval(() => {
            this.updateStatus();
        }, environment.update_interval);

        this.name = new FormControl(this.pump.name);
        this.pin = new FormControl(this.pump.pin);
        this.startTime = new FormControl(`${this.pump.startHour}:${this.pump.startMinute}`);
        this.stopTime = new FormControl(`${this.pump.stopHour}:${this.pump.stopMinute}`);

        this.statsUrl = `${environment.stats_address}/d-solo/nXxpC-Wgk/thermo-station?orgId=1&refresh=10s&from=1580029260847&to=1580050860847&var-deviceId=${this.pump.id}&panelId=2`;
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

        const startHour = parseInt(this.startTime.value.split(":")[0]);
        const startMinute = parseInt(this.startTime.value.split(":")[1]);
        const stopHour = parseInt(this.stopTime.value.split(":")[0]);
        const stopMinute = parseInt(this.stopTime.value.split(":")[1]);

        if (this.pump.id != null) {
            this.http.post<any>(`${environment.api_address}/pump/${this.pump.id}`, {
                name: this.name.value,
                pin: this.pin.value,
                startHour: startHour,
                startMinute: startMinute,
                stopHour: stopHour,
                stopMinute: stopMinute
            }, httpOptions)
                .subscribe(data => {
                    if (data && data.status) {
                        this.pump.name = this.name.value;
                        this.pump.pin = this.pin.value;
                        this.pump.startHour = startHour;
                        this.pump.startMinute = startMinute;
                        this.pump.stopHour = stopHour;
                        this.pump.stopMinute = stopMinute;
                        this.updated.emit(this.pump);
                    }
                });
        }
        else {
            this.http.post<any>(`${environment.api_address}/pumps/add`, {
                name: this.name.value,
                pin: this.pin.value,
                startHour: startHour,
                startMinute: startMinute,
                stopHour: stopHour,
                stopMinute: stopMinute
            }, httpOptions)
                .subscribe(data => {
                    this.pump.id = data.id;
                    this.pump.name = data.name;
                    this.pump.pin = data.pin;
                    this.pump.startHour = data.startHour;
                    this.pump.startMinute = data.startMinute;
                    this.pump.stopHour = data.stopHour;
                    this.pump.stopMinute = data.stopMinute;
                    this.pump.isOn = data.isOn;
                    this.statsUrl = `${environment.stats_address}/d-solo/nXxpC-Wgk/thermo-station?orgId=1&refresh=10s&from=1580029260847&to=1580050860847&var-deviceId=${this.pump.id}&panelId=2`;
                    this.updated.emit(this.pump);
                });
        }
    }

    delete() {

        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json'
            })
        };
        this.http.delete(`${environment.api_address}/pump/${this.pump.id}`, httpOptions)
            .subscribe(() => {
                this.deleted.emit(this.pump);
            });
    }

    private updateStatus() {
        if (this.pump.id != null) {
            this.http.get(`${environment.api_address}/pump/${this.pump.id}/status`)
                .subscribe(
                    (data: any) => {
                        if (data) {
                            this.pump.isOn = data.status;
                        }
                    });
        }
    }

}
