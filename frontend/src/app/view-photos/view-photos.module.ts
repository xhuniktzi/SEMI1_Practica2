import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ViewPhotosRoutingModule } from './view-photos-routing.module';
import { ViewPhotosComponent } from './view-photos.component';


@NgModule({
  declarations: [
    ViewPhotosComponent
  ],
  imports: [
    CommonModule,
    ViewPhotosRoutingModule
  ]
})
export class ViewPhotosModule { }
