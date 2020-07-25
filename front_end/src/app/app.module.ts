import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { NgbModule, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { Routes, RouterModule } from '@angular/router';
import { HttpClientModule } from  '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AuthGuard } from './auth.guard';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { TvViewComponent } from './tv-view/tv-view.component';
import { APIService } from './api.service';
import { CustomerViewComponent } from './customer-view/customer-view.component';
import { ShopViewComponent } from './shop-view/shop-view.component';
import { NavBarComponent } from './nav-bar/nav-bar.component'


const appRoutes: Routes = [
  { path: '', component: CustomerViewComponent },
  { path: 'admin/:id', component: AdminPanelComponent, canActivate: [AuthGuard]},
  { path: 'tv-view/:id', component: TvViewComponent, canActivate: [AuthGuard]},
  { path: 'shop-view/:id', component: ShopViewComponent, canActivate: [AuthGuard]},
  { path: 'book', component: CustomerViewComponent},
  { path: 'book/:id', component: CustomerViewComponent},
  { path: 'nav', component: NavBarComponent, canActivate: [AuthGuard]},

];


@NgModule({
  declarations: [
    AppComponent,
    AdminPanelComponent,
    TvViewComponent,
    CustomerViewComponent,
    ShopViewComponent,
    NavBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule,
    FormsModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [ APIService, NgbActiveModal ],
  bootstrap: [AppComponent]
})
export class AppModule { }
