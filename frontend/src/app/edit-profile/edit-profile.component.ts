import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.scss']
})
export class EditProfileComponent implements OnInit {
  currentUsername: string = '';

  username: string = '';
  name: string = '';
  password: string = '';
  photo: string = '';

  constructor(private route: ActivatedRoute, private api: ApiService, private router: Router) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.currentUsername = params.get('username')!;
    });
  }

  handleCaptureImage(imageDataUrl: string) {
    this.photo = imageDataUrl;
  }

  submit() {
    this.api.updateProfile({
      nombre_completo: this.name,
      usuario: this.username,
      password: this.password,
      photo_base64: this.photo
    }, this.currentUsername).subscribe({
      next: (response) => {
        if ('message' in response) {
          alert(response.message);
          this.router.navigate(['/dashboard', this.username]);
        }
      },
      error: (error) => {
        alert(error.error.message);
      }
    });
  }
}
