import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-pumps',
    templateUrl: './pumps.component.html',
    styleUrls: ['./pumps.component.scss']
})
export class PumpsComponent implements OnInit {

    pumps: any[];

    constructor(private http: HttpClient) { }

    ngOnInit() {
        this.http.get('http://192.168.1.13:5000/pumps')
            .subscribe(
                (data: any[]) => {
                    console.log(data);
                    this.pumps = data;
                });
    }

}
