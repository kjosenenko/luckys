import { Component, OnInit } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import { Observable, interval, Subscription } from 'rxjs';
import { APIService } from '../api.service';
import {NgbModal, ModalDismissReasons, NgbActiveModal} from '@ng-bootstrap/ng-bootstrap';
import { ViewChild } from '@angular/core';

@Component({
  selector: 'shop-view',
  templateUrl: './shop-view.component.html',
  styleUrls: ['./shop-view.component.css']
})
export class ShopViewComponent implements OnInit {
  
  private updateSlots: Subscription;
  private currentSlots;
  slots_list_subscription: Subscription;
  locations_subscription: Subscription;
  noflys_subscription: Subscription;
  slots_list = [];
  locations_list = [];
  noflys_list = [];
  this_location = 0;
  closeResult = '';
  errorMessage = '';
  slotToDelete = null;

  constructor(public api: APIService, private route: ActivatedRoute, private modalService: NgbModal, public modal: NgbActiveModal) { 
    this.route.params.subscribe( params => {
        console.log('Constructor')
        console.log(params); 
        this.this_location = params.id;
        this.api.getLocations();
        this.api.getSlots(this.this_location);
        this.api.getNoFlys(this.this_location);
    });
  }

  ngOnInit() {
    console.log('NgOnInit')
    this.slots_list_subscription = this.api.getSlotsList().subscribe(slots_list => {
      this.slots_list = slots_list;
    });      
    this.locations_subscription = this.api.getLocationsList().subscribe(locations_list => {
      this.locations_list = locations_list;
    });      
    this.noflys_subscription = this.api.getNoFlysList().subscribe(noflys_list => { 
      this.noflys_list = noflys_list;
    }); 
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
      this.api.getSlots(this.this_location).then(value => {
          console.log('Updated slots from service...');
          console.log(this.slots_list);
      })
  }

  saveSlot(slot, modal) {
    console.log(slot)
    slot.open = false;
    this.errorMessage = '';
    this.api.saveSlotToBackend(slot).then(results => {
      this.updateSlotsInfo();
    },
      err => {
        this.errorMessage = 'Error reserving slot';
        this.updateSlotsInfo();
      });
    modal.close('Saved');
  }

  closeUpdateModal(modal) {
    modal.close('Update modal closed');
  }

  removeCustomer(slot, modal) {
    console.log(slot)
    this.errorMessage = '';
    slot.open = true;
    slot.name = '';
    slot.email = '';
    slot.phone = '';
    this.api.saveSlotToBackend(slot).then(results => {
      this.updateSlotsInfo();
    });
    modal.close('Removed');
  }

  seatCustomer(slot, modal) {
    console.log(slot)
    this.errorMessage = '';
    slot.fulfilled = !slot.fulfilled;
    this.api.saveSlotToBackend(slot).then(results => {
      this.updateSlotsInfo();
    },
    err => {
      this.errorMessage = 'Seating Error';
      this.updateSlotsInfo();
    }); 
    modal.close('Seated');
  }

  addToNoFly(bum, modal) {
    bum.nofly = true;
    this.errorMessage = '';
    this.api.saveSlotToBackend(bum).then(results => {
      this.updateSlotsInfo();
    },
    err => {
      this.errorMessage = 'No Fly Error';
      this.updateSlotsInfo();
    });    
    this.api.addBumToNoFly(bum).then( results =>{
      this.api.getNoFlys(this.this_location);
    })
    modal.close('Moved to NoFly');    
  }

  undoNoFly(slot) {
    slot.nofly = false;
    this.errorMessage = '';
    this.api.saveSlotToBackend(slot).then(results => {
      this.updateSlotsInfo();
    },
    err => {
      this.errorMessage = 'No Fly Error';
      this.updateSlotsInfo();
    });
  }

  deleteNoFly(bum, modal) {
    this.api.deleteBum(bum, this.this_location);
    modal.close('Removed from No Fly');
  }

  deleteSlot(slot, modal) {
    this.errorMessage = '';
    this.api.deleteSlotOnBackend(slot, this.this_location).then(results => {
      this.updateSlotsInfo();
    },
      err => {
        this.errorMessage = 'This slot is not open, remove customer before deleting this slot.';
        this.updateSlotsInfo();
      });
    modal.close('Slot Permanently deleted');
  }

  open(content) {
    this.modalService.open(content, {ariaLabelledBy: 'modal-basic-title'}).result.then((result) => {
      this.closeResult = `Closed with: ${result}`;
      console.log('here?')
      console.log(this.closeResult)
      console.log(content)
      switch (this.closeResult) {
        case 'Reserve':
          break;
        case ('Seated'):
          break;
        case 'NoShow':
          break;
        case 'Remove':
          break;
        case 'Delete':      
          break;
        default:        
          break;

      }
    }, (reason) => {
      this.closeResult = `Dismissed ${this.getDismissReason(reason)}`;
      console.log('ahasdf')
      console.log(this.closeResult)
    });
  }

  private getDismissReason(reason: any): string {
    console.log('asdfasd')
    if (reason === ModalDismissReasons.ESC) {
      return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
      return 'by clicking on a backdrop';
    } else {
      return  `with: ${reason}`;
    }
  }

}