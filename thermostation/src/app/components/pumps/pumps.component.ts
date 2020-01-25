import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Component({
    selector: 'app-pumps',
    templateUrl: './pumps.component.html',
    styleUrls: ['./pumps.component.scss']
})
export class PumpsComponent implements OnInit {

    pumps: any[];

    constructor(private http: HttpClient) { }

    ngOnInit() {
        this.http.get(`${environment.api_address}/pumps`)
            .subscribe(
                (data: any[]) => {
                    this.pumps = data;
                });
    }

    pumpUpdated(pump: any) {
        this.pumps[this.pumps.indexOf(pump)] = pump;
    }

    pumpDeleted(pump: any) {
        this.pumps.splice(this.pumps.indexOf(pump), 1);
    }

    addPump() {
        this.pumps.push({
            id: null,
            name: "Nuova pompa",
            pin: null,
            startHour: 12,
            startMinute: 0,
            stopHour: 12,
            stopMinute: 0,
            isOn: false
        });
    }
}
