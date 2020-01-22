import { Component, OnInit, Input } from '@angular/core';

@Component({
    selector: 'app-pump',
    templateUrl: './pump.component.html',
    styleUrls: ['./pump.component.scss']
})
export class PumpComponent implements OnInit {

    @Input() pump: any;

    constructor() { }

    ngOnInit() {
    }

}
