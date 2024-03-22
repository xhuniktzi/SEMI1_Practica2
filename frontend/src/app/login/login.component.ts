import { Component, ViewChild } from '@angular/core';
import { ApiService } from '../api.service';
import { WebcamComponent } from '../shared/webcam/webcam.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  @ViewChild(WebcamComponent) webcam!: WebcamComponent;
  username: string = '';
  password: string = '';
  photo: string = '';

  constructor(private api: ApiService, private router: Router) { }

  handleCaptureImage(imageDataUrl: string) {
    this.photo = imageDataUrl;
  }

  submit() {
    this.webcam.capture();
    this.api.login({
      usuario: this.username,
      password: this.password,
      photo_base64: this.photo
    }).subscribe(
      {
        next: (response) => {
          alert(response.message);
          this.router.navigate(['/dashboard', this.username]);
        },
        error: (error) => {
          alert(error.error.message);
        }
      }
    )
  }
}
