import { Component, OnInit, Input } from '@angular/core';
import { FormControl } from '@angular/forms';

@Component({
    selector: 'app-pump',
    templateUrl: './pump.component.html',
    styleUrls: ['./pump.component.scss']
})
export class PumpComponent implements OnInit {

    @Input() pump: any;

    pinValues: number[] = [];
    name: FormControl = null;
    pin: FormControl = null;

    constructor() {
        this.pinValues = Array(40).fill(0).map((_, i) => i);
    }

    ngOnInit() {
        this.name = new FormControl(this.pump.name);
        this.pin = new FormControl(this.pump.pin);
    }

}
