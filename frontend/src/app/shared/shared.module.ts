import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebcamComponent } from './webcam/webcam.component';



@NgModule({
  declarations: [WebcamComponent],
  imports: [
    CommonModule
  ], exports: [WebcamComponent]
})
export class SharedModule { }
