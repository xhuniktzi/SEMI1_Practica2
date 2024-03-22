import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ViewPhotosComponent } from './view-photos.component';

const routes: Routes = [{ path: '', component: ViewPhotosComponent }];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ViewPhotosRoutingModule { }
