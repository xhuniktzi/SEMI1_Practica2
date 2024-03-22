import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExtractTextComponent } from './extract-text.component';

const routes: Routes = [{ path: '', component: ExtractTextComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ExtractTextRoutingModule { }
