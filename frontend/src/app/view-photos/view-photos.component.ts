import { AfterViewInit, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';
import { IGetPhotosResponse } from '../models/IGetPhotosResponse';

@Component({
  selector: 'app-view-photos',
  templateUrl: './view-photos.component.html',
  styleUrls: ['./view-photos.component.scss']
})
export class ViewPhotosComponent implements OnInit, AfterViewInit{
  username: string = '';

  photosGroupByTag!: Array<{ etiqueta: string, fotos: Array<{ rutaFoto: string; titulo: string;}> }>;

  constructor(private router: ActivatedRoute, private api: ApiService){}

  ngOnInit(): void {
    this.router.paramMap.subscribe(params => {
      this.username = params.get('username')!;
    });
  }

  ngAfterViewInit(): void {
    this.api.getPhotos(this.username).subscribe({
      next: (response) => {
        this.processPhotos(response);
      },
      error: (error) => {
        alert(error.error.message);
      }
    });
  }

  private processPhotos(photos: IGetPhotosResponse[]): void {
    const groupByTag = new Map<string, Array<{rutaFoto: string; titulo: string;}>>();

    photos.forEach(photo => {
      photo.etiquetas.forEach(etiqueta => {
        if (!groupByTag.has(etiqueta)) {
          groupByTag.set(etiqueta, []);
        }
        groupByTag.get(etiqueta)!.push({

          rutaFoto: photo.rutaFoto,
          titulo: photo.titulo
        });
      });
    });

    this.photosGroupByTag = Array.from(groupByTag).map(([etiqueta, fotos]) => ({
      etiqueta,
      fotos
    }));
  }
}
