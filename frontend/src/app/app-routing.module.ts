import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: 'login', loadChildren: () => import('./login/login.module').then(m => m.LoginModule) },
  { path: 'register', loadChildren: () => import('./register/register.module').then(m => m.RegisterModule) },
  { path: 'dashboard/:username', loadChildren: () => import('./dashboard/dashboard.module').then(m => m.DashboardModule) },
  { path: 'upload/:username', loadChildren: () => import('./upload/upload.module').then(m => m.UploadModule) },
  { path: 'view-photos/:username', loadChildren: () => import('./view-photos/view-photos.module').then(m => m.ViewPhotosModule) },
  { path: 'edit-profile/:username', loadChildren: () => import('./edit-profile/edit-profile.module').then(m => m.EditProfileModule) },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'extract-text', loadChildren: () => import('./extract-text/extract-text.module').then(m => m.ExtractTextModule) },
  { path: '**', redirectTo: '/login' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
