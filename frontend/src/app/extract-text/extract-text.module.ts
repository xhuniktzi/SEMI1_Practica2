import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ExtractTextRoutingModule } from './extract-text-routing.module';
import { ExtractTextComponent } from './extract-text.component';
import { FormsModule } from '@angular/forms';


@NgModule({
  declarations: [
    ExtractTextComponent
  ],
  imports: [
    CommonModule,
    ExtractTextRoutingModule,
    FormsModule
  ]
})
export class ExtractTextModule { }
