import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import {
    MatTabsModule,
    MatExpansionModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatIconModule
} from '@angular/material';

import { NgxMaterialTimepickerModule } from 'ngx-material-timepicker';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HomeComponent } from './components/home/home.component';
import { ThermostatsComponent } from './components/thermostats/thermostats.component';
import { PumpsComponent } from './components/pumps/pumps.component';
import { PumpComponent } from './components/pump/pump.component';
import { ThermostatComponent } from './components/thermostat/thermostat.component';
import { SafePipe } from './pipes/safe.pipe';

@NgModule({
    declarations: [
        AppComponent,
        SafePipe,
        HomeComponent,
        ThermostatsComponent,
        PumpsComponent,
        PumpComponent,
        ThermostatComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        BrowserAnimationsModule,
        FormsModule,
        NgxMaterialTimepickerModule,
        ReactiveFormsModule,
        MatTabsModule,
        MatExpansionModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatSelectModule,
        MatIconModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
