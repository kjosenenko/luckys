import { Component, OnInit } from '@angular/core';
import { Observable, interval, Subscription } from 'rxjs';
import { APIService } from '../api.service';
import {NgbModal, ModalDismissReasons, NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import { ActivatedRoute } from "@angular/router";
import { AuthService } from '../auth.service';

// import { format } from 'path';
// import { templateJitUrl } from '@angular/compiler';

@Component({
  selector: 'customer-view',
  templateUrl: './customer-view.component.html',
  styleUrls: ['./customer-view.component.css']
})
export class CustomerViewComponent implements OnInit {

  private updateSlots: Subscription;
  private currentSlots;
  slots_list_subscription: Subscription;
  slots_list = [];
  this_location = 0;
  locations_subscription: Subscription;
  locations_list = [];
  currentLocation = -1;
  closeResult = '';
  errorMessage = '';
  confirmationVariable = false;
  temporaryFormName = '';
  temporaryFormSlot = '';
  temporaryFormLocation = '';

  constructor(public api: APIService, private route: ActivatedRoute, private modalService: NgbModal, public modal: NgbActiveModal, public auth: AuthService) { 
    this.route.params.subscribe( params => {
        this.this_location = params.id;
        this.api.getOpenSlots()
        if (this.this_location) {
          this.currentLocation = this.this_location;
        } else {
          this.currentLocation = 0;
        }
    });
  }

  ngOnInit() {
    this.slots_list_subscription = this.api.getOpenSlotsList().subscribe(slots_list => {
      this.slots_list = slots_list;
    });      
    this.locations_subscription = this.api.getLocationsList().subscribe(locations_list => {      
      this.locations_list = locations_list;
      this.locations_list.unshift({'id': 0, 'name': 'All Locations'});
    });
  }

  updateSlotsInfo() {
      this.api.getOpenSlots().then(value => {
          console.log('Updated slots from service...');
          console.log(this.slots_list);
      })
  }

  locationName(location_id) {
    for (var this_loc of this.locations_list) {
      if (this_loc.id == location_id) {
        return this_loc.name;
      }
    }
  }

  locationAddress(location_id) {
    for (var this_loc of this.locations_list) {
      if (this_loc.id == location_id) {
        return this_loc.address;
      }
    }
  }

  locationShort(location_id) {
    for (var this_loc of this.locations_list) {
      if (this_loc.id == location_id) {
        return this_loc.name + ' (' + this_loc.address + ')';
      }
    }
  }

  correctTime(slot) {
    let newDate = new Date().toDateString();
    let newerDate = newDate + " " + slot.slot + " GMT-0600 (Mountain Daylight Time)";
    return newerDate;
  }

  setTemporaryFormData(slot, modal) {
    this.temporaryFormName = slot.name;
    this.temporaryFormSlot = this.correctTime(slot);
    this.temporaryFormLocation = this.locationShort(slot.location);
    modal.close('Temporary Form Data Set');
  }

  saveSlot(slot, modal) {
    this.errorMessage = '';
    slot.open = false;
    this.confirmationVariable = true;
    this.api.saveSlotToBackend(slot).then(results => {
      this.updateSlotsInfo();
    },
    err => {
      this.errorMessage = 'Error reserving slot.';
      this.updateSlotsInfo();
    });
    console.log(this.confirmationVariable)
    modal.close('Booked');
  }

  open(content) {
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
      console.log(this.closeResult)
      console.log(content)
      switch (this.closeResult) {
        case 'Booked':
          break;
        default:        
          break;

      }
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
      console.log(this.closeResult)
    });
  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return  `with: ${reason}`;
    }
  }
}
