import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { ThermostatsComponent } from './components/thermostats/thermostats.component';
import { PumpsComponent } from './components/pumps/pumps.component';

const routes: Routes = [
    {
        path: "",
        component: HomeComponent,
        children: [
            { path: "thermostats", component: ThermostatsComponent },
            { path: "pumps", component: PumpsComponent }
        ]
    },
    { path: "**", component: HomeComponent }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
