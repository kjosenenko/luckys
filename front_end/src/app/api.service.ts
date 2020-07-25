import { Injectable } from '@angular/core';
import { HttpClient } from  '@angular/common/http';
import { Observable, Subject } from 'rxjs';


@Injectable({
  providedIn: 'root'
})

export class APIService {

  API_URL = 'http://localhost:8000'
  //API_URL = 'https://luckys.blackstardev.com/api'
  private slots = new Subject<any>();
  private openSlots = new Subject<any>();
  private locations = new Subject<any>();
  private noflys = new Subject<any>();
  private currentLocation = new Subject<any>();

  days = [
    'Sunday', 
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday'
  ];

  constructor(private  httpClient:  HttpClient) {
    this.getLocations();
    this.getOpenSlots();
  }

  getSlotsList(): Observable<any> {
    return this.slots.asObservable();
  }

  getOpenSlotsList(): Observable<any> {
    return this.openSlots.asObservable();
  }

  getLocationsList(): Observable<any> {
    return this.locations.asObservable();
  }

  getNoFlysList(): Observable<any> {
    return this.noflys.asObservable();
  }

  getCurrentLocation(): Observable<any> {
    return this.currentLocation.asObservable();
  }

  saveSlotOpeningHoursToBackend(openinghours) {
    return this.httpClient.post(this.API_URL + '/openinghours/' + openinghours.id + '/', openinghours).toPromise().then( result => {
      console.log(result)
    });        
  }

  saveSlotToBackend(slot) {
    return this.httpClient.post(this.API_URL + '/slots/' + slot.id + '/', slot).toPromise().then( result => {
      console.log(result)
    });        
  }

  addBumToNoFly(bum) {
    return this.httpClient.post(this.API_URL + '/noflys/', bum).toPromise().then( result => {
      console.log(result)
      return result;
    });        
  }  

  deleteBum(bum, this_location) {
    return this.httpClient.delete(this.API_URL + '/noflys/' + bum.id + '/').toPromise().then( result => {
      console.log(result)
      this.getNoFlys(this_location)
    });
  }

  deleteSlotOnBackend(slot, this_location) {
    return this.httpClient.delete(this.API_URL + '/slots/' + slot.id + '/').toPromise().then( result => {
      console.log(result)
      this.getSlots(this_location)
    });        
  }

  getLocations() {
    return this.httpClient.get(this.API_URL + '/locations/?format=json').toPromise().then( results => {
      console.log(results)
      this.locations.next(results);
    });    
  }

  getLocation(this_location) {
    return this.httpClient.get(this.API_URL + '/locations/' + this_location + '/?format=json').toPromise().then( results => {
      this.currentLocation.next(results);
      return results
    });    
  }

  getSlots(this_location) {
    console.log('Getting slots...' + this_location)
    return this.httpClient.get(this.API_URL + '/slots/location/' + this_location + '/?format=json').toPromise().then( results => {
      this.slots.next(results);
      console.log(results)
    });        
  }

  getOpenSlots() {
    console.log('Getting OPEN slots...')
    return this.httpClient.get(this.API_URL + '/slots/open/?format=json').toPromise().then( results => {
      this.openSlots.next(results);
      console.log(results)
    });        
  }

  getNoFlys(this_location) {
    console.log('Getting No Flys...' + this_location)
    return this.httpClient.get(this.API_URL + '/noflys/location/' + this_location + '/?format=json').toPromise().then( results => {
      this.noflys.next(results);
      console.log(results)
    });        
  }

  handleError(error: any): Promise <any> {
    console.error('An Error Occured: ', error)
    return Promise.reject(error.message || error)
  }

}

