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
    }

    ngOnDestroy() {
        clearInterval(this.updateInterval);
    }

    save() {
        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json',
                'Authorization': 'my-auth-token'
            })
        };

        if(this.pump.id != null) {
        this.http.post<any>(`${environment.api_address}/pump/${this.pump.id}`, { name: this.name.value, pin: this.pin.value }, httpOptions)
            .subscribe(data => {
                if (data && data.status) {
                    this.pump.name = this.name.value;
                    this.pump.pin = this.pin.value;
                    this.updated.emit(this.pump);
                }
            });
        }
        else {
            this.http.post<any>(`${environment.api_address}/pumps/add`, { name: this.name.value, pin: this.pin.value }, httpOptions)
                .subscribe(data => {
                    this.pump.id = data.id;
                    this.pump.name = data.name;
                    this.pump.pin = data.pin;
                    this.pump.isOn = data.isOn;
                    this.updated.emit(this.pump);
                });
        } 
    }

    delete() {

        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json',
                'Authorization': 'my-auth-token'
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
