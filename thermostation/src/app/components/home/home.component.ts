import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
    links: any[];

    constructor() {
        this.links = [
            { path: '/thermostats', title: 'Termostati'},
            { path: '/pumps', title: 'Pompe' }
        ];
    }

    ngOnInit() {
    }

}
