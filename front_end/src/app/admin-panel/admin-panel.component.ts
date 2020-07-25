import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { APIService } from '../api.service';
import { Observable, interval, Subscription } from 'rxjs';
import { AuthService } from '../auth.service';

@Component({
  selector: 'admin',
  templateUrl: './admin-panel.component.html',
  styleUrls: ['./admin-panel.component.css']
})
export class AdminPanelComponent implements OnInit {
  this_location = 0;	
  shop_info = null;
  shop_subscription: Subscription;
  currentShopHours = null;
  currentWeekday = 1;
  message = '';


  constructor(public api: APIService, private route: ActivatedRoute, public auth: AuthService) { 
    this.route.params.subscribe( params => {
    	this.this_location = params.id;
        if (this.this_location != 0) {
        	this.api.getLocation(this.this_location);
  			this.shop_subscription = this.api.getCurrentLocation().subscribe(shop => {
      			this.shop_info = shop;
      			this.updateDay();
    		});      
        }
    });
  }

  updateDay() {
  	for (var this_day of this.shop_info['opening_hours']) {
  		if (this_day['weekday'] == this.currentWeekday) {
  			this.currentShopHours = this_day;
  		}
  	}
  }

  saveOpeningHours() {
    console.log('...saving opening hours.')
    this.api.saveSlotOpeningHoursToBackend(this.currentShopHours).then( results => {
      this.api.getLocation(this.this_location);
      this.message = 'Updated';
      setTimeout(()=>{    
        this.message = '';
      }, 3000);
    })
  }

  ngOnInit() {
  }

}
