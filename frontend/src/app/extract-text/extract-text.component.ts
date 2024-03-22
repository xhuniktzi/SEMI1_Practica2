import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';

@Component({
  selector: 'app-extract-text',
  templateUrl: './extract-text.component.html',
  styleUrls: ['./extract-text.component.scss']
})
export class ExtractTextComponent implements OnInit {

  username: string = '';

  photo_base64: string = '';

  text: string = '';

  constructor(private route: ActivatedRoute, private api: ApiService) { }

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
    this.api.extractText({
      image_base64: this.photo_base64
    }).subscribe({
      next: response => {
        if ('message' in response) {
          alert(response.message);
        }

        if ('detected_text' in response) {
          this.text = response.detected_text;
        }
      },
      error: error => {
        console.error(error.error.message);
      }
    })
  }
}
