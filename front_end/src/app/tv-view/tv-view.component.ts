import { Component, OnInit, OnDestroy } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import { Observable, interval, Subscription } from 'rxjs';
import { APIService } from '../api.service';

@Component({
  selector: 'tv-view',
  templateUrl: './tv-view.component.html',
  styleUrls: ['./tv-view.component.css']
})
export class TvViewComponent implements OnInit, OnDestroy {

  private updateSlots: Subscription;
  private currentSlots;
  slots_list_subscription: Subscription;
  locations_subscription: Subscription;
  noflys_subscription: Subscription;
  slots_list = [];
  locations_list = [];
  noflys_list = [];
  this_location = 0;
  today: number = Date.now();

  constructor(public api: APIService, private route: ActivatedRoute) { 
    this.route.params.subscribe( params => {
        console.log(params); 
        this.this_location = params.id;
        this.api.getLocations();        
        this.api.getSlots(this.this_location)
        this.api.getNoFlys(this.this_location)
    });
  }

  ngOnInit() {
    this.slots_list_subscription = this.api.getSlotsList().subscribe(slots_list => {
      this.slots_list = slots_list;
    });    
    this.noflys_subscription = this.api.getNoFlysList().subscribe(noflys_list => {
      this.noflys_list = noflys_list;
    });    
    this.locations_subscription = this.api.getLocationsList().subscribe(locations_list => {
      this.locations_list = locations_list;
      console.log(this.locations_list)
    });  
    this.updateSlots = interval(15000).subscribe( (val) => { this.updateSlotsInfo() })
  }

  ngOnDestroy() {
    if (this.updateSlots) {
      this.updateSlots.unsubscribe();
      console.log('unsubscribed');
    }
  }

  correctTime(slot) {
    let newDate = new Date().toDateString();
    let newerDate = newDate + " " + slot.slot + " GMT-0600 (Mountain Daylight Time)";
    return newerDate;
  }

  locationName(location_id) {
    for (var this_loc of this.locations_list) {
      if (this_loc.id == location_id) {
        return this_loc.name;
      }
    }
  }

  updateSlotsInfo() {
    this.today = Date.now();
    this.api.getSlots(this.this_location).then(value => {
      console.log(this.slots_list);
    })
    this.api.getNoFlys(this.this_location).then(value => {
      console.log(this.noflys_list);
    })
  }

  getBumDate(bum_id) {
    for (var this_bum of this.noflys_list) {
      if (this_bum.id == bum_id) {
        let bumDate = (this_bum.added).slice(0,10);
        return bumDate;
      }
    }
  }

}
