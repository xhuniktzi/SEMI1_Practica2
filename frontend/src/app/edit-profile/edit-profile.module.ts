import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EditProfileRoutingModule } from './edit-profile-routing.module';
import { EditProfileComponent } from './edit-profile.component';
import { FormsModule } from '@angular/forms';
import { SharedModule } from "../shared/shared.module";


@NgModule({
    declarations: [
        EditProfileComponent
    ],
    imports: [
        CommonModule,
        EditProfileRoutingModule,
        FormsModule,
        SharedModule
    ]
})
export class EditProfileModule { }
