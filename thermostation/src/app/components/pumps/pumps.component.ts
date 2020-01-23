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

}
