import { Component } from '@angular/core';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent {
  username: string = '';
  name: string = '';
  password: string = '';
  photo: string = '';

  constructor(private api: ApiService) { }
  
  handleCaptureImage(imageDataUrl: string) {
    this.photo = imageDataUrl;
  }

  submit() {
    this.api.register({
      usuario: this.username,
      nombre_completo: this.name,
      password: this.password,
      photo_base64: this.photo
    }).subscribe(
      {
        next: (response) => {
          alert(response.message);

        },
        error: (error) => {
          alert(error.error.message);
        }
      }
    )
  }
}
