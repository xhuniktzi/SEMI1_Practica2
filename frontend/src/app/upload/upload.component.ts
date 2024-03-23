import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { ActivatedRoute } from '@angular/router';
import { FormGroup, FormBuilder } from '@angular/forms'; // Import FormGroup and FormBuilder


@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {

  username: string = '';

  title: string = '';
  description: string = '';
  photo_base64: string = '';

  constructor(private api: ApiService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.username = params.get('username')!;
    });
  }

  onFileSelected(event: any) {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];

      const reader = new FileReader();
      reader.onload = (e: any) => {
        const imageBase64 = e.target.result as string;
        const base64Raw = imageBase64.split(',')[1];
        this.photo_base64 = base64Raw;
      };

      reader.readAsDataURL(file);
    }
  }

  onUpload() {
    this.api.uploadPhoto({
      nombre: this.title,
      descripcion: this.description,
      photo_base64: this.photo_base64
      , username: this.username
    }).subscribe({
      next: (response) => {
        alert(response.message);
      },
      error: (error) => {
        alert(error.error.message);
      }
    });
  }

}
